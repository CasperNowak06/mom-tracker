from flask import Flask

app = Flask(__name__)

# THE FRONTEND (Pure art)
HTML_CODE = """
<!DOCTYPE html><html lang="sv"><head>
    <meta charset="UTF-8">
    <title>Mamma NärVarning™</title>
    <style>body{background:#000;color:#0f0;text-align:center;padding:50px;}</style>
</head><body>
    <h1>🚨 Mamma NärVarning 🚨</h1>
    <p>Status: idk yet lol</p>
    <button onclick="alert('Not implemented yet bro')">Kolla Mamma</button>
</body></html>
"""

@app.route("/")
def index():
    return HTML_CODE

if __name__ == "__main__":
    app.run(debug=True)