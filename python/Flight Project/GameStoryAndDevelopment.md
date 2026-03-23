# Mankind Vs AI: The TerminalEscape Design Document

## 1. Overview

Mankind vs AI: The Terminal Escape is a strategy game that combines knowledge of geography and resource management. A player(theif)/Human tries to reach their safe airport by utilising their knowledge of geography and managing their limited resources (money and co2 credit) before the police(AI) catches them. The game is played in the terminal, and the player tries to escape by flying through airports(or terminals) and hence the title.

Spoiler: KNowledge of geography helps in choosing the better flights, as naturally the closer you get to your desired airport, the more chances are you will get flights to your safe airport, and cheaper. But thats not all :) Add more spoilets and tips as the game round progresses

Spoiler 2: The chances of the AI catching the thief increases on every round of game play.

spoiler 3:

spoiler 4:
 .
 .
 .

## 2. Play Flow

1. **Play Start** - ONe time operation
    - Initialize constants and constraints that will impact the game play expereice, such as making it hard, easy, resource limits and so on.
    - Load country mapping from DB.
    - Set game session target (starting and safe airports).
2. **Play rounds** - Loops untill game session ends
    - DIsplay relevant player information.
    - Generate and display flight options.
    - Get player input (validate for correctness)
    - Update player status (money, CO2, current location, etc).
    - Increase/decrease the chance that flight to safe airport will become available next round if not caught by police.
    - Check game session status for thief(win if arrived in safe airport, loss if resources run out).
    - Execute police turn including game session status check for police.
    - Increase chance police will catch thief next round.

## 3. Modules, Functions and requirments

- **Game Constraints**: Contains all game constraints for controlling game feel, for example controlling reward for knowldge vs random choices.

- **Main Software Module**: Start the game session.

- **Game Module**: Main game logic and rounds; includes player turns, resource tracking, game session status, etc.

- **DataBase Module**: Handles all database connections and queries for airports and countries.

- **Utilities**: Common helper functions such as distance calculations, debuging, etc.

- **Flights Module**: FOr managing available flight options and player choices.

- **Police Module**: Handles police search logic and turn resolution.


## 4. Module & Function Requirements

### constants.py
- Define all game balancing constants (starting money, CO2, costs, police probabilities, etc.).


### game.py

- **execute_player_choice(money, co2, selected, cost, co2_cost)**: update player status based on choices made

- **update_flight_availability(old_distance, new_distance, flight_availability)**: Flight availability to safe airport depending on player progress.

- **display_status(round_no, money, co2, current, safe_airport)**: Show game round status and return distance to the safe airport.

- **start_game()**: Main game loop; orchestrates all game actions and checks win/loss conditions.

### db.py
- **get_large_airports()**: A list of one large airport per country the DB.

- **get_airport_details(ident)**: Return airport details using ident.

- **get_random_airport(exclude_country=None)**: Returns a single random airport. If exclude is set, the random airport will not include the country set in exclude.

- **country_iso_to_name()**: Map of country names to ISO country codes.


### utils.py

- **debug_print(message)**: Print debug messages if DEBUG is enabled.

- **get_distance(lat1, lon1, lat2, lon2)**: Calculates distance between two coordinates

### flights.py

- **get_closer_airports(current, airports, safe_airport)**: list of available airports that are closer to safe airport than current location.

- **get_available_flights(current, safe_airport, destination_availability)**: Generate a list of flight options, prioritizing closer airports and possibly including the safe airport. Get list of available flights. Closer airports, if available should be offered first including the safe airport based on the probability of its availability

- **show_flight_options(current, safe_airport, destination_availability)**: Print available flight options and return their details.

- **player_choice(flights_info)**: Get and validate the player's input such as next flight, game continuation etc.

### police.py

- **search_airports(player_airport)**: list of airports for the police to search. Must include player's current airport as there is always a chance catch thief.

- **police_turn(player_airport, police_chance)**: Simulate a police search and determine if the player is caught.


## 5. Example Game Flow

1. Player enters their name.
2. Game selects a random starting airport and a different safe airport.
3. Each round:
    - Player sees their status and available flights.
    - Player chooses a flight (or quits).
    - Costs are applied; location is updated.
    - Safe airport chance is updated.
    - Police may search and catch the player.
    - Game ends if player wins, runs out of resources, or is caught.

## 6. Planned Features & Improvements

### 1. Player Session Persistence
- Add a new table to the database to store player names and their game state (current location, money, CO2, safe airport, police chance, etc.).
- When a player starts the game, prompt for their name. If a session exists and is not finished (not game over or won), offer to continue or start over.
- If the previous session ended (win or loss), archive the session and allow a new game to begin.
- This enables players to resume unfinished games and prevents replaying completed sessions.

### 2. Personal Best / High Score Tracking
- Track each player's best performance (e.g., fewest rounds, most money/CO2 left, fastest win, etc.).
- Store personal bests in the database and display them at the end of each game or somewhere that makes sense

### 3. Global Leaderboard
- Maintain a leaderboard table in the database to track top performances across all players.
- Show rankings based on criteria such as fastest win, most resources left, or other metrics.
- Display the leaderboard on game start or after a game ends.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Mankind Vs AI: The TerminalEscape                        |
|                            Database Schema                                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────┐
│       PLAYERS           │
├─────────────────────────┤
│ • player_id (PK)        │◄────┐
│ • player_name (UNIQUE)  │     │
│ • created_at            │     │
│ • last_played           │     │  1:N relationship
│ • total_games           │     │  (One player, many sessions)
│ • games_won             │     │
│ • games_lost            │     │
└─────────────────────────┘     │
                                │
                                │
                    ┌───────────┴──────────────┐
                    │                          │
        ┌───────────▼───────────┐    ┌────────▼──────────┐
        │   GAME_SESSIONS       │    │ player_statistics │
        ├───────────────────────┤    │     (VIEW)        │
        │ • session_id (PK)     │    ├───────────────────┤
        │ • player_id (FK) ─────┼───►│ Aggregated stats  │
        │ • start_airport       │    │ • win_rate        │
        │ • safe_airport        │    │ • best_co2        │
        │ • current_airport     │    │ • best_money      │
        │ • money               │    │ • fastest_rounds  │
        │ • co2                 │    └───────────────────┘
        │ • round_no            │
        │ • police_chance       │
        │ • flight_availability │
        │ • status              │◄───────┐
        │ • started_at          │        │
        │ • finished_at         │        │  Used by leaderboard views
        │ • final_co2_used      │────────┤
        │ • final_money_used    │        │
        │ • final_rounds        │        │
        └───────────────────────┘        │
                                         │
                                         │
               ┌─────────────────────────┴──────────────────────────┐
               │                                                     │
   ┌───────────▼───────────────┐              ┌────────────────────▼──────┐
   │ global_leaderboard_co2    │              │ global_leaderboard_speed  │
   │        (VIEW)             │              │         (VIEW)            │
   ├───────────────────────────┤              ├───────────────────────────┤
   │ Top 100 players by        │              │ Top 100 players by        │
   │ CO2 efficiency            │              │ speed (fewest rounds)     │
   │ • player_name             │              │ • player_name             │
   │ • co2_used (MIN)          │              │ • rounds (MIN)            │
   │ • rounds                  │              │ • co2_used                │
   │ • finished_at             │              │ • money_used              │
   └───────────────────────────┘              │ • finished_at             │
                                              └───────────────────────────┘

