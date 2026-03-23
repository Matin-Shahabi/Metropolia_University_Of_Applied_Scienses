import mysql.connector
import random

# ============================================================
# DATABASE CONNECTION
# ============================================================
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="msh701150",
    database="flight_game"
)

cursor = db.cursor(dictionary=True)

# ============================================================
# DATABASE HELPERS
# ============================================================
def get_large_airports():
    cursor.execute("SELECT * FROM airport WHERE type='large_airport' GROUP BY iso_country")
    return cursor.fetchall()

def get_airport_details(ident):
    cursor.execute("SELECT * FROM airport WHERE ident=%s", (ident,))
    return cursor.fetchone()

def get_random_airport(exclude_country=None):
    airports = get_large_airports()
    if exclude_country:
        airports = [a for a in airports if a["iso_country"] != exclude_country]
    return random.choice(airports)

def country_iso_to_name():
    cursor.execute("SELECT iso_country, name FROM country")
    rows = cursor.fetchall()
    return {row['iso_country']: row['name'] for row in rows}
