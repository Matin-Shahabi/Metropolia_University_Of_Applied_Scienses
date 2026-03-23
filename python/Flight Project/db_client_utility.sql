-- ============================================================
-- Database Client Utility - Query Collection
-- ============================================================
-- This file contains executable queries for the CLI utility.
-- Queries are marked with @QUERY: name and @END tags.
-- The bash script extracts and executes these queries.
-- ============================================================


-- ============================================================
-- INSPECTION QUERIES
-- ============================================================

-- @QUERY: show_tables
SHOW TABLES;
-- @END

-- @QUERY: show_table_details_players
DESCRIBE players;
-- @END

-- @QUERY: show_table_details_sessions
DESCRIBE player_game_sessions;
-- @END

-- @QUERY: show_row_counts
SELECT 
    'players' as table_name, COUNT(*) as row_count FROM players
UNION ALL
SELECT 'player_game_sessions', COUNT(*) FROM player_game_sessions;
-- @END

-- @QUERY: show_views
SHOW FULL TABLES WHERE Table_type = 'VIEW';
-- @END


-- ============================================================
-- PLAYER QUERIES
-- ============================================================

-- @QUERY: show_players
SELECT 
    player_id as ID,
    player_name as Name,
    total_games as Games,
    games_won as Wins,
    games_lost as Losses,
    ROUND(games_won * 100.0 / NULLIF(total_games, 0), 1) AS 'Win%',
    DATE_FORMAT(last_played, '%Y-%m-%d %H:%i') as 'Last Played'
FROM players
ORDER BY last_played DESC;
-- @END

-- @QUERY: show_top_players
SELECT 
    player_name,
    total_games,
    games_won,
    games_lost,
    ROUND(games_won * 100.0 / NULLIF(total_games, 0), 2) AS win_rate
FROM players
ORDER BY total_games DESC
LIMIT 10;
-- @END


-- ============================================================
-- GAME SESSION QUERIES
-- ============================================================

-- @QUERY: show_recent_games
SELECT 
    p.player_name as Player,
    gs.status as Status,
    gs.final_rounds as Rounds,
    gs.final_co2_used as CO2,
    DATE_FORMAT(gs.started_at, '%Y-%m-%d %H:%i') as Started
FROM player_game_sessions gs
JOIN players p ON gs.player_id = p.player_id
ORDER BY gs.started_at DESC
LIMIT 20;
-- @END

-- @QUERY: show_active_games
SELECT 
    p.player_name as Player,
    gs.current_airport_ident as Location,
    gs.money as Money,
    gs.co2 as CO2,
    gs.round_no as Round,
    DATE_FORMAT(gs.last_saved_at, '%Y-%m-%d %H:%i') as 'Last Saved'
FROM player_game_sessions gs
JOIN players p ON gs.player_id = p.player_id
WHERE gs.status = 'in_progress'
ORDER BY gs.last_saved_at DESC;
-- @END

-- @QUERY: show_game_outcomes
SELECT 
    status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM player_game_sessions WHERE status != 'in_progress'), 2) as percentage
FROM player_game_sessions
WHERE status != 'in_progress'
GROUP BY status
ORDER BY count DESC;
-- @END


-- ============================================================
-- LEADERBOARD QUERIES
-- ============================================================

-- @QUERY: show_leaderboard_co2
SELECT * FROM global_leaderboard_co2 LIMIT 10;
-- @END

-- @QUERY: show_leaderboard_speed
SELECT * FROM global_leaderboard_speed LIMIT 10;
-- @END

-- @QUERY: show_player_statistics
SELECT * FROM player_statistics ORDER BY win_rate DESC LIMIT 10;
-- @END


-- ============================================================
-- MAINTENANCE QUERIES
-- ============================================================

-- @QUERY: cleanup_abandoned_games
UPDATE player_game_sessions 
SET status = 'abandoned' 
WHERE status = 'in_progress' 
AND last_saved_at < DATE_SUB(NOW(), INTERVAL 30 DAY);
-- @END

-- @QUERY: show_database_size
SELECT 
    table_name AS 'Table',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'test_flight_game_db'
ORDER BY (data_length + index_length) DESC;
-- @END


-- ============================================================
-- TESTING QUERIES
-- ============================================================

-- @QUERY: test_connection
SELECT 'Database connection successful!' as status, NOW() as timestamp;
-- @END

-- @QUERY: verify_tables
SELECT 
    CASE 
        WHEN COUNT(*) = 2 THEN 'All required tables exist'
        ELSE CONCAT('Missing tables! Found: ', COUNT(*), ' of 2')
    END as table_check
FROM information_schema.TABLES
WHERE table_schema = 'test_flight_game_db'
AND table_name IN ('players', 'player_game_sessions');
-- @END

-- @QUERY: verify_views
SELECT 
    CASE 
        WHEN COUNT(*) = 3 THEN 'All required views exist'
        ELSE CONCAT('Missing views! Found: ', COUNT(*), ' of 3')
    END as view_check
FROM information_schema.VIEWS
WHERE table_schema = 'test_flight_game_db'
AND table_name IN ('player_statistics', 'global_leaderboard_co2', 'global_leaderboard_speed');
-- @END

-- @QUERY: show_foreign_keys
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE table_schema = 'test_flight_game_db'
AND REFERENCED_TABLE_NAME IS NOT NULL;
-- @END
