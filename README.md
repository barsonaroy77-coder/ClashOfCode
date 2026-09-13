# ClashOfCode ⚔️

An advanced, responsive web application built with **Flask** and **Tailwind CSS** that interfaces directly with the official **Supercell API**. It delivers comprehensive player intelligence, localized Town Hall level caps (TH1 through TH18), and precise upgrade analytics to help players track their maxing progress.

---

## 📸 Preview
<p align="center">
<img width="1916" height="857" alt="image" src="https://github.com/user-attachments/assets/0c8fd451-c969-4e51-954d-008e1644e8d8" />
</p>

---

## ✨ Features

- **Dynamic Town Hall Scaling :** Automatically overrides global API caps to match the specific upgrade maximums for the player's exact Town Hall tier.
- **Comprehensive Progression Vectors:** Tracks four major upgrade categories independently:
  - **Heroes** (including all heroes according to the town hall)
  - **Lab & Armies** (Troops, Spells, and Siege Machines organized via clean exclusive accordions)
  - **Defences** (Major structural upgrade timeline estimators)
  - **Pets** (Tracked natively from Town Hall 14 onwards)
- **Visual Analytics:** Real-time **Chart.js** bar graph visualization mapping out remaining upgrade days across categories.
- **Cozy Dark Aesthetic UI:** A modern, polished dark mode interface styled with Tailwind CSS, featuring soft contrast containers, smooth scrollbars, and high-visibility status badges.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Requests
- **Frontend:** HTML5, Tailwind CSS, Chart.js
- **API:** Official Supercell Clash of Clans Developer API

---

## 🚀 Getting Started

### Prerequisites
Ensure you have Python installed on your local machine along with Flask and Requests.

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/ClashOfCode.git](https://github.com/your-username/ClashOfCode.git)
   cd ClashOfCode
