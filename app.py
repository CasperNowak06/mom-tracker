from flask import Flask, jsonify
import os
import sqlite3
from dotenv import load_dotenv # NEW TECH

load_dotenv() # Load the secrets shhhh

app = Flask(__name__)

# GETTING THE SECRET VAR
MOMS_IP = os.getenv("MOM_IP_ADDRESS")
print("Target acquired: " + MOMS_IP)

def init_db():
    conn = sqlite3.connect('mom.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS status (msg TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return """
    <button onclick="fetch('/check').then(r=>r.json()).then(d=>alert(d.status))">
    CHECK MOM
    </button>
    """

@app.route("/check")
def check_mom():
    # Still doing the ping here, page loads kinda slow but whatever
    response = os.system("ping -n 1 " + MOMS_IP)
    msg = "CHILL"
    if response == 0:
        msg = "PANIC"
    
    conn = sqlite3.connect('mom.db')
    c = conn.cursor()
    c.execute("UPDATE status SET msg = ?", (msg,)) # My discord friend said use ? for safety
    conn.commit()
    conn.close()
    
    return jsonify({"status": msg})

if __name__ == "__main__":
    app.run(debug=True)