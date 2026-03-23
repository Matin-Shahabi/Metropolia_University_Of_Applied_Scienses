##########################              exercise 1               #########################
import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='flight_game',
    user='root',
    password='RN1363rn1363',
    autocommit=True
)

icao = input("Enter ICAO code: ").strip().upper()

sql = "SELECT name, municipality FROM airport WHERE ident = %s"
cursor = connection.cursor()
cursor.execute(sql, (icao,))
result = cursor.fetchone()

if result:
    name, municipality = result
    print(f"Airport name: {name}")
    print(f"Location (town): {municipality}")
else:
    print("No airport found with that ICAO code.")

 ################################   exersice 2    ###################################
import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='flight_game',
    user='root',
    password='RN1363rn1363',
    autocommit=True
)

country = input("Enter country code (e.g. FI): ").strip().upper()

sql = """
     SELECT type, COUNT(*) 
     FROM airport 
     WHERE iso_country = %s 
     GROUP BY type 
     ORDER BY type
 """
cursor = connection.cursor()
cursor.execute(sql, (country,))
results = cursor.fetchall()

if results:
    print(f"Airports in country {country}:")
    for airport_type, count in results:
        print(f"{airport_type}: {count}")
else:
    print("No airports found for that country code.")
############################     exersice 3    ###########################
import mysql.connector
from geopy.distance import distance

connection = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='flight_game',
    user='root',
    password='RN1363rn1363',
    autocommit=True
)

icao1 = input("Enter first ICAO code: ").strip().upper()
icao2 = input("Enter second ICAO code: ").strip().upper()

def get_coordinates(icao_code):
    sql = """
        SELECT latitude_deg, longitude_deg 
        FROM airport 
        WHERE ident = %s
    """
    cursor = connection.cursor()
    cursor.execute(sql, (icao_code,))
    result = cursor.fetchone()
    if result:
        return result[0], result[1]
    else:
        return None

coords1 = get_coordinates(icao1)
coords2 = get_coordinates(icao2)

if not coords1:
    print(f"No airport found with ICAO code {icao1}.")
elif not coords2:
    print(f"No airport found with ICAO code {icao2}.")
else:
    dist_km = distance(coords1, coords2).km
    print(f"Distance between {icao1} and {icao2}: {dist_km:.2f} km")



