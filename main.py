import requests
import json
import os
import config



# 1. Paste your long API token from the Supercell Developer portal here
API_KEY =config.API_KEY
# CRITICAL: You must replace the '#' in your tag with '%23'
# Example: If your tag in-game is #YQ89RR, you must write "%23YQ89RR"
PLAYER_TAG = "%23R28VYRQVV"

def fetch_player_data():
    url = f"https://api.clashofclans.com/v1/players/{PLAYER_TAG}"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }

    
    print("Connecting to Clash of Clans API...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        # Save the data to a local JSON file
        with open("player_data.json", "w") as file:
            json.dump(data, file, indent=4)
            
        print(f"Success! Data for {data.get('name')} saved to player_data.json")
    
    # Custom error messages to help you debug common API issues
    elif response.status_code == 403:
        print("Error 403: Access Denied. Check if your API key is correct and your IP address matches the one registered on the developer portal.")
    elif response.status_code == 404:
        print("Error 404: Player not found. Make sure you used %23 instead of # in your PLAYER_TAG variable.")
    else:
        print(f"Failed to fetch data. Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    fetch_player_data()