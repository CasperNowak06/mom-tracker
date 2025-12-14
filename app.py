from flask import Flask, jsonify
import os

app = Flask(__name__)

MOMS_IP = "192.168.1.69" # lol

HTML_CODE = """
<!DOCTYPE html><html lang="sv"><head>
    <meta charset="UTF-8">
    <style>body{background:#000;color:#0f0;text-align:center;padding:50px;}</style>
</head><body>
    <h1>🚨 Mamma NärVarning 🚨</h1>
    <button onclick="check()">CHECK STATUS</button>
    <script>
    function check() {
        fetch('/check').then(r => r.json()).then(d => alert(d.status));
    }
    </script>
</body></html>
"""

@app.route("/")
def index():
    return HTML_CODE

@app.route("/check")
def check_mom():
    # HACKER LOGIC
    response = os.system("ping -n 1 " + MOMS_IP)
    status = "SAFE"
    if response == 0:
        status = "RUN FOR YOUR LIFE"
    
    # Save to file just in case (Persistence layer)
    f = open("status.txt", "w")
    f.write(status)
    f.close()
    
    return jsonify({"status": status})

if __name__ == "__main__":
    app.run(debug=True)