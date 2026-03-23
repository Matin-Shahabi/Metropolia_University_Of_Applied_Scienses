from constants import MAX_FLIGHT_OPTIONS
from db import get_large_airports
from utils import debug_print
import random
import time

COUNTRY_NAMES = None  # To be set by game.py

def search_airports(player_airport):
    airports = get_large_airports()
    nearby = random.sample(airports, min(MAX_FLIGHT_OPTIONS, len(airports)))
    if player_airport not in nearby:
        nearby.append(player_airport)
    return nearby

def police_turn(player_airport, police_chance):
    print("\n👮 Police is searching nearby airports...", flush=True)
    debug_print(f"Police catch probability: {round(police_chance*100,2)}%")
    nearby = search_airports(player_airport)
    for airport in nearby:
        time.sleep(2)
        country_name = COUNTRY_NAMES.get(airport['iso_country'], airport['iso_country'])
        print(f"Police checking: {airport['name']} ({country_name})", flush=True)
        time.sleep(0.3)
        roll = random.random()
        debug_print(f"Police roll: {round(roll,4)}")
        if airport["ident"] == player_airport["ident"] and roll < police_chance:
            print(f"\n💀 Police caught you at {airport['name']}! Game Over!")
            return True
    print("Police did not find you this turn.")
    return False
