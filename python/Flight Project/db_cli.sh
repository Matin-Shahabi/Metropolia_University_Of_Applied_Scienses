#!/bin/bash

# ============================================================
# TerminalEscape Database CLI Utility
# ============================================================
# Interactive tool for database inspection and management.
# ============================================================

# Database configuration
DB_HOST="localhost"
DB_USER="root"
DB_PASS="msh701150"
DB_NAME="flight_game"
QUERY_FILE="db_client_utility.sql"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Required tables and views
REQUIRED_TABLES=("players" "player_game_sessions")
REQUIRED_VIEWS=("player_statistics" "global_leaderboard_co2" "global_leaderboard_speed")

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

check_mysql_client() {
    if ! command -v mysql &> /dev/null; then
        echo -e "${RED}✗ Error: mysql client not found${NC}"
        echo "Please install: sudo apt install mysql-client"
        exit 1
    fi
}

check_query_file() {
    if [ ! -f "$QUERY_FILE" ]; then
        echo -e "${RED}✗ Error: $QUERY_FILE not found${NC}"
        echo "Run this script from the FlightGame directory"
        exit 1
    fi
}

test_connection() {
    mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "SELECT 1;" &> /dev/null
    return $?
}

# Extract and run a named query from db_client_utility.sql
run_named_query() {
    local query_name="$1"
    local query=$(awk "/-- @QUERY: $query_name/,/-- @END/" "$QUERY_FILE" | grep -v "^-- @" | grep -v "^--$")
    
    if [ -z "$query" ]; then
        echo -e "${RED}✗ Error: Query '$query_name' not found${NC}"
        return 1
    fi
    
    mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "$query"
}

# Run query with stderr captured
run_named_query_raw() {
    local query_name="$1"
    local query=$(awk "/-- @QUERY: $query_name/,/-- @END/" "$QUERY_FILE" | grep -v "^-- @" | grep -v "^--$")
    
    if [ -z "$query" ]; then
        echo -e "${RED}✗ Error: Query '$query_name' not found${NC}"
        return 1
    fi
    
    mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "$query" 2>&1
}

# Run raw SQL query
run_query_raw() {
    mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "$1" 2>&1
}

# Drop all tables and views
drop_all_objects() {
    echo ""
    echo -e "${RED}${BOLD}⚠️  WARNING: This will delete ALL data!${NC}"
    echo "============================================================"
    echo "This action will drop:"
    echo "  - All views (player_statistics, leaderboards)"
    echo "  - All tables (players, player_game_sessions)"
    echo "  - ALL player data, game sessions, and statistics"
    echo ""
    echo "This action CANNOT be undone!"
    echo "============================================================"
    echo ""
    read -p "Are you ABSOLUTELY sure? Type 'DELETE' to confirm: " confirm
    
    if [ "$confirm" != "DELETE" ]; then
        echo -e "${YELLOW}Drop cancelled.${NC}"
        return 1
    fi
    
    echo ""
    echo "Dropping database objects..."
    
    # Drop views first (no dependencies)
    for view in "${REQUIRED_VIEWS[@]}"; do
        echo -e "  Dropping view: ${YELLOW}$view${NC}"
        mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "DROP VIEW IF EXISTS $view;" 2>&1 > /dev/null
    done
    
    # Drop tables (in reverse order due to foreign keys)
    echo -e "  Dropping table: ${YELLOW}player_game_sessions${NC}"
    mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "DROP TABLE IF EXISTS player_game_sessions;" 2>&1 > /dev/null
    
    echo -e "  Dropping table: ${YELLOW}players${NC}"
    mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "DROP TABLE IF EXISTS players;" 2>&1 > /dev/null
    
    echo ""
    echo -e "${GREEN}✓ All objects dropped${NC}"
    echo ""
    echo "You should now run: ./setup_db.sh to recreate tables"
    return 0
}

# ============================================================
# INSPECTION FUNCTIONS
# ============================================================

show_tables() {
    echo -e "\n${CYAN}${BOLD}📋 Tables in database:${NC}"
    echo "============================================================"
    run_named_query "show_tables"
}

show_table_details() {
    echo -e "\n${CYAN}${BOLD}📊 Table Details:${NC}"
    echo "============================================================"
    
    for table in "${REQUIRED_TABLES[@]}"; do
        echo -e "\n${YELLOW}Table: $table${NC}"
        case $table in
            "players")
                run_named_query "show_table_details_players" 2>/dev/null || echo -e "${RED}  ✗ Table does not exist${NC}"
                ;;
            "player_game_sessions")
                run_named_query "show_table_details_sessions" 2>/dev/null || echo -e "${RED}  ✗ Table does not exist${NC}"
                ;;
        esac
    done
}

show_row_counts() {
    echo -e "\n${CYAN}${BOLD}📈 Row Counts:${NC}"
    echo "============================================================"
    run_named_query "show_row_counts"
}

check_database_status() {
    echo -e "\n${CYAN}${BOLD}🔍 Database Status:${NC}"
    echo "============================================================"
    
    # Check tables
    echo -e "\n${BOLD}Tables:${NC}"
    for table in "${REQUIRED_TABLES[@]}"; do
        result=$(run_query_raw "SELECT COUNT(*) as cnt FROM information_schema.TABLES WHERE table_schema='$DB_NAME' AND table_name='$table';" | tail -1)
        if [ "$result" = "1" ]; then
            echo -e "  ${GREEN}✓${NC} $table"
        else
            echo -e "  ${RED}✗${NC} $table ${RED}(MISSING)${NC}"
        fi
    done
    
    # Check views
    echo -e "\n${BOLD}Views:${NC}"
    for view in "${REQUIRED_VIEWS[@]}"; do
        result=$(run_query_raw "SELECT COUNT(*) as cnt FROM information_schema.VIEWS WHERE table_schema='$DB_NAME' AND table_name='$view';" | tail -1)
        if [ "$result" = "1" ]; then
            echo -e "  ${GREEN}✓${NC} $view"
        else
            echo -e "  ${RED}✗${NC} $view ${RED}(MISSING)${NC}"
        fi
    done
    
    echo ""
    echo -e "${YELLOW}Tip: Run ./setup_db.sh to create missing objects${NC}"
}

show_players() {
    echo -e "\n${CYAN}${BOLD}👥 All Players:${NC}"
    echo "============================================================"
    run_named_query "show_players"
}

show_recent_games() {
    echo -e "\n${CYAN}${BOLD}🎮 Recent Games (Last 20):${NC}"
    echo "============================================================"
    run_named_query "show_recent_games"
}

show_leaderboards() {
    echo -e "\n${CYAN}${BOLD}🏆 CO2 Efficiency Leaderboard (Top 10):${NC}"
    echo "============================================================"
    run_named_query "show_leaderboard_co2"
    
    echo -e "\n${CYAN}${BOLD}⚡ Speed Leaderboard (Top 10):${NC}"
    echo "============================================================"
    run_named_query "show_leaderboard_speed"
}

show_active_games() {
    echo -e "\n${CYAN}${BOLD}🎯 Active/Unfinished Games:${NC}"
    echo "============================================================"
    run_named_query "show_active_games"
}

show_game_outcomes() {
    echo -e "\n${CYAN}${BOLD}📊 Game Outcomes Breakdown:${NC}"
    echo "============================================================"
    run_named_query "show_game_outcomes"
}

show_database_size() {
    echo -e "\n${CYAN}${BOLD}💾 Database Size Information:${NC}"
    echo "============================================================"
    run_named_query "show_database_size"
}

# ============================================================
# MAIN MENU
# ============================================================

show_menu() {
    echo ""
    echo "============================================================"
    echo -e "${BOLD}${BLUE}  TerminalEscape Database CLI${NC}"
    echo "============================================================"
    echo ""
    echo -e "${BOLD}Inspection:${NC}"
    echo "  1) Show all tables"
    echo "  2) Show table schemas (structure)"
    echo "  3) Show row counts"
    echo "  4) Check database status"
    echo "  5) Show database size"
    echo ""
    echo -e "${BOLD}Data:${NC}"
    echo "  6) Show all players"
    echo "  7) Show recent games"
    echo "  8) Show active/unfinished games"
    echo "  9) Show game outcomes breakdown"
    echo ""
    echo -e "${BOLD}Leaderboards:${NC}"
    echo "  10) Show leaderboards"
    echo ""
    echo -e "${BOLD}Maintenance:${NC}"
    echo "  11) ${RED}Drop all tables and views${NC} (destructive!)"
    echo ""
    echo -e "${BOLD}Other:${NC}"
    echo "  0) Exit"
    echo ""
    echo "============================================================"
}

main_loop() {
    while true; do
        show_menu
        read -p "Select option: " choice
        
        case $choice in
            1) show_tables ;;
            2) show_table_details ;;
            3) show_row_counts ;;
            4) check_database_status ;;
            5) show_database_size ;;
            6) show_players ;;
            7) show_recent_games ;;
            8) show_active_games ;;
            9) show_game_outcomes ;;
            10) show_leaderboards ;;
            11) drop_all_objects ;;
            0) 
                echo -e "\n${GREEN}Goodbye!${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid option. Please try again.${NC}"
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# ============================================================
# STARTUP
# ============================================================

clear
echo "============================================================"
echo -e "${BOLD}${BLUE}TerminalEscape Database CLI Utility${NC}"
echo "============================================================"

# Check prerequisites
check_mysql_client
check_query_file

echo ""
echo "Testing database connection..."
if test_connection; then
    echo -e "${GREEN}✓ Connected to database: $DB_NAME${NC}"
    
    # Start interactive menu
    main_loop
else
    echo -e "${RED}✗ Failed to connect to database${NC}"
    echo "Please check:"
    echo "  - MariaDB is running: sudo systemctl status mariadb"
    echo "  - Database credentials are correct"
    echo "  - Database '$DB_NAME' exists"
    exit 1
fi
