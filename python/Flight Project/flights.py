from db import get_large_airports  # DB helper to fetch main airports
from utils import debug_print, get_distance  # Utility functions
from constants import MAX_FLIGHT_OPTIONS, COST_PER_KM, CO2_PER_KM  # Game constants
import random

# COUNTRY_NAMES is set externally by game.py for readable output
COUNTRY_NAMES = None  # To be set by game.py

def get_closer_airports(current, airports, safe_airport):
    """
    Filters airports to those that are closer to the safe airport than the player's current location.
    Args:
        current (dict): Current airport object
        airports (list): List of airport objects
        safe_airport (dict): Safe airport object
    Returns:
        list: Airports closer to the safe airport than current
    """
    current_distance = get_distance(current["latitude_deg"], current["longitude_deg"],
                                 safe_airport["latitude_deg"], safe_airport["longitude_deg"])
    # Only include airports that are not the current one and are closer to the safe airport
    closer_airports = [a for a in airports if a["ident"] != current["ident"] and
                       get_distance(a["latitude_deg"], a["longitude_deg"],
                                 safe_airport["latitude_deg"], safe_airport["longitude_deg"]) < current_distance]
    random.shuffle(closer_airports)  # Shuffle for randomness
    return closer_airports

def get_available_flights(current, safe_airport, destination_availability, round_no=1):
    """
    Generates a list of flight options for the player:
    - May include the safe airport based on probability.
    - Prioritizes airports that move the player closer to the safe airport.
    - Fills remaining slots with random airports.
    Args:
        current (dict): Current airport object
        safe_airport (dict): Safe airport object
        destination_availability (float): Probability of safe airport appearing
        round_no (int): Current round number
    Returns:
        list: Selected airport options
    """
    airports = get_large_airports()
    options = []
    roll = random.random()
    debug_print(f"Safe airport appearance chance: {round(destination_availability*100,2)}%")
    debug_print(f"Safe airport roll: {round(roll,4)}")
    debug_print(f"Current round: {round_no}")
    # Add safe airport to options if roll succeeds AND round >= 3
    if roll < destination_availability and round_no < 3:
        debug_print(f"Safe airport NOT added to options because it is early: round {round_no}.")
    if roll < destination_availability and round_no >= 3:
        options.append(safe_airport)
        debug_print("Safe airport ADDED to options.")
    # Add airports that are closer to the safe airport
    closer_airports = get_closer_airports(current, airports, safe_airport)
    # print closer airports for debugging if safe airport is in closer_airports
    if safe_airport in closer_airports:
        debug_print("Safe airport is in the list of closer airports.")
        # pop it out if its less than round 3
        if round_no < 3:
            closer_airports.remove(safe_airport)
            debug_print(f"Safe airport REMOVED from closer airports because it is early: round {round_no}.")
    
    debug_print
    debug_print(f"Found {len(closer_airports)} closer airports to safe airport.")
    for a in closer_airports:
        if a not in options:
            options.append(a)
        if len(options) >= MAX_FLIGHT_OPTIONS:
            break
    # Fill remaining slots with random airports
    if len(options) < MAX_FLIGHT_OPTIONS:
        # If round < 3, exclude safe airport from random fill
        if round_no < 3:
            remaining = [a for a in airports if a not in options and
                         a["ident"] != current["ident"] and
                         a["ident"] != safe_airport["ident"]]
        else:
            remaining = [a for a in airports if a not in options and
                         a["ident"] != current["ident"]]
        random.shuffle(remaining)
        options.extend(remaining[:MAX_FLIGHT_OPTIONS - len(options)])
    random.shuffle(options)  # Shuffle for unpredictability
    return options[:MAX_FLIGHT_OPTIONS]

def show_flight_options(current, safe_airport, destination_availability, round_no=1):
    """
    Displays available flight options to the player, including:
    - Airport name and country
    - Cost and CO2 for each flight
    - Distance to safe airport for each option
    Args:
        current (dict): Current airport object
        safe_airport (dict): Safe airport object
        destination_availability (float): Probability of safe airport appearing
        round_no (int): Current round number
    Returns:
        list: Flight info tuples (airport, cost, co2_cost, dist_to_safe_option)
    """
    flights = get_available_flights(current, safe_airport, destination_availability, round_no)
    flights_info = []
    print("\nAvailable flights:")
    for i, airport in enumerate(flights):
        # Calculate flight distance, cost, and CO2
        distance_km = int(get_distance(current['latitude_deg'], current['longitude_deg'],
                                    airport['latitude_deg'], airport['longitude_deg']))
        cost = int(distance_km * COST_PER_KM)
        co2_cost = int(distance_km * CO2_PER_KM)
        # Calculate distance from this airport to the safe airport
        dist_to_safe_option = int(get_distance(airport['latitude_deg'], airport['longitude_deg'],
                                            safe_airport['latitude_deg'], safe_airport['longitude_deg']))
        flights_info.append((airport, cost, co2_cost, dist_to_safe_option))
        country_name = COUNTRY_NAMES.get(airport['iso_country'], airport['iso_country'])
        #print(f"{i+1}. {airport['name']} ({country_name}) | Cost: {cost} | CO2: {co2_cost}")
        """
        print("-" * 80)
        print(f"{'No':<3} {'Airport':<25} {'Country':<20} {'Cost':<10} {'CO2':<10}")
        print("-" * 80)

        print(f"{i + 1:<3} {airport['name']:<25} {country_name:<20} {cost:<10} {co2_cost:<10}")
        """

       # print(f"{str(i + 1):3s} {airport['name']:15s} {country_name:15s} |cost: {str(cost):15} | CO2: {str(co2_cost):15s}")
        print(f"{i + 1:<3} {airport['name']:<40} {country_name:<15} | cost: {cost:<6} | CO2: {co2_cost:<6}")

        # Debug: print distance from this option to the safe airport
        debug_print(f"Option {i+1}: Distance to safe airport = {dist_to_safe_option} km")
    return flights_info

def player_choice(flights_info):
    """
    Handles player input for selecting a flight option.
    - Prompts for flight number or quit.
    - Validates input and returns selected flight info or None if quitting.
    Args:
        flights_info (list): List of flight info tuples
    Returns:
        tuple or None: Selected flight info or None if quitting
    """
    choice = input("Choose flight number (or Q to quit): ").strip()
    if choice.lower() == "q":
        return None  # Player chose to quit
    if not choice.isdigit() or not (1 <= int(choice) <= len(flights_info)):
        print("Invalid choice.")
        return player_choice(flights_info)  # Retry input
    return flights_info[int(choice)-1]
