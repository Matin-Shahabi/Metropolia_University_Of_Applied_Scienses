# backend/routes/game.py
from flask import Blueprint, request, jsonify
from services.player_service import create_game_session, save_game_state, load_unfinished_game, finish_game_session
from services.db import get_cursor
from models.game_logic import GameSession, get_available_flights, get_random_airport, police_turn
from config import Config
import random

game_bp = Blueprint('game', __name__)

@game_bp.route('/new', methods=['POST'])
def new_game():
    data = request.get_json()
    player_id = data.get('player_id')
    
    if not player_id:
        return jsonify({"error": "player_id is required"}), 400

    current = get_random_airport()
    safe_airport = get_random_airport(exclude_country=current["iso_country"])
    
    flight_availability = random.uniform(0.05, 0.15)
    
    session_id = create_game_session(
        player_id=player_id,
        start_airport=current['ident'],
        safe_airport=safe_airport['ident'],
        money=Config.START_MONEY,
        co2=Config.START_CO2,
        police_chance=Config.POLICE_CATCH_START,
        flight_availability=flight_availability
    )
    
    game = GameSession({
        'session_id': session_id,
        'player_id': player_id,
        'current_airport_ident': current['ident'],
        'safe_airport_ident': safe_airport['ident'],
        'money': Config.START_MONEY,
        'co2': Config.START_CO2,
        'round_no': 1,
        'police_chance': Config.POLICE_CATCH_START,
        'flight_availability': flight_availability
    })
    
    flights = get_available_flights(game.current, game.safe_airport, game.flight_availability, 1)
    
    return jsonify({
        "success": True,
        "session_id": session_id,
        "game_state": game.get_full_state(),
        "available_flights": [{"ident": f["ident"], "name": f["name"]} for f in flights]
    })


@game_bp.route('/continue', methods=['POST'])
def continue_game():
    data = request.get_json()
    player_id = data.get('player_id')
    
    if not player_id:
        return jsonify({"error": "player_id is required"}), 400
    
    session_data = load_unfinished_game(player_id)
    if not session_data:
        return jsonify({"error": "No unfinished game found for this player"}), 404
    
    game = GameSession(session_data)
    flights = get_available_flights(game.current, game.safe_airport, game.flight_availability, game.round_no)
    
    return jsonify({
        "success": True,
        "session_id": game.session_id,
        "game_state": game.get_full_state(),
        "available_flights": [{"ident": f["ident"], "name": f["name"]} for f in flights]
    })


@game_bp.route('/move', methods=['POST'])
def make_move():
    data = request.get_json()
    session_id = data.get('session_id')
    selected_ident = data.get('selected_ident')
    
    if not session_id or not selected_ident:
        return jsonify({"error": "session_id and selected_ident are required"}), 400
    
    # Load session
    cursor = get_cursor()  # از services.db
    cursor.execute("SELECT * FROM player_game_sessions WHERE session_id = %s AND status = 'in_progress'", (session_id,))
    session_data = cursor.fetchone()
    
    if not session_data:
        return jsonify({"error": "Session not found or already finished"}), 400
    
    game = GameSession(session_data)
    selected, error = game.process_move(selected_ident)
    
    if error:
        return jsonify({"error": error}), 400
    
    # Save state
    save_game_state(
        session_id=game.session_id,
        current_airport=game.current['ident'],
        money=game.money,
        co2=game.co2,
        round_no=game.round_no,
        police_chance=game.police_chance,
        flight_availability=game.flight_availability
    )
    
    # Check win
    if game.current['ident'] == game.safe_airport['ident']:
        final_co2 = Config.START_CO2 - game.co2
        final_money = Config.START_MONEY - game.money
        finish_game_session(game.session_id, 'won', final_co2, final_money, game.round_no, game.total_distance)
        return jsonify({
            "success": True,
            "game_over": True,
            "result": "won",
            "game_state": game.get_full_state()
        })
    
    # Check resource loss
    if game.money <= 0 or game.co2 <= 0:
        final_co2 = Config.START_CO2 - game.co2
        final_money = Config.START_MONEY - game.money
        finish_game_session(game.session_id, 'lost_resources', final_co2, final_money, game.round_no, game.total_distance)
        return jsonify({
            "success": True,
            "game_over": True,
            "result": "lost_resources",
            "game_state": game.get_full_state()
        })
    
    # Police turn
    if police_turn(game.current, game.police_chance):
        final_co2 = Config.START_CO2 - game.co2
        final_money = Config.START_MONEY - game.money
        finish_game_session(game.session_id, 'lost_police', final_co2, final_money, game.round_no, game.total_distance)
        return jsonify({
            "success": True,
            "game_over": True,
            "result": "caught",
            "game_state": game.get_full_state()
        })
    
    # Continue game
    new_flights = get_available_flights(game.current, game.safe_airport, game.flight_availability, game.round_no)
    
    return jsonify({
        "success": True,
        "game_over": False,
        "game_state": game.get_full_state(),
        "available_flights": [{"ident": f["ident"], "name": f["name"]} for f in new_flights]
    })