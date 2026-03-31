from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# -------------------------------
# تابع بررسی عدد اول
# -------------------------------
def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


# -------------------------------
# API شماره 1: بررسی عدد اول
# -------------------------------
@app.route('/prime_number/<int:number>')
def prime_number(number):
    result = {
        "Number": number,
        "isPrime": is_prime(number)
    }
    return jsonify(result)


# -------------------------------
# اتصال به دیتابیس
# -------------------------------
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="msh701150",
        database="flight_game"   # اسم دیتابیسی که داری
    )
    return connection


# -------------------------------
# API شماره 2: اطلاعات فرودگاه
# -------------------------------
@app.route('/airport/<icao>')
def airport_info(icao):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT name, municipality FROM airport WHERE ident = %s"
    cursor.execute(query, (icao,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        response = {
            "ICAO": icao,
            "Name": result["name"],
            "Location": result["municipality"]
        }
    else:
        response = {
            "error": "Airport not found"
        }

    return jsonify(response)


# -------------------------------
# اجرای سرور
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)