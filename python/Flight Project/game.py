

import random

# ===============================
# Mankind Vs AI: The Terminal Escape
# Main Game Logic
# ===============================
# This module contains the main game loop and core helpers for TerminalEscape.
# It orchestrates player turns, resource management, win/loss conditions, and
# delegates police and flight logic to their respective modules.

# --- Imports ---
from db import country_iso_to_name, get_random_airport, get_airport_details  # DB helpers
from constants import START_MONEY, START_CO2, POLICE_CATCH_START, POLICE_CATCH_INCREMENT, POLICE_CATCH_MAX, FLIGHT_AVAILABILITY_MAX  # Game constants
from utils import debug_print, get_distance  # Utility functions
from police import search_airports, police_turn  # Police logic
from flights import get_closer_airports, get_available_flights, show_flight_options, player_choice  # Flight logic
# Player database operations for profiles, save/resume, and statistics
from player_db import (
    get_or_create_player,
    create_game_session,
    save_game_state,
    load_unfinished_game,
    finish_game_session,
    abandon_game_session,
    get_player_personal_bests,
    get_global_leaderboard_co2,
    get_global_leaderboard_speed,
    get_player_history
)


# --- Global country mapping for readable output ---
COUNTRY_NAMES = country_iso_to_name()  # {iso_code: country_name}

# Share country mapping with police and flights modules for consistent output
# This allows those modules to print country names instead of ISO codes when showing airports.
import police, flights
police.COUNTRY_NAMES = COUNTRY_NAMES
flights.COUNTRY_NAMES = COUNTRY_NAMES

# ============================================================
# FLIGHT & SAFE CHANCE HELPERS
# ============================================================

def execute_player_choice(money, co2, selected, cost, co2_cost):
    """
    Deducts the cost and CO2 for a flight and updates the player's current airport.
    Args:
        money (int): Current player money
        co2 (int): Current player CO2 credits
        selected (dict): Selected airport object
        cost (int): Money cost for the flight
        co2_cost (int): CO2 cost for the flight
    Returns:
        tuple: (updated money, updated co2, new current airport object)
    """
    money -= cost
    co2 -= co2_cost
    current = get_airport_details(selected["ident"])
    debug_print(f"Money after flight: {money}")
    debug_print(f"CO2 after flight: {co2}")
    return money, co2, current


def update_flight_availability(old_distance, new_distance, flight_availability):
    """
    Updates the probability of the safe airport appearing in options based on player progress.
    - If the player moves closer to the safe airport, the chance increases proportionally.
    - If the player moves farther, a small penalty is applied.
    Args:
        old_distance (float): Previous distance to safe airport
        new_distance (float): New distance to safe airport
        flight_availability (float): Current chance value
    Returns:
        float: Updated safe airport chance
    """
    if new_distance < old_distance:
        improvement_ratio = (old_distance - new_distance) / old_distance
        increment = improvement_ratio * 0.5
        flight_availability = min(FLIGHT_AVAILABILITY_MAX, flight_availability + increment)
        debug_print(f"Moved CLOSER by {round(improvement_ratio*100,2)}%")
        debug_print(f"Safe airport chance increased by {round(increment*100,2)}%")
    else: # If player moved farther, apply a small penalty to the safe airport chance - ?
        flight_availability = max(0, flight_availability - 0.01)
        debug_print("Moved FARTHER — chance -1% penalty.")
    debug_print(f"New safe airport chance: {round(flight_availability*100,2)}%")
    return flight_availability


def display_status(round_no, money, co2, current, safe_airport):
    """
    Prints the current game status for the player, including:
    - Round number
    - Money and CO2 credits
    - Current and safe airport (with country)
    - Distance to safe airport
    Returns:
        float: Distance to safe airport (km)
    """
    print("\n-------------------------")
    print(f"Round: {round_no}")
    print(f"Money: {money}")
    print(f"CO2 credits: {co2}")
    current_country = COUNTRY_NAMES.get(current['iso_country'], current['iso_country'])
    safe_country = COUNTRY_NAMES.get(safe_airport['iso_country'], safe_airport['iso_country'])
    print(f"Current Airport: {current['name']} ({current_country})")
    print(f"Safe airport: {safe_airport['name']} ({safe_country})")
    distance_to_safe = get_distance(current['latitude_deg'], current['longitude_deg'],
                                 safe_airport['latitude_deg'], safe_airport['longitude_deg'])
    print(f"Distance to safe airport: {int(distance_to_safe)} km")
    return distance_to_safe

# ============================================================
# PLAYER MENU & STATISTICS
# ============================================================

def show_player_menu(player):
    """Display player profile menu with options to continue, start new, view stats, or quit."""
    player_id = player['player_id']
    player_name = player['player_name']
    
    print("\n" + "="*60)
    print(f"🎮 Welcome, {player_name}!")
    print("="*60)
    
    # Check for unfinished game
    unfinished = load_unfinished_game(player_id)
    
    if unfinished:
        print(f"\n📂 You have an unfinished game:")
        print(f"   Started: {unfinished['started_at']}")
        print(f"   Round: {unfinished['round_no']}")
        print(f"   Money: {unfinished['money']}, CO2: {unfinished['co2']}")
        current_country = COUNTRY_NAMES.get(unfinished['current_airport_ident'][:2], unfinished['current_airport_ident'])
        safe_country = COUNTRY_NAMES.get(unfinished['safe_airport_ident'][:2], unfinished['safe_airport_ident'])
        print(f"   Current: {unfinished['current_airport_ident']}")
        print(f"   Target: {unfinished['safe_airport_ident']}")
        
        while True:
            choice = input("\n[S]tory, [C]ontinue game, [N]ew game, [M]yScore, [L]eaderboard, [Q]uit: ").strip().upper()

            if choice == 'C':
                return 'continue', unfinished
            elif choice == 'S':
                # Part 1: The Setup
                print("\n" + "="*60)
                print("📖 MANKIND VS AI: THE TERMINAL ESCAPE")
                print("="*60)
                print("\nSet on a dark, rain-soaked night, you are humanity's final")
                print("hope. The enemy, an AI-powered global police force. It hunts")
                print("you relentlessly.")
                print("\nAs your engine roars to life on the misty runway, alarms blare")
                print("in the AI command center. Endless data streams flash across")
                print("their systems as they calculate the location of one fugitive")
                print("human, you. Hidden in your suitcase is the world's last chance")
                print("for survival: a next-generation chip meant for the final manned")
                print("crew preparing to flee from an airport on the other side of the")
                print("world. The AI has limitless speed, intelligence, and resources.")
                print("You have only your wits, your knowledge of geography, and a")
                print("dwindling stash of cash.")
                input("\nPress Enter to continue...")
                
                # Part 2: The Stakes
                print("\nYou dream that one day, humanity will reclaim the AI-infested")
                print("Earth. But that hope comes with responsibility. You can't simply")
                print("blaze through airports or take reckless flights. Every move,")
                print("every mile flown, leaves a CO₂ trace you'd rather not worsen.")
                print("Yet the AI police are learning fast, adapting with every")
                print("decision you make, for real.")
                print("\nSuddenly, the departure hall's screen flickers to life. The AI")
                print("is watching. You have a decision to make.")
                input("\nPress Enter to continue...")
                
                # Part 3: The Challenge
                print("\nChoose carefully. Move too aggressively, and you'll drain your")
                print("funds and choke the planet you're trying to save. Move too")
                print("slowly, and the AI will outthink and overtake you. Every trip")
                print("wastes fuel, costs money, and raises your risk of capture.")
                print("\nEvery decision counts. Mankind's survival depends on your")
                print("speed, strategy, and resource management. Only those who master")
                print("the balance, risk, timing, precision and good old geography")
                print("might live to see the hidden hangar doors open and the final")
                print("escape plane waiting beyond them.")
                print("\nSet against wind, rain, roaring engines, and neon-lit runways,")
                print("Mankind Vs AI: The Terminal Escape is more than a game of")
                print("chance—it's a test of survival under pressure. One wrong move,")
                print("and all of humanity is lost.")
                print("\n" + "="*60)
                input("\nPress Enter to return to the menu...")
                return show_player_menu(player)  # Show menu again
            elif choice == 'N':
                # Ask if they want to abandon the old game
                abandon = input("⚠️  Abandon unfinished game? (y/n): ").strip().lower()
                if abandon == 'y':
                    abandon_game_session(unfinished['session_id'])
                    print("✓ Previous game abandoned.")
                else:
                    return show_player_menu(player)  # Show menu again
                return 'new', None
            elif choice == 'M':
                show_player_stats(player_id, player_name)
                return show_player_menu(player)  # Show menu again
            elif choice == 'L':
                show_leaderboards()
                return show_player_menu(player)  # Show menu again
            elif choice == 'Q':
                return 'quit', None
            else:
                print("❌ Invalid choice. Please select from the options below.")
    else:
        print(f"\n✨ No unfinished games found.")
        
        while True:
            choice = input("\n[S]tory, [N]ew game, [M]yScore, [L]eaderboard, [Q]uit: ").strip().upper()

            if choice == 'N':
                return 'new', None
            elif choice == 'S':
                # Part 1: The Setup
                print("\n" + "="*60)
                print("📖 MANKIND VS AI: THE TERMINAL ESCAPE")
                print("="*60)
                print("\nSet on a dark, rain-soaked night, you are humanity's final")
                print("hope. The enemy, an AI-powered global police force. It hunts")
                print("you relentlessly.")
                print("\nAs your engine roars to life on the misty runway, alarms blare")
                print("in the AI command center. Endless data streams flash across")
                print("their systems as they calculate the location of one fugitive")
                print("human, you. Hidden in your suitcase is the world's last chance")
                print("for survival: a next-generation chip meant for the final manned")
                print("crew preparing to flee from an airport on the other side of the")
                print("world. The AI has limitless speed, intelligence, and resources.")
                print("You have only your wits, your knowledge of geography, and a")
                print("dwindling stash of cash.")
                input("\nPress Enter to continue...")
                
                # Part 2: The Stakes
                print("\nYou dream that one day, humanity will reclaim the AI-infested")
                print("Earth. But that hope comes with responsibility. You can't simply")
                print("blaze through airports or take reckless flights. Every move,")
                print("every mile flown, leaves a CO₂ trace you'd rather not worsen.")
                print("Yet the AI police are learning fast, adapting with every")
                print("decision you make, for real.")
                print("\nSuddenly, the departure hall's screen flickers to life. The AI")
                print("is watching. You have a decision to make.")
                input("\nPress Enter to continue...")
                
                # Part 3: The Challenge
                print("\nChoose carefully. Move too aggressively, and you'll drain your")
                print("funds and choke the planet you're trying to save. Move too")
                print("slowly, and the AI will outthink and overtake you. Every trip")
                print("wastes fuel, costs money, and raises your risk of capture.")
                print("\nEvery decision counts. Mankind's survival depends on your")
                print("speed, strategy, and resource management. Only those who master")
                print("the balance, risk, timing, precision and good old geography")
                print("might live to see the hidden hangar doors open and the final")
                print("escape plane waiting beyond them.")
                print("\nSet against wind, rain, roaring engines, and neon-lit runways,")
                print("Mankind Vs AI: The Terminal Escape is more than a game of")
                print("chance—it's a test of survival under pressure. One wrong move,")
                print("and all of humanity is lost.")
                print("\n" + "="*60)
                input("\nPress Enter to return to the menu...")
                return show_player_menu(player)  # Show menu again
            elif choice == 'M':
                show_player_stats(player_id, player_name)
                return show_player_menu(player)
            elif choice == 'L':
                show_leaderboards()
                return show_player_menu(player)
            elif choice == 'Q':
                return 'quit', None
            else:
                print("❌ Invalid choice. Please select from the options below.")


def show_player_stats(player_id, player_name):
    """Display player's game history and personal bests."""
    print("\n" + "="*60)
    print(f"📊 STATISTICS FOR {player_name}")
    print("="*60)
    
    # Personal bests
    bests = get_player_personal_bests(player_id)
    if bests and bests['total_won_games'] > 0:
        print(f"\n🏆 Personal Bests:")
        print(f"   Best CO2 Efficiency: {bests['best_co2']} CO2")
        if bests['best_money']:
            print(f"   Best Money Efficiency: {bests['best_money']} Money")
        if bests['fastest_rounds']:
            print(f"   Fastest Win: {bests['fastest_rounds']} rounds")
        print(f"   Total Wins: {bests['total_won_games']}")
    else:
        print("\n   No wins yet. Keep trying! 💪")
    
    # Recent games
    history = get_player_history(player_id, limit=5)
    if history:
        print(f"\n📜 Recent Games:")
        for i, game in enumerate(history, 1):
            status_display = {
                'won': ('✅', 'WON'),
                'lost_resources': ('💀', 'LOST - Out of Resources'),
                'lost_police': ('👮', 'CAUGHT BY POLICE'),
                'abandoned': ('❌', 'ABANDONED'),
                'in_progress': ('⏸️', 'IN PROGRESS')
            }
            
            emoji, status_text = status_display.get(game['status'], ('❓', game['status'].upper()))
            
            print(f"\n   {i}. {emoji} {status_text}")
            print(f"      Started: {game['started_at']}")
            if game['status'] != 'in_progress':
                rounds_info = f"Rounds: {game['final_rounds']}" if game['final_rounds'] else f"Round: {game['last_round']}"
                co2_info = f"CO2 used: {game['final_co2_used']}" if game['final_co2_used'] else ""
                print(f"      {rounds_info}, {co2_info}")
    
    input("\nPress Enter to continue...")


def show_leaderboards():
    """Display global leaderboards."""
    print("\n" + "="*60)
    print("🌍 GLOBAL LEADERBOARDS")
    print("="*60)
    
    # CO2 Efficiency Leaderboard
    print("\n🌱 Top 10 - CO2 Efficiency:")
    co2_leaders = get_global_leaderboard_co2(limit=10)
    if co2_leaders:
        for i, entry in enumerate(co2_leaders, 1):
            print(f"   {i:2d}. {entry['player_name']:20s} - {entry['co2_used']:5d} CO2 ({entry['rounds']} rounds)")
    else:
        print("   No data yet. Be the first! 🚀")
    
    # Speed Leaderboard
    print("\n⚡ Top 10 - Fastest Wins:")
    speed_leaders = get_global_leaderboard_speed(limit=10)
    if speed_leaders:
        for i, entry in enumerate(speed_leaders, 1):
            print(f"   {i:2d}. {entry['player_name']:20s} - {entry['rounds']:3d} rounds (CO2: {entry['co2_used']})")
    else:
        print("   No data yet. Be the first! 🚀")
    
    input("\nPress Enter to continue...")


# ============================================================
# MAIN GAME LOOP
# ============================================================

def start_game():
    """
    Main game controller with full database integration.
    Handles:
    1. Player login and profile management
    2. Save/resume functionality
    3. Game loop with auto-save
    4. Statistics tracking
    5. Win/loss recording
    """
    print("="*60)
    print("🎮 MANKIND Vs AI: THE TERMINAL ESCAPE")
    print("The Ultimate Escape Game")

    print("="*60)
    
    # Step 1: Get or create player profile
    player_name = input("\n👤 Enter your player name: ").strip()
    if not player_name:
        player_name = "Anonymous"
    
    player = get_or_create_player(player_name)
    player_id = player['player_id']
    
    # Step 2: Show menu and handle player choice
    action, game_data = show_player_menu(player)
    
    if action == 'quit':
        print("\n👋 Thanks for playing! See you next time!")
        return
    
    # Step 3: Initialize or resume game
    session_id = None
    
    if action == 'continue':
        # Resume from saved state
        session_id = game_data['session_id']
        current = get_airport_details(game_data['current_airport_ident'])
        safe_airport = get_airport_details(game_data['safe_airport_ident'])
        money = game_data['money']
        co2 = game_data['co2']
        round_no = game_data['round_no'] - 1  # Will be incremented in loop
        police_chance = game_data['police_chance']
        flight_availability = game_data['flight_availability']
        
        print(f"\n🔄 Resuming game from round {game_data['round_no']}...")
        
    else:  # action == 'new'
        # Start new game
        current = get_random_airport()
        safe_airport = get_random_airport(exclude_country=current["iso_country"])
        money = START_MONEY
        co2 = START_CO2
        round_no = 0
        police_chance = POLICE_CATCH_START
        flight_availability = random.uniform(0.05, 0.15)
        
        # Create session in database
        session_id = create_game_session(
            player_id=player_id,
            start_airport=current['ident'],
            safe_airport=safe_airport['ident'],
            money=money,
            co2=co2,
            police_chance=police_chance,
            flight_availability=flight_availability
        )
        
        print(f"\n✨ New game started!")

    print("\n🎯 Your goal: Reach the SAFE AIRPORT before money, CO2, or police catches you!")
    
    # Track initial values for final statistics
    initial_money = money
    initial_co2 = co2
    total_distance = 0
    
    # Main game loop: runs until win, loss, or exit
    while True:
        round_no += 1  # Advance round counter
        
        # Show current status and get distance to safe airport
        old_distance = display_status(round_no, money, co2, current, safe_airport)

        # Generate and display available flight options for this turn

        flights_info = show_flight_options(current, safe_airport, flight_availability, round_no)

        # Handle player's flight selection (or exit)
        result = player_choice(flights_info)
        if result is None:
            print("\n⚠️  Game paused. Your progress has been saved.")
            # Save final state before exit
            save_game_state(session_id, current['ident'], money, co2, round_no, police_chance, flight_availability)
            break  # Player chose to exit
        
        # Unpack selected flight and its costs
        selected, cost, co2_cost, new_distance = result

        # Track distance traveled
        flight_distance = get_distance(current['latitude_deg'], current['longitude_deg'],
                                       selected['latitude_deg'], selected['longitude_deg'])
        total_distance += flight_distance

        # Deduct costs and update current airport
        money, co2, current = execute_player_choice(money, co2, selected, cost, co2_cost)
        
        # Adjust safe airport chance based on progress
        flight_availability = update_flight_availability(old_distance, new_distance, flight_availability)

        # Auto-save game state after each move
        save_game_state(session_id, current['ident'], money, co2, round_no, police_chance, flight_availability)
        debug_print(f"Game state auto-saved (session {session_id})")

        # Win condition: player reached the safe airport
        if current["ident"] == safe_airport["ident"]:
            print(f"\n🎉 You reached the SAFE AIRPORT: {safe_airport['name']}! You win!")
            
            # Calculate final statistics
            final_co2_used = initial_co2 - co2
            final_money_used = initial_money - money
            
            # Record win in database
            finish_game_session(
                session_id=session_id,
                status='won',
                final_co2_used=final_co2_used,
                final_money_used=final_money_used,
                final_rounds=round_no,
                final_distance=int(total_distance)
            )
            
            # Show statistics
            print(f"\n📊 Final Statistics:")
            print(f"   Rounds: {round_no}")
            print(f"   CO2 used: {final_co2_used}")
            print(f"   Money used: {final_money_used}")
            print(f"   Distance traveled: {int(total_distance)} km")
            
            # Show personal bests
            bests = get_player_personal_bests(player_id)
            if bests:
                print(f"\n🏆 Your Personal Bests:")
                if bests['best_co2'] == final_co2_used:
                    print(f"   🌟 NEW RECORD! Best CO2: {bests['best_co2']}")
                else:
                    print(f"   Best CO2: {bests['best_co2']} (You: {final_co2_used})")
                
                if bests['fastest_rounds'] == round_no:
                    print(f"   🌟 NEW RECORD! Fastest: {bests['fastest_rounds']} rounds")
                else:
                    print(f"   Fastest: {bests['fastest_rounds']} rounds (You: {round_no})")
            
            break
        
        # Loss condition: out of money or CO2
        if money <= 0 or co2 <= 0:
            print("\n💀 Game Over! You ran out of resources.")
            
            # Calculate final statistics
            final_co2_used = initial_co2 - co2
            final_money_used = initial_money - money
            
            # Record loss in database
            finish_game_session(
                session_id=session_id,
                status='lost_resources',
                final_co2_used=final_co2_used,
                final_money_used=final_money_used,
                final_rounds=round_no,
                final_distance=int(total_distance)
            )
            
            print(f"\n📊 You survived {round_no} rounds before running out of resources.")
            break
        
        # Police turn: check if player is caught
        if police_turn(current, police_chance):
            # Calculate final statistics
            final_co2_used = initial_co2 - co2
            final_money_used = initial_money - money
            
            # Record police loss in database
            finish_game_session(
                session_id=session_id,
                status='lost_police',
                final_co2_used=final_co2_used,
                final_money_used=final_money_used,
                final_rounds=round_no,
                final_distance=int(total_distance)
            )
            
            print(f"\n📊 You were caught after {round_no} rounds.")
            break
        
        # Increase police catch probability for next round
        police_chance = min(POLICE_CATCH_MAX, police_chance + POLICE_CATCH_INCREMENT)
        debug_print(f"Police chance increased to {round(police_chance*100,2)}%")
    
    # Show leaderboard after game ends (if not just paused)
    if result is not None:  # Game actually ended, not paused
        print("\n" + "="*60)
        view_leaderboard = input("📊 View global leaderboards? (y/n): ").strip().lower()
        if view_leaderboard == 'y':
            show_leaderboards()
        
        # Ask if player wants to play again
        print("\n" + "="*60)
        play_again = input("🎮 Play another game? (y/n): ").strip().lower()
        if play_again == 'y':
            # Ask if they want to continue as same player or change
            print("\n" + "="*60)
            same_player = input(f"Continue as {player_name}? (y/n): ").strip().lower()
            if same_player == 'y':
                # Show menu for same player
                action, game_data = show_player_menu(player)
                if action != 'quit':
                    print("\n" + "="*60)
                    start_game()  # Start fresh game session
            else:
                print("\n" + "="*60)
                start_game()  # Recursively start with new player
            return
        else:
            # Player chose not to play again
            print(f"\n👋 {player_name}, Thanks for playing Terminal Escape!")
            print("\n" + "=" * 40)
            print("          GAME OVER")
            print(f"   Thanks for playing, {player_name}!")
            print("=" * 40)
            return
    
    # If game was paused (player pressed Q during game)
    print(f"\n👋 {player_name}, Thanks for playing Terminal Escape!")
    print("Your progress has been saved. See you next time!")