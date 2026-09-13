from flask import Flask, render_template, request, jsonify
import requests
from config import API_KEY

app = Flask(__name__)

def clean_tag(tag):
    tag = tag.strip().upper()
    if not tag.startswith('#'):
        tag = '#' + tag
    return tag.replace('#', '%23')

HERO_UPGRADE_DAYS = 7
TROOP_UPGRADE_DAYS = 5
SPELL_UPGRADE_DAYS = 6
PET_UPGRADE_DAYS = 8
DEFENCE_UPGRADE_DAYS = 12

def calculate_maxing_stats(player_data):
    th_level = player_data.get('townHallLevel', 15)
    
    # 1. Strict Hero Caps per Town Hall Tier (TH1 to TH18)
    
    hero_max_caps = {
        18: {'Barbarian King': 100, 'Archer Queen': 100, 'Grand Warden': 75, 'Royal Champion': 50, 'Minion Prince': 95},
        17: {'Barbarian King': 95, 'Archer Queen': 95, 'Grand Warden': 70, 'Royal Champion': 45, 'Minion Prince': 90},
        16: {'Barbarian King': 95, 'Archer Queen': 95, 'Grand Warden': 70, 'Royal Champion': 45, 'Minion Prince': 80},
        15: {'Barbarian King': 90, 'Archer Queen': 90, 'Grand Warden': 65, 'Royal Champion': 40, 'Minion Prince': 70},
        14: {'Barbarian King': 80, 'Archer Queen': 80, 'Grand Warden': 55, 'Royal Champion': 30, 'Minion Prince': 60},
        13: {'Barbarian King': 75, 'Archer Queen': 75, 'Grand Warden': 50, 'Royal Champion': 25,'Minion Prince': 50},
        12: {'Barbarian King': 65, 'Archer Queen': 65, 'Grand Warden': 40,'Minion Prince': 40},
        11: {'Barbarian King': 40, 'Archer Queen': 40, 'Grand Warden': 20,'Minion Prince': 30},
        10: {'Barbarian King': 40, 'Archer Queen': 40,'Minion Prince': 20},
        9:  {'Barbarian King': 30, 'Archer Queen': 30,'Minion Prince': 10},
        8:  {'Barbarian King': 10},
        7:  {'Barbarian King': 5},
    }
    active_hero_caps = hero_max_caps.get(th_level, {'Barbarian King': 5, 'Archer Queen': 5, 'Grand Warden': 5, 'Royal Champion': 5})

    heroes_days = 0
    adjusted_heroes = []
    for hero in player_data.get('heroes', []):
        name = hero.get('name')
        if name in active_hero_caps:
            max_level = active_hero_caps[name]
            hero['maxLevel'] = max_level  # Overwrite global API maxLevel with TH-specific cap
            levels_left = max(0, max_level - hero.get('level', 0))
            heroes_days += levels_left * HERO_UPGRADE_DAYS
            adjusted_heroes.append(hero)
    
    player_data['heroes'] = adjusted_heroes
    # 2. Strict Lab Max Caps per Town Hall Tier (Troops & Spells)
    # Mapping maximum allowed laboratory level caps for TH15 and TH16 as baseline examples, falling back safely
    lab_max_caps = {
        15: {
            'Barbarian': 11, 'Archer': 11, 'Giant': 11, 'Goblin': 9, 'Wall Breaker': 11,
            'Balloon': 10, 'Wizard': 11, 'Healer': 8, 'Dragon': 10, 'P.E.K.K.A': 10,
            'Minion': 11, 'Hog Rider': 12, 'Valkyrie': 10, 'Golem': 12, 'Witch': 6,
            'Lava Hound': 6, 'Bowler': 7, 'Baby Dragon': 9, 'Miner': 9, 'Electro Dragon': 6,
            'Yeti': 5, 'Dragon Rider': 3, 'Electro Titan': 3, 'Root Rider': 2, 'Apprentice Warden': 4,
            'Lightning Spell': 10, 'Healing Spell': 9, 'Rage Spell': 6, 'Jump Spell': 5,
            'Freeze Spell': 7, 'Poison Spell': 9, 'Earthquake Spell': 6, 'Haste Spell': 5,
            'Clone Spell': 8, 'Skeleton Spell': 8, 'Bat Spell': 6, 'Invisibility Spell': 4,
            'Recall Spell': 4, 'Revive Spell': 2
        },
        16: {
            'Barbarian': 12, 'Archer': 12, 'Giant': 12, 'Goblin': 10, 'Wall Breaker': 12,
            'Balloon': 11, 'Wizard': 12, 'Healer': 9, 'Dragon': 11, 'P.E.K.K.A': 11,
            'Minion': 12, 'Hog Rider': 13, 'Valkyrie': 11, 'Golem': 13, 'Witch': 7,
            'Lava Hound': 7, 'Bowler': 8, 'Baby Dragon': 10, 'Miner': 10, 'Electro Dragon': 7,
            'Yeti': 6, 'Dragon Rider': 4, 'Electro Titan': 4, 'Root Rider': 3, 'Apprentice Warden': 5,
            'Lightning Spell': 11, 'Healing Spell': 10, 'Rage Spell': 7, 'Jump Spell': 6,
            'Freeze Spell': 8, 'Poison Spell': 10, 'Earthquake Spell': 7, 'Haste Spell': 6,
            'Clone Spell': 9, 'Skeleton Spell': 9, 'Bat Spell': 7, 'Invisibility Spell': 5,
            'Recall Spell': 5, 'Revive Spell': 3
        }
    }
    active_lab = lab_max_caps.get(th_level, {})

    army_days = 0
    pet_names = ['L.A.S.S.I', 'Electro Owl', 'Mighty Yak', 'Unicorn', 'Frosty', 'Diggy', 'Poison Lizard', 'Phoenix', 'Spirit Fox', 'Angry Jelly']

    for troop in player_data.get('troops', []):
        name = troop.get('name')
        if name in pet_names:
            continue
        # Use TH-specific max cap if available, otherwise cap to current level if no dict exists for lower THs
        max_lvl = active_lab.get(name, troop.get('maxLevel', troop.get('level', 1)))
        curr_lvl = troop.get('level', 1)
        levels_left = max(0, max_lvl - curr_lvl)
        army_days += levels_left * TROOP_UPGRADE_DAYS

    for spell in player_data.get('spells', []):
        name = spell.get('name')
        max_lvl = active_lab.get(name, spell.get('maxLevel', spell.get('level', 1)))
        curr_lvl = spell.get('level', 1)
        levels_left = max(0, max_lvl - curr_lvl)
        army_days += levels_left * SPELL_UPGRADE_DAYS

    # 3. Defences calculation scaled to TH level
    defences_multiplier = {
        18: 60, 17: 55, 16: 50, 15: 42, 14: 35, 
        13: 28, 12: 22, 11: 18, 10: 12, 9: 8, 8: 5, 7: 3, 6: 2
    }
    total_defences_left = defences_multiplier.get(th_level, 15)
    defences_days = total_defences_left * DEFENCE_UPGRADE_DAYS

    # 4. Strict Pet Max Caps per Town Hall Tier (TH14 to TH18)
    pet_max_caps = {
        18: {'L.A.S.S.I': 15, 'Electro Owl': 15, 'Mighty Yak': 15, 'Unicorn': 15, 'Frosty': 15, 'Diggy': 15, 'Poison Lizard': 15, 'Phoenix': 15, 'Spirit Fox': 15, 'Angry Jelly': 15},
        17: {'L.A.S.S.I': 10, 'Electro Owl': 10, 'Mighty Yak': 10, 'Unicorn': 10, 'Frosty': 10, 'Diggy': 10, 'Poison Lizard': 10, 'Phoenix': 10, 'Spirit Fox': 10, 'Angry Jelly': 10},
        16: {'L.A.S.S.I': 15, 'Electro Owl': 15, 'Mighty Yak': 15, 'Unicorn': 10, 'Frosty': 10, 'Diggy': 10, 'Poison Lizard': 10, 'Phoenix': 10, 'Spirit Fox': 10, 'Angry Jelly': 10},
        15: {'L.A.S.S.I': 15, 'Electro Owl': 10, 'Mighty Yak': 15, 'Unicorn': 10, 'Frosty': 10, 'Diggy': 10, 'Poison Lizard': 10, 'Phoenix': 10},
        14: {'L.A.S.S.I': 10, 'Electro Owl': 5, 'Mighty Yak': 10, 'Unicorn': 10},
    }
    active_pet_caps = pet_max_caps.get(th_level, {})

    pets_days = 0
    for troop in player_data.get('troops', []):
        name = troop.get('name')
        if name in active_pet_caps:
            max_level = active_pet_caps.get(name, troop.get('level', 1))
            levels_left = max(0, max_level - troop.get('level', 0))
            pets_days += levels_left * PET_UPGRADE_DAYS

    total_days = heroes_days + army_days + defences_days + pets_days
    
    return {
        "heroesDays": heroes_days,
        "armyDays": army_days,
        "defencesDays": defences_days,
        "petsDays": pets_days,
        "totalDays": total_days
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/player', methods=['GET'])
def get_player_data():
    raw_tag = request.args.get('tag', '')
    if not raw_tag:
        return jsonify({"error": "No player tag provided"}), 400
    
    formatted_tag = clean_tag(raw_tag)
    url = f"https://api.clashofclans.com/v1/players/{formatted_tag}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        maxing_stats = calculate_maxing_stats(data)
        data['maxingEstimates'] = maxing_stats
        return jsonify(data)
    else:
        return jsonify({"error": "Player not found"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=8000)