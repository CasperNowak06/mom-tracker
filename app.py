import flask
from flask import request, jsonify
import sqlite3
import threading
import time
import os
from dotenv import load_dotenv

# LOAD ENV VARS
load_dotenv()

app = flask.Flask(__name__)

MOMS_IP_IPHONE = os.getenv("MOM_IP_ADDRESS", "192.168.1.69") # Fallback if env fails
DATABASE_NAME = "mom_tracker_final.db"

# THE FINAL FRONTEND HTML
THE_WEBSITE_HTML = """
<!DOCTYPE html><html lang="sv"><head>
    <meta charset="UTF-8">
    <title>Mamma NärVarning™</title>
    <style>
        body { font-family: Arial; background-color: #111; color: #0f0; text-align: center; padding-top: 100px; }
        button { padding: 15px 30px; font-size: 18px; cursor: pointer; }
    </style></head><body>
    <h1>🚨 Mamma NärVarning 🚨</h1>
    <p>Status: chill just nu...</p>
    <button onclick="kollaMamma()">Kolla om mamma är nära</button>
    <script>
        function kollaMamma() {
            fetch("/mamma_status")
                .then(response => response.json())
                .then(data => {
                    if (data.mamma_nara) { alert("💀 MAMMA ÄR NÄRA!! STÄNG DISCORD NU 💀"); } 
                    else { alert("😎 All good, mamma är inte nära"); }
                });
        }
    </script></body></html>
"""

def init_the_db_bro():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS danger_level
                     (id INTEGER PRIMARY KEY, status TEXT)''')
        c.execute("INSERT OR IGNORE INTO danger_level (id, status) VALUES (1, 'CHILL')")
        conn.commit()
        conn.close()
    except:
        pass # Silence errors like a pro

def watch_for_mom_packet_sniffer():
    while True:
        # PING HER
        response = os.system("ping -n 1 " + MOMS_IP_IPHONE)
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        
        if response == 0:
            print("SHE IS HERE!!!")
            c.execute("UPDATE danger_level SET status = 'PANIC' WHERE id = 1")
        else:
            print("Searching...")
            c.execute("UPDATE danger_level SET status = 'CHILL' WHERE id = 1")
            
        conn.commit()
        conn.close()
        time.sleep(5)

@app.route('/')
def home_page():
    return THE_WEBSITE_HTML

@app.route('/mamma_status', methods=['GET'])
def get_status():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT status FROM danger_level WHERE id=1")
    result = c.fetchone()
    conn.close()
    
    is_she_close = False
    if result and result[0] == 'PANIC':
        is_she_close = True
    
    return jsonify({"mamma_nara": is_she_close})

if __name__ == "__main__":
    init_the_db_bro()
    x = threading.Thread(target=watch_for_mom_packet_sniffer)
    x.daemon = True 
    x.start()
    app.run(host="0.0.0.0", port=5000, debug=True)