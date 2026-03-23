# MANKIND VS AI: The Terminal Escape
## Requirements Specification Document

---

## 1. Introduction

This document serves as the requirement specification for a flight game project as part of the course work in the software-1 module at Metropolia University of Applied Sciences. It is structured for the course instructors, class-mates, members of the development team in Group 10, and for the general users. Below, a clear explanation of the vision of the game, its main features, database usage, quality requirements, sustainability considerations, and technical constraints will be explained.

---

## 2. Vision

### 2.1 General Idea

This game is an interactive airport strategy game developed using a relational database and a Python environment. Mankind (Player) here is considered to be a robber while AI with its innovative thinking plays the police.

The player travels the world between airports with a specific goal in mind to reach a certain destination airport while managing money and CO₂ emission. In order to win, the player must make his way to a location designated as the safe airport while navigating through available airports.

The idea behind this game is to be able to combine strategy, geography, resource management and awareness on sustainable travel choices.

---

## 3. Functional Requirements

### 3.1 Gameplay

#### Game Start
- The user should be able to create a new profile or load an already existing player profile.
- The starting and destination airport should never be the same during a new game play session start.
- These airports should be generated randomly, from a list of one large airport per country.

#### During Game Play
- The user should be able to save, quit, see status, resources, restart a game session at any moment in the game during their turn.
- After each round, the players' available money and CO₂ credit should be recalculated based on the flight distance they travelled.
- The program logic should always offer flight options that are closer to the destination than current location if available.
- Safe airports should NOT appear as a flight option for at least 3 rounds of play.
- Getting closer to the safe airport should increase the probability of getting the final flight to the safe airport, capped max at 75% (configurable).
- The probability of Police AI winning should start at 0% and increase on every turn by a set amount, capped max at 50% (configurable).

#### Game End (Win or Game Over)
- The game ends (Player Wins) when the player has reached the safe airport without finishing the allocated money and CO₂ credit.
- The game ends (Game Over) when the Police AI catches the player (increasing probability with a max set at 50%).

### 3.2 Database Requirements

In order to save player information and game progress and support game statistics, new tables and views are added to the original airport database used in the course work.

### 3.3 User Interaction

- This game will be fully playable using keyboard input and in the terminal.
- Invalid input shall not crash the program and rather be handled gracefully.

### 3.4 Game Goal: The Story

This game has a concrete and direct objective: mankind survival. That is, the player must manage his resources and avoid the AI at all cost to reach the safe airport.

---

## 4. Quality Requirements

### 4.1 Usability
- At the start of the game, clear instructions are shown to help the players experience.
- Simple numeric inputs are being demanded for the game input and clear informative feedback is shown back to the player.
- There should be clear documentation and starting guide for future developers and maintainers of the game.

### 4.2 Reliability
- The software used to play this game shall not crash by wrong user input.
- Data, such as game play sessions, should be safely and reliably stored in the database.

### 4.3 Performance
- Database queries shall be efficiently executed with a game response time of less than 1 second.
- **Note:** Police AI search in the airports will take 2 seconds per search, a total of 10 seconds for 5 airports for improving game tension and feel. This is configurable.

### 4.4 Maintainability
- The various codes have been separated into different modules with clear function names for easy modifications and tracking.
- Game data is stored safely and promptly to avoid data loss.

### 4.5 Security
- Reasonable efforts should be made to make the software safe and secure across vulnerabilities.
- As this project is part of both Python Studies and Database Studies, the software should implement secure coding and input validation to prevent SQL injection.
- The source code, documentation, and related materials should be stored safely and securely in a version control system such as GitHub.

---

## 5. Sustainable Development Consideration

This game shall support and promote sustainability by taking into consideration CO₂ emission per flight and limiting total allowed emission. This leads to encouraging environmental responsibility choices making the player aware of the impact of flying too much and over long distances.
