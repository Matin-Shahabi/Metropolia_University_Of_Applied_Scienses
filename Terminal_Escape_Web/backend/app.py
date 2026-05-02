# backend/app.py
from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from services.db import init_db

def create_app():
    app = Flask(__name__, 
                static_folder='../frontend',  
                template_folder='../frontend')
    
    app.config.from_object(Config)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize Database
    init_db()

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.game import game_bp
    from routes.player import player_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(game_bp, url_prefix='/api/game')
    app.register_blueprint(player_bp, url_prefix='/api/player')

    # Serve frontend files
    @app.route('/')
    def home():
        return send_from_directory('../frontend', 'index.html')

    @app.route('/<path:filename>')
    def serve_static(filename):
        return send_from_directory('../frontend', filename)

    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Terminal Escape Web Server Started!")
    print("Open: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)