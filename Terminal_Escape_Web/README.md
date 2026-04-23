# 🛫 Mankind vs AI: Terminal Escape

**Final Project - Software 1 Course**  
**Metropolia University of Applied Sciences**

A web-based strategy game where humanity tries to escape from an AI-controlled global police force by managing limited resources (Money & CO₂) while using geography knowledge.

---

## ✨ Features

- Modern, clean and responsive web interface using **Tailwind CSS**
- Interactive world map with **Leaflet.js** showing current location and safe airport
- Player registration and persistent game sessions (Save / Resume)
- Real-time flight selection with cost and CO₂ consumption displayed
- Police chase system with increasing probability
- Global Leaderboards (CO₂ Efficiency & Speed)
- Personal statistics and best records
- Full REST API backend with JSON communication

---

## 🛠 Tech Stack

**Backend:**
- Python + Flask
- MySQL / MariaDB
- mysql-connector-python

**Frontend:**
- HTML5 + Tailwind CSS
- Vanilla JavaScript
- Leaflet.js (Interactive Map)

**Database:**
- Airport database extended with `players` and `player_game_sessions` tables

---

## 🚀 How to Run

### Prerequisites
- Python 3.8+
- MariaDB/MySQL with database `terminal_escape_web`
- `setup_database.sql` already executed

### Quick Start

```bash
# 1. Go to project root
cd terminal-escape-web

# 2. Run the game (recommended)
./run.sh

---


## 🎮 How to Play

- Enter your player name
- The game starts or resumes automatically
- Study the map — your current position and safe airport are marked
- Choose a flight from the available options
- Check the cost and CO₂ of each flight before choosing
- Manage your resources wisely — running out of money or CO₂ = Game Over
- Reach the safe airport before the police catches you

Tip: Getting closer to the safe airport increases the chance of direct flights appearing.

## 🏆 Leaderboards
- Two competitive categories:

- CO₂ Efficiency – Lowest CO₂ used to win (Sustainability focus)
- Speed – Fewest rounds to reach the safe airport




## Project Of Group 4 