#!/bin/bash

# ============================================================
# TerminalEscape Database Setup
# ============================================================
# Idempotent setup script - safe to run multiple times.
# Checks for required tables/views and creates missing ones.
#
# Usage:
#   ./setup_db.sh           # Normal setup (creates missing objects)
#   ./setup_db.sh --drop    # Drop all tables and recreate
#   ./setup_db.sh -d        # Same as --drop
# ============================================================

# Database configuration
DB_HOST="localhost"
DB_USER="root"
DB_PASS="msh701150"
DB_NAME="flight_game"
SCHEMA_FILE="setup_database.sql"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

# Required tables and views
REQUIRED_TABLES=("players" "player_game_sessions")
REQUIRED_VIEWS=("player_statistics" "global_leaderboard_co2" "global_leaderboard_speed")

# Parse command line arguments
DROP_TABLES=false
if [[ "$1" == "--drop" ]] || [[ "$1" == "-d" ]]; then
    DROP_TABLES=true
fi

# ============================================================
# HELPER FUNCTIONS
# ============================================================

check_mysql_client() {
    if ! command -v mysql &> /dev/null; then
        echo -e "${RED}✗ Error: mysql client not found${NC}"
        echo "Please install: sudo apt install mysql-client"
        exit 1
    fi
}

test_connection() {
    mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "SELECT 1;" &> /dev/null
    return $?
}

check_object() {
    local type=$1  # TABLES or VIEWS
    local name=$2
    local result=$(mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "SELECT COUNT(*) as cnt FROM information_schema.$type WHERE table_schema='$DB_NAME' AND table_name='$name';" 2>&1 | tail -1)
    echo "$result"
}

drop_all_objects() {
    echo -e "${RED}${BOLD}⚠️  WARNING: This will delete ALL data!${NC}"
    echo "This action will drop:"
    echo "  - All views (player_statistics, leaderboards)"
    echo "  - All tables (players, player_game_sessions)"
    echo "  - ALL player data, game sessions, and statistics"
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
        mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "DROP VIEW IF EXISTS $view;" 2>&1
    done
    
    # Drop tables (in reverse order due to foreign keys)
    echo -e "  Dropping table: ${YELLOW}player_game_sessions${NC}"
    mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "DROP TABLE IF EXISTS player_game_sessions;" 2>&1
    
    echo -e "  Dropping table: ${YELLOW}players${NC}"
    mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "DROP TABLE IF EXISTS players;" 2>&1
    
    echo -e "${GREEN}✓ All objects dropped${NC}"
    return 0
}

# ============================================================
# MAIN SETUP
# ============================================================

echo "============================================================"
echo -e "${BOLD}${BLUE}TerminalEscape Database Setup${NC}"
if $DROP_TABLES; then
    echo -e "${RED}[DROP MODE]${NC}"
fi
echo "============================================================"
echo ""

# Check prerequisites
check_mysql_client

if [ ! -f "$SCHEMA_FILE" ]; then
    echo -e "${RED}✗ Error: $SCHEMA_FILE not found${NC}"
    echo "Run this script from the FlightGame directory"
    exit 1
fi

echo "Testing database connection..."
if ! test_connection; then
    echo -e "${RED}✗ Failed to connect to database${NC}"
    echo "Please check:"
    echo "  - MariaDB is running"
    echo "  - Credentials are correct"
    echo "  - Database '$DB_NAME' exists"
    exit 1
fi
echo -e "${GREEN}✓ Connected to database: $DB_NAME${NC}"
echo ""

# Handle drop flag
if $DROP_TABLES; then
    if drop_all_objects; then
        echo ""
        echo "Proceeding with recreation..."
        echo ""
    else
        exit 1
    fi
fi

# Check current status
echo "Checking database objects..."
echo ""

missing_tables=0
missing_views=0

echo -e "${BOLD}Tables:${NC}"
for table in "${REQUIRED_TABLES[@]}"; do
    result=$(check_object "TABLES" "$table")
    if [ "$result" = "1" ]; then
        echo -e "  ${GREEN}✓${NC} $table"
    else
        echo -e "  ${YELLOW}○${NC} $table (missing)"
        missing_tables=$((missing_tables + 1))
    fi
done

echo ""
echo -e "${BOLD}Views:${NC}"
for view in "${REQUIRED_VIEWS[@]}"; do
    result=$(check_object "VIEWS" "$view")
    if [ "$result" = "1" ]; then
        echo -e "  ${GREEN}✓${NC} $view"
    else
        echo -e "  ${YELLOW}○${NC} $view (missing)"
        missing_views=$((missing_views + 1))
    fi
done

echo ""
echo "============================================================"

# Determine action
if [ $missing_tables -eq 0 ] && [ $missing_views -eq 0 ]; then
    echo -e "${GREEN}✓ All database objects exist - setup complete!${NC}"
    exit 0
fi

# Need to run setup
echo -e "${YELLOW}Missing: $missing_tables table(s), $missing_views view(s)${NC}"
echo ""
echo "Running database setup..."
echo ""

mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" < "$SCHEMA_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo -e "${GREEN}✓ Database setup completed successfully!${NC}"
    echo ""
    
    # Verify setup
    echo "Verifying objects..."
    all_ok=true
    for table in "${REQUIRED_TABLES[@]}"; do
        result=$(check_object "TABLES" "$table")
        if [ "$result" != "1" ]; then
            echo -e "  ${RED}✗${NC} Table $table still missing"
            all_ok=false
        fi
    done
    for view in "${REQUIRED_VIEWS[@]}"; do
        result=$(check_object "VIEWS" "$view")
        if [ "$result" != "1" ]; then
            echo -e "  ${RED}✗${NC} View $view still missing"
            all_ok=false
        fi
    done
    
    if $all_ok; then
        echo -e "${GREEN}✓ All objects verified${NC}"
    fi
    exit 0
else
    echo ""
    echo "============================================================"
    echo -e "${RED}✗ Setup failed - check error messages above${NC}"
    exit 1
fi
