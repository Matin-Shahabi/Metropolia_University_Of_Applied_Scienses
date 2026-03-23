# Mankind vs AI: The Terminal Escape

Set on a dark, rain-soaked night, you are humanity’s final hope. The enemy, an AI-powered global police force. It hunts you relentlessly.

As your engine roars to life on the misty runway, alarms blare in the AI command center. Endless data streams flash across their systems as they calculate the location of one fugitive human, you. Hidden in your suitcase is the world’s last chance for survival: a next-generation chip meant for the final manned crew preparing to flee from an airport on the other side of the world. The AI has limitless speed, intelligence, and resources. You have only your wits, your knowledge of geography, and a dwindling stash of cash.

You dream that one day, humanity will reclaim the AI-infested Earth. But that hope comes with responsibility. You can’t simply blaze through airports or take reckless flights. Every move, every mile flown, leaves a CO₂ trace you’d rather not worsen. Yet the AI police are learning fast, adapting with every decision you make, for real.

Suddenly, the departure hall’s screen flickers to life. The AI is watching. You have a decision to make.

Choose carefully. Move too aggressively, and you’ll drain your funds and choke the planet you’re trying to save. Move too slowly, and the AI will outthink and overtake you. Every trip wastes fuel, costs money, and raises your risk of capture.

Every decision counts. Mankind’s survival depends on your speed, strategy, and resource management. Only those who master the balance, risk, timing, precision and good old geography might live to see the hidden hangar doors open and the final escape plane waiting beyond them.

Set against wind, rain, roaring engines, and neon-lit runways, Mankind Vs AI: The Terminal Escape is more than a game of chance—it’s a test of survival under pressure. One wrong move, and all of humanity is lost.


## 🚀 Quick Start

### Prerequisites
- Python 3.x
- MariaDB/MySQL database
- Airport database (flight_game schema)

### Database Setup

1. **One-time setup** - Creates player profiles, game sessions, and leaderboard tables:

   **Option A (Linux/MacOS): Shell script**
   ```bash
   ./setup_db.sh
   ```

   **Option B (WIndows): Python script**
   ```bash
   python3 setup_db.py
   ```

   Both scripts are idempotent (safe to run multiple times) and will only create missing tables/views.
   Remember to change the database connection strings to the one you are using locally.

2. **Database CLI tool (Optional)** - Inspect database, view stats, manage data:
```bash
./db_cli.sh
```

### Run the Game

```bash
python3 main.py
```

**First time?**
1. Enter your player name (creates your profile automatically)
2. Choose **[S]tory** to read the game narrative (optional)
3. Choose **[N]ew game** to start
4. Select flights by entering 1-5
5. Press **Q** to quit (auto-saves your progress)

**Returning player?**
1. Enter your name
2. Choose **[C]ontinue** to resume your saved game
3. Or view **[M]yScore** for your statistics and **[L]eaderboards**

## 🎮 How to Play

### Menu Options
- **[S]tory** - Read the cinematic game narrative (3 parts)
- **[C]ontinue** - Resume your saved game (if available)
- **[N]ew game** - Start a fresh escape attempt
- **[M]yScore** - View your personal statistics and best records
- **[L]eaderboard** - See global rankings for CO2 efficiency and speed
- **[Q]uit** - Exit the game

### Objective
Reach your safe airport before:
- The police catch you
- You run out of money
- You run out of CO2 credits

### Each Round
1. **View status** - See your current location, resources, and distance to safety
2. **Choose flight** - Select from 1-5 available destinations
3. **Pay costs** - Money and CO2 deducted based on distance
4. **Police search** - AI searches nearby airports (catch chance increases each round)
5. **Repeat** - Continue until you win or lose

### Strategy Tips
- **Geography matters** - Flights closer to your target appear more often
- **Watch resources** - Balance speed vs conservation
- **Safe airport chance** - Increases as you get closer
- **Police pressure** - Catch probability rises every round

## 📊 Features

✅ **Cinematic Story** - Read the dramatic narrative in 3 parts  
✅ **Player Profiles** - Unique accounts with persistent stats  
✅ **Auto-Save** - Progress saved after every round  
✅ **Save/Resume** - Pause and continue games anytime  
✅ **Personal Bests** - Track your best CO2 efficiency and speed  
✅ **Global Leaderboards** - Compete for top CO2/speed rankings  
✅ **Game History** - View all your past games and outcomes  
✅ **Input Validation** - Clear error messages guide you through menus  

## 🗄️ Database Tools

### Setup Scripts (`setup_db.sh` / `setup_db.py`)
- Idempotent setup (safe to run multiple times)
- Creates required tables and views
- Verifies database structure
- Available in both shell and Python versions

### CLI Utility (`db_cli.sh`)
Interactive menu with options:
- Show all tables and schemas
- View player stats and game history  
- Check active/unfinished games
- Display leaderboards
- Show database size and health

### Manual Queries
For direct database access:
```sql
-- View all players
SELECT * FROM players;

-- Check your games
SELECT * FROM player_game_sessions WHERE player_id = YOUR_ID;

-- See leaderboards
SELECT * FROM global_leaderboard_co2 LIMIT 10;
SELECT * FROM global_leaderboard_speed LIMIT 10;
```

## 📁 Project Structure

```
├── main.py              # Game entry point
├── game.py              # Main game logic and loops
├── flights.py           # Flight generation and selection
├── police.py            # AI police search logic
├── db.py                # Airport database queries
├── player_db.py         # Player/session database API
├── constants.py         # Game balancing settings
├── utils.py             # Helper functions
├── setup_db.sh          # Database setup script (bash)
├── setup_db.py          # Database setup script (python)
├── db_cli.sh            # Database management CLI
├── setup_database.sql   # Database schema (tables + views)
└── db_client_utility.sql # Query collection for CLI
```

## 🐛 Troubleshooting

**Database connection failed?**
- Check MariaDB is running: `sudo systemctl status mariadb`
- Verify credentials in `db.py` and scripts
- Ensure `test_flight_game_db` database exists

**Tables missing?**
```bash
./setup_db.sh  # Shell version
# or
python3 setup_db.py  # Python version
```

**Game won't save?**
- Check database connection
- Look for errors in terminal output

## 🏆 Leaderboards

Compete globally in two categories:
1. **CO2 Efficiency** - Use the least CO2 to reach safety
2. **Speed** - Win in the fewest rounds

View rankings:
- In-game: Choose **[L]eaderboard** from menu
- CLI tool: Run `./db_cli.sh` → option 10
- Direct query: See "Manual Queries" above

## 🎯 Tips for High Scores

- Choose flights that move you closer to the target
- Geography knowledge reduces costs (shorter distances)
- Balance risk vs progress - faster isn't always better
- Study the leaderboards to see winning strategies

**Pro tip:** Geography knowledge helps! Getting closer to your destination increases the chance of finding direct flights.

---

**Ready to escape in the termninal?** Run `python3 main.py` and start your journey! ✈️