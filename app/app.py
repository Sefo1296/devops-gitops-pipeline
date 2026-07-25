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
    width:450px;
    padding:35px;
    border-radius:20px;
    box-shadow:0 10px 30px rgba(0,0,0,0.3);
    text-align:center;
}}

h1 {{
    color:#667eea;
    font-size:32px;
}}

.welcome {{
    color:#555;
    font-size:18px;
}}

.info {{
    background:#f4f6ff;
    padding:15px;
    border-radius:12px;
    margin-top:20px;
    text-align:left;
}}

.badge {{
    display:inline-block;
    background:#28a745;
    color:white;
    padding:8px 15px;
    border-radius:20px;
    margin-top:15px;
}}

.footer {{
    margin-top:20px;
    color:#888;
    font-size:13px;
}}

</style>

</head>

<body>

<div class="card">

<h1>🚀 DevOps GitOps Pipeline</h1>

<p class="welcome">
Welcome to the new colorful Flask application!
</p>

<div class="badge">
Application Healthy
</div>


<div class="info">

<p><b>Version:</b> {APP_VERSION}</p>

<p><b>Hostname:</b> {socket.gethostname()}</p>

<p><b>Time:</b> {datetime.now()}</p>

</div>


<div class="footer">
Powered by Jenkins + Docker + Kubernetes + ArgoCD
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
