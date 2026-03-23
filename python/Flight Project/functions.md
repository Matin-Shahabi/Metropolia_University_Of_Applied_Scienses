| Function                        | Location      | Purpose                                                       |
| ------------------------------- | ------------- | ------------------------------------------------------------- |
| `debug_print`                   | utils.py      | Prints debug info if DEBUG=True                               |
| `haversine`                     | utils.py      | Calculates distance between two coordinates                   |
| `country_iso_to_name`          | db.py         | Loads ISO → Country mapping from DB                           |
| `get_large_airports`             | db.py         | Returns all large airports (1 per country)                    |
| `get_airport_details`          | db.py         | Returns airport by ident (updates player location)            |
| `get_random_airport`            | db.py         | Returns a random airport, optionally excluding a country      |
| `search_airports`        | police.py     | Chooses nearby airports for police search                     |
| `police_turn`           | police.py     | Simulates police check, may end game if caught                |
| `get_closer_airports`   | flights.py    | Returns airports closer to safe airport than current          |
| `get_available_flights` | flights.py    | Chooses flights intelligently using distance + chance         |
| `show_flight_options`        | flights.py    | Prints flight options with cost/CO2 for the player            |
| `player_choice`          | flights.py    | Gets and validates player input for flight                    |
| `execute_player_choice`            | game.py       | Deducts money/CO2 and updates player location                 |
| `update_flight_availability`            | game.py       | Updates probability of safe airport appearing                 |
| `display_status`                  | game.py       | Prints round info, player status, distance to safe airport    |
| `start_game`                    | game.py       | Main loop: orchestrates rounds, flights, police, and win/loss |
