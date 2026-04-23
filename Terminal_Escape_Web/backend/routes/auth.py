# backend/routes/auth.py
from flask import Blueprint, request, jsonify
from services.player_service import get_or_create_player

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    player_name = data.get('player_name', '').strip()
    
    if not player_name or len(player_name) < 2:
        return jsonify({"error": "Player name must be at least 2 characters"}), 400
    
    player = get_or_create_player(player_name)
    
    return jsonify({
        "success": True,
        "player": player
    })