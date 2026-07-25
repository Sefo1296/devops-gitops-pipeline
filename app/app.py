from flask import Flask
import socket
from datetime import datetime

app = Flask(__name__)

APP_VERSION = "2.0.0"

@app.route("/")
def home():
    return f"""
<!DOCTYPE html>
<html>
<head>
<title>DevOps GitOps Dashboard</title>

<style>
body {{
    margin:0;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg,#667eea,#764ba2);
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
}}

.card {{
    background:white;
    width:500px;
    padding:40px;
    border-radius:20px;
    text-align:center;
    box-shadow:0 15px 35px rgba(0,0,0,0.3);
}}

h1 {{
    color:#667eea;
    font-size:32px;
}}

.status {{
    background:#d4edda;
    color:#155724;
    padding:10px;
    border-radius:10px;
    margin:20px;
    font-weight:bold;
}}

.info {{
    text-align:left;
    background:#f8f9fa;
    padding:20px;
    border-radius:15px;
}}

.footer {{
    margin-top:20px;
    color:#777;
}}
</style>

</head>

<body>

<div class="card">

<h1>🚀 DevOps GitOps Pipeline</h1>

<div class="status">
✅ Application Running Successfully
</div>

<div class="info">

<p><strong>Version:</strong> {APP_VERSION}</p>

<p><strong>Hostname:</strong> {socket.gethostname()}</p>

<p><strong>Deployment:</strong> Kubernetes + ArgoCD</p>

<p><strong>Time:</strong> {datetime.now()}</p>

</div>

<div class="footer">
Built with Flask | Docker | Jenkins | Kubernetes
</div>

</div>

</body>
</html>
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
