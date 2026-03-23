"""
player_db.py
============
Database operations for player profiles and game session management.
Handles player creation, game save/load, and statistics tracking.
"""

from db import db, cursor

SESSIONS_TABLE = "player_game_sessions"


# ============================================================
# PLAYER PROFILE OPERATIONS
# ============================================================

def get_or_create_player(player_name):
    """
    Get existing player or create a new one.
    Args:
        player_name (str): Player's name
    Returns:
        dict: Player info with player_id and player_name
    """
    # Try to find existing player
    cursor.execute("SELECT player_id, player_name FROM players WHERE player_name = %s", (player_name,))
    player = cursor.fetchone()
    
    if player:
        return player
    
    # Create new player
    cursor.execute("INSERT INTO players (player_name) VALUES (%s)", (player_name,))
    db.commit()
    player_id = cursor.lastrowid
    return {"player_id": player_id, "player_name": player_name}


def get_player_statistics(player_id):
    """
    Get comprehensive statistics for a player.
    Args:
        player_id (int): Player's ID
    Returns:
        dict: Player statistics including win rate, personal bests, etc.
    """
    cursor.execute("""
        SELECT * FROM player_statistics WHERE player_id = %s
    """, (player_id,))
    return cursor.fetchone()


def get_player_history(player_id, limit=10):
    """
    Get player's recent game history.
    Args:
        player_id (int): Player's ID
        limit (int): Number of recent games to fetch
    Returns:
        list: Recent game sessions
    """
    cursor.execute("""
        SELECT 
            session_id,
            status,
            started_at,
            finished_at,
            final_rounds,
            final_co2_used,
            final_money_used,
            round_no AS last_round
        FROM player_game_sessions 
        WHERE player_id = %s 
        ORDER BY started_at DESC 
        LIMIT %s
    """, (player_id, limit))
    return cursor.fetchall()


# ============================================================
# GAME SESSION OPERATIONS
# ============================================================

def create_game_session(player_id, start_airport, safe_airport, money, co2, police_chance, flight_availability):
    """
    Create a new game session.
    Args:
        player_id (int): Player's ID
        start_airport (str): Starting airport ident
        safe_airport (str): Safe airport ident
        money (int): Starting money
        co2 (int): Starting CO2
        police_chance (float): Initial police catch probability
        flight_availability (float): Initial safe airport appearance chance
    Returns:
        int: New session ID
    """
    cursor.execute("""
        INSERT INTO player_game_sessions 
        (player_id, start_airport_ident, safe_airport_ident, current_airport_ident, 
         money, co2, round_no, police_chance, flight_availability)
        VALUES (%s, %s, %s, %s, %s, %s, 1, %s, %s)
    """, (player_id, start_airport, safe_airport, start_airport, money, co2, police_chance, flight_availability))
    db.commit()
    return cursor.lastrowid


def save_game_state(session_id, current_airport, money, co2, round_no, police_chance, flight_availability):
    """
    Save current game state.
    Args:
        session_id (int): Game session ID
        current_airport (str): Current airport ident
        money (int): Current money
        co2 (int): Current CO2
        round_no (int): Current round number
        police_chance (float): Current police catch probability
        flight_availability (float): Current safe airport appearance chance
    """
    cursor.execute("""
        UPDATE player_game_sessions 
        SET current_airport_ident = %s,
            money = %s,
            co2 = %s,
            round_no = %s,
            police_chance = %s,
            flight_availability = %s
        WHERE session_id = %s
    """, (current_airport, money, co2, round_no, police_chance, flight_availability, session_id))
    db.commit()


def load_unfinished_game(player_id):
    """
    Load the most recent unfinished game for a player.
    Args:
        player_id (int): Player's ID
    Returns:
        dict or None: Game session data or None if no unfinished game
    """
    cursor.execute("""
        SELECT * FROM player_game_sessions 
        WHERE player_id = %s AND status = 'in_progress' 
        ORDER BY last_saved_at DESC 
        LIMIT 1
    """, (player_id,))
    return cursor.fetchone()


def finish_game_session(session_id, status, final_co2_used, final_money_used, final_rounds, final_distance=0):
    """
    Mark a game session as finished and record final statistics.
    Args:
        session_id (int): Game session ID
        status (str): Final status ('won', 'lost_resources', 'lost_police', 'abandoned')
        final_co2_used (int): Total CO2 used
        final_money_used (int): Total money used
        final_rounds (int): Total rounds played
        final_distance (int): Total distance traveled (optional)
    """
    cursor.execute("""
        UPDATE player_game_sessions 
        SET status = %s,
            finished_at = NOW(),
            final_co2_used = %s,
            final_money_used = %s,
            final_rounds = %s,
            final_distance_traveled = %s
        WHERE session_id = %s
    """, (status, final_co2_used, final_money_used, final_rounds, final_distance, session_id))
    db.commit()
    
    # Update player statistics
    cursor.execute("SELECT player_id FROM player_game_sessions WHERE session_id = %s", (session_id,))
    result = cursor.fetchone()
    if result:
        player_id = result['player_id']
        games_won_increment = 1 if status == 'won' else 0
        games_lost_increment = 1 if status in ['lost_resources', 'lost_police'] else 0
        
        cursor.execute("""
            UPDATE players 
            SET total_games = total_games + 1,
                games_won = games_won + %s,
                games_lost = games_lost + %s
            WHERE player_id = %s
        """, (games_won_increment, games_lost_increment, player_id))
        db.commit()


def abandon_game_session(session_id):
    """
    Mark a game session as abandoned.
    Args:
        session_id (int): Game session ID
    """
    cursor.execute("""
        UPDATE player_game_sessions 
        SET status = 'abandoned',
            finished_at = NOW()
        WHERE session_id = %s
    """, (session_id,))
    db.commit()


# ============================================================
# LEADERBOARD & STATISTICS QUERIES
# ============================================================

def get_global_leaderboard_co2(limit=10):
    """
    Get global leaderboard by CO2 efficiency.
    Args:
        limit (int): Number of top players to return
    Returns:
        list: Top players by CO2 efficiency
    """
    cursor.execute("""
        SELECT * FROM global_leaderboard_co2 LIMIT %s
    """, (limit,))
    return cursor.fetchall()


def get_global_leaderboard_speed(limit=10):
    """
    Get global leaderboard by speed (fewest rounds).
    Args:
        limit (int): Number of top players to return
    Returns:
        list: Top players by speed
    """
    cursor.execute("""
        SELECT * FROM global_leaderboard_speed LIMIT %s
    """, (limit,))
    return cursor.fetchall()


def get_player_personal_bests(player_id):
    """
    Get player's personal best records.
    Args:
        player_id (int): Player's ID
    Returns:
        dict: Personal best statistics
    """
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


def get_player_rank_co2(player_id):
    """
    Get player's rank in CO2 efficiency leaderboard.
    Args:
        player_id (int): Player's ID
    Returns:
        int or None: Player's rank (1-based) or None if no winning games
    """
    cursor.execute("""
        SELECT COUNT(*) + 1 AS rank
        FROM (
            SELECT player_id, MIN(final_co2_used) AS best_co2
            FROM player_game_sessions
            WHERE status = 'won' AND final_co2_used IS NOT NULL
            GROUP BY player_id
        ) AS rankings
        WHERE best_co2 < (
            SELECT MIN(final_co2_used)
            FROM player_game_sessions
            WHERE player_id = %s AND status = 'won'
        )
    """, (player_id,))
    result = cursor.fetchone()
    return result['rank'] if result else None
