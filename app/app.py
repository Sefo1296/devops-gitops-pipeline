from flask import Flask
import socket
from datetime import datetime

app = Flask(__name__)

APP_VERSION = "1.0.0"

@app.route("/")
def home():
    return f"""
    <h1>DevOps GitOps Pipeline</h1>
    <p>Welcome to THE BEST EVER Flask application!</p>
    <p><strong>Version:</strong> {APP_VERSION}</p>
    <p><strong>Hostname:</strong> {socket.gethostname()}</p>
    <p><strong>Time:</strong> {datetime.now()}</p>
    """

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

@app.route("/info")
def info():
    return {
        "version": APP_VERSION,
        "hostname": socket.gethostname(),
        "time": str(datetime.now())
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
