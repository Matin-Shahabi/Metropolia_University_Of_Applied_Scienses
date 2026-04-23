# backend/services/db.py
import mysql.connector
from mysql.connector import Error
from config import Config

db = None
cursor = None

def init_db():
    """Initialize database connection"""
    global db, cursor
    try:
        db = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = db.cursor(dictionary=True)
        print("✅ Database connection successful")
        return True
    except Error as e:
        print(f"❌ Database connection failed: {e}")
        return False

def get_cursor():
    """Get database cursor (reconnect if needed)"""
    global db, cursor
    if not db or not db.is_connected():
        init_db()
    return cursor

def commit():
    """Commit changes to database"""
    if db:
        db.commit()