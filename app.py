from flask import Flask, jsonify
import os
import sqlite3

app = Flask(__name__)
MOMS_IP = "192.168.1.69"

def init_db():
    conn = sqlite3.connect('mom.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS status (msg TEXT)')
    # clear old data
    c.execute('DELETE FROM status')
    c.execute("INSERT INTO status VALUES ('UNKNOWN')")
    conn.commit()
    conn.close()

init_db() # Run this when app starts

@app.route("/")
def index():
    return "<h1>Go to /check to check status (no frontend rn, im fixing backend)</h1>"

@app.route("/check")
def check_mom():
    response = os.system("ping -n 1 " + MOMS_IP)
    msg = "CHILL"
    if response == 0:
        msg = "PANIC"
        
    # SQL INJECTION (The good kind)
    conn = sqlite3.connect('mom.db')
    c = conn.cursor()
    c.execute(f"UPDATE status SET msg = '{msg}'") # f-strings are fast
    conn.commit()
    conn.close()
    
    return jsonify({"status": msg})

if __name__ == "__main__":
    app.run(debug=True)