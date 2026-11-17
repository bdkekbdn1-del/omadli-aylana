from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            balance INTEGER DEFAULT 0,
            spins INTEGER DEFAULT 1
        )
    ''')
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO users (balance, spins) VALUES (0, 1)')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return "Omadli Aylana Python Serveri ishlayapti!"

@app.route('/get_data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT balance, spins FROM users WHERE id = 1')
    user = cursor.fetchone()
    conn.close()
    return jsonify({"balance": user[0], "spins": user[1]})

@app.route('/update_data', methods=['POST'])
def update_data():
    data = request.json
    balance = data.get('balance')
    spins = data.get('spins')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if balance is not None and spins is not None:
        cursor.execute('UPDATE users SET balance = ?, spins = ? WHERE id = 1', (balance, spins))
    elif balance is not None:
        cursor.execute('UPDATE users SET balance = ? WHERE id = 1', (balance,))
    elif spins is not None:
        cursor.execute('UPDATE users SET spins = ? WHERE id = 1', (spins,))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
  
