# backend/routes/player.py
from flask import Blueprint, request, jsonify
from services.player_service import (
    get_player_personal_bests,
    get_global_leaderboard_co2,
    get_global_leaderboard_speed,
)

player_bp = Blueprint("player", __name__)


@player_bp.route("/stats", methods=["GET"])
def get_stats():
    player_id = request.args.get("player_id")
    if not player_id:
        return jsonify({"error": "player_id is required"}), 400

    bests = get_player_personal_bests(int(player_id))
    return jsonify({"success": True, "personal_bests": bests or {}})


@player_bp.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    co2 = get_global_leaderboard_co2(limit=10)
    speed = get_global_leaderboard_speed(limit=10)

    return jsonify(
        {"success": True, "co2_leaderboard": co2, "speed_leaderboard": speed}
    )
