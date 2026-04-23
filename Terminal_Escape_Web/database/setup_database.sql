-- ============================================================
-- TerminalEscape Database Schema
-- ============================================================
-- This schema supports:
-- - Player profiles
-- - Game session history and save/resume
-- - Personal best tracking
-- - Global leaderboards
-- ============================================================

-- Table: players
-- Stores player profile information
CREATE TABLE IF NOT EXISTS players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    total_games INT DEFAULT 0,
    games_won INT DEFAULT 0,
    games_lost INT DEFAULT 0,
    INDEX idx_player_name (player_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table: player_game_sessions
-- Stores all gameplay sessions with full state for save/resume
CREATE TABLE IF NOT EXISTS player_game_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    
    -- Game state information
    start_airport_ident VARCHAR(10) NOT NULL,
    safe_airport_ident VARCHAR(10) NOT NULL,
    current_airport_ident VARCHAR(10) NOT NULL,
    
    -- Player resources
    money INT NOT NULL,
    co2 INT NOT NULL,
    round_no INT DEFAULT 1,
    
    -- Game mechanics state
    police_chance FLOAT NOT NULL,
    flight_availability FLOAT NOT NULL,
    
    -- Session status and outcome
    status ENUM('in_progress', 'won', 'lost_resources', 'lost_police', 'abandoned') DEFAULT 'in_progress',
    
    -- Timestamps
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP NULL DEFAULT NULL,
    last_saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Final statistics (populated when game ends)
    final_co2_used INT NULL,
    final_money_used INT NULL,
    final_rounds INT NULL,
    final_distance_traveled INT NULL,
    
    -- Foreign key constraint
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
    
    -- Indexes for common queries
    INDEX idx_player_status (player_id, status),
    INDEX idx_player_finished (player_id, finished_at),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- USEFUL VIEWS FOR LEADERBOARDS AND STATISTICS
-- ============================================================

-- View: player_statistics
-- Aggregates player performance metrics
CREATE OR REPLACE VIEW player_statistics AS
SELECT 
    p.player_id,
    p.player_name,
    p.total_games,
    p.games_won,
    p.games_lost,
    ROUND(p.games_won * 100.0 / NULLIF(p.total_games, 0), 2) AS win_rate,
    MIN(CASE WHEN gs.status = 'won' THEN gs.final_co2_used END) AS best_co2_efficiency,
    MIN(CASE WHEN gs.status = 'won' THEN gs.final_money_used END) AS best_money_efficiency,
    MIN(CASE WHEN gs.status = 'won' THEN gs.final_rounds END) AS fastest_win_rounds,
    p.created_at,
    p.last_played
FROM players p
LEFT JOIN player_game_sessions gs ON p.player_id = gs.player_id
GROUP BY p.player_id, p.player_name, p.total_games, p.games_won, p.games_lost, p.created_at, p.last_played;


-- View: global_leaderboard_co2
-- Top players by CO2 efficiency (lowest CO2 used in winning games)
CREATE OR REPLACE VIEW global_leaderboard_co2 AS
SELECT 
    p.player_name,
    gs.final_co2_used AS co2_used,
    gs.final_rounds AS rounds,
    gs.finished_at
FROM player_game_sessions gs
JOIN players p ON gs.player_id = p.player_id
WHERE gs.status = 'won' AND gs.final_co2_used IS NOT NULL
ORDER BY gs.final_co2_used ASC, gs.final_rounds ASC
LIMIT 100;


-- View: global_leaderboard_speed
-- Top players by speed (fewest rounds to win)
CREATE OR REPLACE VIEW global_leaderboard_speed AS
SELECT 
    p.player_name,
    gs.final_rounds AS rounds,
    gs.final_co2_used AS co2_used,
    gs.final_money_used AS money_used,
    gs.finished_at
FROM player_game_sessions gs
JOIN players p ON gs.player_id = p.player_id
WHERE gs.status = 'won' AND gs.final_rounds IS NOT NULL
ORDER BY gs.final_rounds ASC, gs.final_co2_used ASC
LIMIT 100;


-- ============================================================
-- SAMPLE QUERIES
-- ============================================================

-- Get or create player:
-- SELECT player_id, player_name FROM players WHERE player_name = 'PlayerName';
-- INSERT INTO players (player_name) VALUES ('PlayerName');

-- Load unfinished game for player:
-- SELECT * FROM player_game_sessions WHERE player_id = ? AND status = 'in_progress' ORDER BY last_saved_at DESC LIMIT 1;

-- Save game state:
-- UPDATE player_game_sessions SET current_airport_ident=?, money=?, co2=?, round_no=?, police_chance=?, flight_availability=? WHERE session_id=?;

-- Create new game session:
-- INSERT INTO player_game_sessions (player_id, start_airport_ident, safe_airport_ident, current_airport_ident, money, co2, police_chance, flight_availability) VALUES (?, ?, ?, ?, ?, ?, ?, ?);

-- Complete game session (won):
-- UPDATE player_game_sessions SET status='won', finished_at=NOW(), final_co2_used=?, final_money_used=?, final_rounds=? WHERE session_id=?;
-- UPDATE players SET total_games = total_games + 1, games_won = games_won + 1 WHERE player_id = ?;

-- Get player's personal best:
-- SELECT MIN(final_co2_used) FROM player_game_sessions WHERE player_id = ? AND status = 'won';

-- Get player's game history:
-- SELECT session_id, status, started_at, finished_at, final_rounds, final_co2_used FROM player_game_sessions WHERE player_id = ? ORDER BY started_at DESC;
