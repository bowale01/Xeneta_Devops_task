# wsgi.py

from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host="db",
                            database="rates",
                            user="postgres",
                            password="password")
    return conn

@app.route('/rates', methods=['GET'])
def get_rates():
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    orig_code = request.args.get('orig_code')
    dest_code = request.args.get('dest_code')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT day, price, count
        FROM rates
        WHERE day BETWEEN %s AND %s
        AND orig_code = %s
        AND dest_code = %s
    """, (date_from, date_to, orig_code, dest_code))
    rates = cur.fetchall()

    result = [
        {'day': rate[0], 'price': rate[1], 'count': rate[2]} 
        for rate in rates
    ]
    
    cur.close()
    conn.close()
    
    return jsonify({"rates": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
