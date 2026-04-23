# backend/models/game_logic.py
import random
from services.db import get_cursor
from utils import get_distance
from config import Config

def get_airport_details(ident):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM airport WHERE ident = %s", (ident,))
    return cursor.fetchone()

def get_large_airports():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM airport WHERE type = 'large_airport' GROUP BY iso_country")
    return cursor.fetchall()

def get_random_airport(exclude_country=None):
    airports = get_large_airports()
    if exclude_country:
        airports = [a for a in airports if a["iso_country"] != exclude_country]
    return random.choice(airports)

# ====================== Flight Logic ======================

def get_closer_airports(current, airports, safe_airport):
    current_dist = get_distance(
        current['latitude_deg'], current['longitude_deg'],
        safe_airport['latitude_deg'], safe_airport['longitude_deg']
    )
    closer = [
        a for a in airports 
        if a["ident"] != current["ident"] and
        get_distance(a['latitude_deg'], a['longitude_deg'],
                     safe_airport['latitude_deg'], safe_airport['longitude_deg']) < current_dist
    ]
    random.shuffle(closer)
    return closer

def get_available_flights(current, safe_airport, flight_availability, round_no):
    airports = get_large_airports()
    options = []
    
    # Safe airport after round 3
    if round_no >= 3 and random.random() < flight_availability:
        if safe_airport not in options:
            options.append(safe_airport)
    
    # Closer airports
    closer = get_closer_airports(current, airports, safe_airport)
    for airport in closer:
        if airport not in options and len(options) < Config.MAX_FLIGHT_OPTIONS:
            options.append(airport)
    
    # Fill remaining
    if len(options) < Config.MAX_FLIGHT_OPTIONS:
        remaining = [a for a in airports if a not in options and a["ident"] != current["ident"]]
        if round_no < 3:
            remaining = [a for a in remaining if a["ident"] != safe_airport["ident"]]
        random.shuffle(remaining)
        options.extend(remaining[:Config.MAX_FLIGHT_OPTIONS - len(options)])
    
    random.shuffle(options)
    return options[:Config.MAX_FLIGHT_OPTIONS]

def calculate_flight_cost(current, destination):
    distance = get_distance(
        current['latitude_deg'], current['longitude_deg'],
        destination['latitude_deg'], destination['longitude_deg']
    )
    money_cost = int(distance * Config.COST_PER_KM)
    co2_cost = int(distance * Config.CO2_PER_KM)
    return money_cost, co2_cost, int(distance)

# ====================== Police Logic ======================

def police_turn(current_airport, police_chance):
    airports = get_large_airports()
    nearby = random.sample(airports, min(5, len(airports)))
    if current_airport not in nearby:
        nearby.append(current_airport)
    
    for airport in nearby:
        if airport["ident"] == current_airport["ident"] and random.random() < police_chance:
            return True
    return False

# ====================== GameSession Class (بهبود یافته) ======================

class GameSession:
    def __init__(self, session_data):
        self.session_id = session_data['session_id']
        self.player_id = session_data['player_id']
        self.current = get_airport_details(session_data['current_airport_ident'])
        self.safe_airport = get_airport_details(session_data['safe_airport_ident'])
        self.money = session_data['money']
        self.co2 = session_data['co2']
        self.round_no = session_data.get('round_no', 1)
        self.police_chance = session_data.get('police_chance', Config.POLICE_CATCH_START)
        self.flight_availability = session_data.get('flight_availability', 0.1)
        self.total_distance = session_data.get('final_distance_traveled', 0) or 0

    def get_full_state(self):
        distance_to_safe = get_distance(
            self.current['latitude_deg'], self.current['longitude_deg'],
            self.safe_airport['latitude_deg'], self.safe_airport['longitude_deg']
        )
        
        return {
            "session_id": self.session_id,
            "round": self.round_no,
            "money": self.money,
            "co2": self.co2,
            "police_chance_percent": round(self.police_chance * 100, 1),
            "flight_availability_percent": round(self.flight_availability * 100, 1),
            "current_airport": self.current,
            "safe_airport": self.safe_airport,
            "distance_to_safe_km": int(distance_to_safe),
            "total_distance_traveled": self.total_distance
        }

    def process_move(self, selected_ident):
        selected = get_airport_details(selected_ident)
        if not selected:
            return None, "Airport not found"

        money_cost, co2_cost, flight_distance = calculate_flight_cost(self.current, selected)

        self.money -= money_cost
        self.co2 -= co2_cost
        self.total_distance += flight_distance
        
        old_current = self.current
        self.current = selected
        self.round_no += 1

        # Update flight availability (better if closer)
        old_dist = get_distance(
            old_current['latitude_deg'], old_current['longitude_deg'],
            self.safe_airport['latitude_deg'], self.safe_airport['longitude_deg']
        )
        new_dist = get_distance(
            self.current['latitude_deg'], self.current['longitude_deg'],
            self.safe_airport['latitude_deg'], self.safe_airport['longitude_deg']
        )

        if new_dist < old_dist:
            improvement = (old_dist - new_dist) / old_dist
            self.flight_availability = min(Config.FLIGHT_AVAILABILITY_MAX, 
                                         self.flight_availability + improvement * 0.45)

        # Increase police chance
        self.police_chance = min(Config.POLICE_CATCH_MAX, 
                               self.police_chance + Config.POLICE_CATCH_INCREMENT)

        return selected, None