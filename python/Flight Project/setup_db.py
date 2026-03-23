#!/usr/bin/env python3

"""
TerminalEscape Database Setup
==================================
Idempotent setup script - safe to run multiple times.
Checks for required tables/views and creates missing ones.

Usage:
    python3 setup_db.py           # Normal setup (creates missing objects)
    python3 setup_db.py --drop    # Drop all tables and recreate
    python3 setup_db.py -d        # Same as --drop
"""

import sys
import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'msh701150',
    'database': 'flight_game'
}

SCHEMA_FILE = 'setup_database.sql'

# Required database objects
REQUIRED_TABLES = ['players', 'player_game_sessions']
REQUIRED_VIEWS = ['player_statistics', 'global_leaderboard_co2', 'global_leaderboard_speed']

# ANSI color codes
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color


def test_connection():
    """Test database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        conn.close()
        return True
    except Error:
        return False


def check_object(cursor, object_type, name):
    """
    Check if a table or view exists.
    
    Args:
        cursor: Database cursor
        object_type: 'TABLES' or 'VIEWS'
        name: Object name
    
    Returns:
        bool: True if exists, False otherwise
    """
    query = f"""
        SELECT COUNT(*) as cnt 
        FROM information_schema.{object_type}
        WHERE table_schema = %s AND table_name = %s
    """
    cursor.execute(query, (DB_CONFIG['database'], name))
    result = cursor.fetchone()
    return result['cnt'] == 1


def run_schema_file(cursor, filepath):
    """
    Execute SQL from schema file.
    
    Args:
        cursor: Database cursor
        filepath: Path to SQL file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filepath, 'r') as f:
            sql_script = f.read()
        
        # Split by semicolons and execute each statement
        statements = sql_script.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
        
        return True
    except Exception as e:
        print(f"{Colors.RED}Error executing SQL: {e}{Colors.NC}")
        return False


def drop_all_objects(cursor, conn):
    """
    Drop all tables and views.
    
    Args:
        cursor: Database cursor
        conn: Database connection
    
    Returns:
        bool: True if confirmed and dropped, False if cancelled
    """
    print(f"{Colors.RED}{Colors.BOLD}⚠️  WARNING: This will delete ALL data!{Colors.NC}")
    print("This action will drop:")
    print("  - All views (player_statistics, leaderboards)")
    print("  - All tables (players, player_game_sessions)")
    print("  - ALL player data, game sessions, and statistics")
    print()
    
    confirm = input("Are you ABSOLUTELY sure? Type 'DELETE' to confirm: ")
    
    if confirm != 'DELETE':
        print(f"{Colors.YELLOW}Drop cancelled.{Colors.NC}")
        return False
    
    print()
    print("Dropping database objects...")
    
    try:
        # Drop views first (no dependencies)
        for view in REQUIRED_VIEWS:
            print(f"  Dropping view: {Colors.YELLOW}{view}{Colors.NC}")
            cursor.execute(f"DROP VIEW IF EXISTS {view}")
        
        # Drop tables (in reverse order due to foreign keys)
        print(f"  Dropping table: {Colors.YELLOW}player_game_sessions{Colors.NC}")
        cursor.execute("DROP TABLE IF EXISTS player_game_sessions")
        
        print(f"  Dropping table: {Colors.YELLOW}players{Colors.NC}")
        cursor.execute("DROP TABLE IF EXISTS players")
        
        conn.commit()
        print(f"{Colors.GREEN}✓ All objects dropped{Colors.NC}")
        return True
        
    except Error as e:
        print(f"{Colors.RED}Error dropping objects: {e}{Colors.NC}")
        return False


def main():
    """Main setup function."""
    # Check for drop flag
    drop_mode = len(sys.argv) > 1 and sys.argv[1] in ['--drop', '-d']
    
    print("=" * 60)
    print(f"{Colors.BOLD}{Colors.BLUE}TerminalEscape Database Setup{Colors.NC}")
    if drop_mode:
        print(f"{Colors.RED}[DROP MODE]{Colors.NC}")
    print("=" * 60)
    print()
    
    # Check if schema file exists
    try:
        with open(SCHEMA_FILE, 'r') as f:
            pass
    except FileNotFoundError:
        print(f"{Colors.RED}✗ Error: {SCHEMA_FILE} not found{Colors.NC}")
        print("Run this script from the FlightGame directory")
        sys.exit(1)
    
    # Test connection
    print("Testing database connection...")
    if not test_connection():
        print(f"{Colors.RED}✗ Failed to connect to database{Colors.NC}")
        print("Please check:")
        print("  - MariaDB is running")
        print("  - Credentials are correct")
        print(f"  - Database '{DB_CONFIG['database']}' exists")
        sys.exit(1)
    
    print(f"{Colors.GREEN}✓ Connected to database: {DB_CONFIG['database']}{Colors.NC}")
    print()
    
    # Connect to database
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
    except Error as e:
        print(f"{Colors.RED}✗ Connection error: {e}{Colors.NC}")
        sys.exit(1)
    
    # Handle drop mode
    if drop_mode:
        if drop_all_objects(cursor, conn):
            print()
            print("Proceeding with recreation...")
            print()
        else:
            cursor.close()
            conn.close()
            sys.exit(1)
    
    # Check current status
    print("Checking database objects...")
    print()
    
    missing_tables = 0
    missing_views = 0
    
    print(f"{Colors.BOLD}Tables:{Colors.NC}")
    for table in REQUIRED_TABLES:
        if check_object(cursor, 'TABLES', table):
            print(f"  {Colors.GREEN}✓{Colors.NC} {table}")
        else:
            print(f"  {Colors.YELLOW}○{Colors.NC} {table} (missing)")
            missing_tables += 1
    
    print()
    print(f"{Colors.BOLD}Views:{Colors.NC}")
    for view in REQUIRED_VIEWS:
        if check_object(cursor, 'VIEWS', view):
            print(f"  {Colors.GREEN}✓{Colors.NC} {view}")
        else:
            print(f"  {Colors.YELLOW}○{Colors.NC} {view} (missing)")
            missing_views += 1
    
    print()
    print("=" * 60)
    
    # Determine action
    if missing_tables == 0 and missing_views == 0:
        print(f"{Colors.GREEN}✓ All database objects exist - setup complete!{Colors.NC}")
        cursor.close()
        conn.close()
        sys.exit(0)
    
    # Need to run setup
    print(f"{Colors.YELLOW}Missing: {missing_tables} table(s), {missing_views} view(s){Colors.NC}")
    print()
    print("Running database setup...")
    print()
    
    # Execute schema file
    if run_schema_file(cursor, SCHEMA_FILE):
        conn.commit()
        
        print()
        print("=" * 60)
        print(f"{Colors.GREEN}✓ Database setup completed successfully!{Colors.NC}")
        print()
        
        # Verify setup
        print("Verifying objects...")
        all_ok = True
        
        for table in REQUIRED_TABLES:
            if not check_object(cursor, 'TABLES', table):
                print(f"  {Colors.RED}✗{Colors.NC} Table {table} still missing")
                all_ok = False
        
        for view in REQUIRED_VIEWS:
            if not check_object(cursor, 'VIEWS', view):
                print(f"  {Colors.RED}✗{Colors.NC} View {view} still missing")
                all_ok = False
        
        if all_ok:
            print(f"{Colors.GREEN}✓ All objects verified{Colors.NC}")
        
        cursor.close()
        conn.close()
        sys.exit(0)
    else:
        print()
        print("=" * 60)
        print(f"{Colors.RED}✗ Setup failed - check error messages above{Colors.NC}")
        cursor.close()
        conn.close()
        sys.exit(1)


if __name__ == "__main__":
    main()
