# backend/services/player_service.py
from services.db import get_cursor, commit
import random

def get_or_create_player(player_name):
    cursor = get_cursor()
    cursor.execute("SELECT player_id, player_name FROM players WHERE player_name = %s", (player_name,))
    player = cursor.fetchone()
    
    if player:
        return player
    
    cursor.execute("INSERT INTO players (player_name) VALUES (%s)", (player_name,))
    commit()
    player_id = cursor.lastrowid
    return {"player_id": player_id, "player_name": player_name}


def create_game_session(player_id, start_airport, safe_airport, money, co2, police_chance, flight_availability):
    cursor = get_cursor()
    cursor.execute("""
        INSERT INTO player_game_sessions 
        (player_id, start_airport_ident, safe_airport_ident, current_airport_ident, 
         money, co2, round_no, police_chance, flight_availability)
        VALUES (%s, %s, %s, %s, %s, %s, 1, %s, %s)
    """, (player_id, start_airport, safe_airport, start_airport, money, co2, police_chance, flight_availability))
    commit()
    return cursor.lastrowid


def save_game_state(session_id, current_airport, money, co2, round_no, police_chance, flight_availability):
    cursor = get_cursor()
    cursor.execute("""
        UPDATE player_game_sessions 
        SET current_airport_ident = %s, money = %s, co2 = %s, 
            round_no = %s, police_chance = %s, flight_availability = %s,
            last_saved_at = NOW()
        WHERE session_id = %s
    """, (current_airport, money, co2, round_no, police_chance, flight_availability, session_id))
    commit()


def load_unfinished_game(player_id):
    cursor = get_cursor()
    cursor.execute("""
        SELECT * FROM player_game_sessions 
        WHERE player_id = %s AND status = 'in_progress' 
        ORDER BY last_saved_at DESC LIMIT 1
    """, (player_id,))
    return cursor.fetchone()


def finish_game_session(session_id, status, final_co2_used, final_money_used, final_rounds, final_distance=0):
    cursor = get_cursor()
    cursor.execute("""
        UPDATE player_game_sessions 
        SET status = %s, finished_at = NOW(), final_co2_used = %s,
            final_money_used = %s, final_rounds = %s, final_distance_traveled = %s
        WHERE session_id = %s
    """, (status, final_co2_used, final_money_used, final_rounds, final_distance, session_id))
    commit()

    # Update player stats
    cursor.execute("SELECT player_id FROM player_game_sessions WHERE session_id = %s", (session_id,))
    result = cursor.fetchone()
    if result:
        player_id = result['player_id']
        won = 1 if status == 'won' else 0
        lost = 1 if status in ['lost_resources', 'lost_police'] else 0
        
        cursor.execute("""
            UPDATE players 
            SET total_games = total_games + 1,
                games_won = games_won + %s,
                games_lost = games_lost + %s,
                last_played = NOW()
            WHERE player_id = %s
        """, (won, lost, player_id))
        commit()


def get_player_personal_bests(player_id):
    cursor = get_cursor()
    cursor.execute("""
        SELECT 
            MIN(final_co2_used) AS best_co2,
            MIN(final_money_used) AS best_money,
            MIN(final_rounds) AS fastest_rounds,
            COUNT(*) AS total_won_games
        FROM player_game_sessions 
        WHERE player_id = %s AND status = 'won'
    """, (player_id,))
    return cursor.fetchone()


def get_global_leaderboard_co2(limit=10):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM global_leaderboard_co2 LIMIT %s", (limit,))
    return cursor.fetchall()


def get_global_leaderboard_speed(limit=10):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM global_leaderboard_speed LIMIT %s", (limit,))
    return cursor.fetchall()