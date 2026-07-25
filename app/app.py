from flask import Flask
import socket
from datetime import datetime
import os

app = Flask(__name__)

APP_VERSION = "2.0.0"

@app.route("/")
def home():

    hostname = socket.gethostname()
    namespace = os.getenv("KUBERNETES_NAMESPACE", "default")
    image = os.getenv("IMAGE_TAG", "latest")
    build = os.getenv("BUILD_NUMBER", "Unknown")

    return f"""
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">
<title>DevOps Dashboard</title>

<style>

body {{
margin:0;
font-family:Arial;
background:linear-gradient(-45deg,#667eea,#764ba2,#6dd5fa,#23d5ab);
background-size:400% 400%;
animation:bg 12s ease infinite;
color:white;
}}

@keyframes bg {{
0%{{background-position:0% 50%;}}
50%{{background-position:100% 50%;}}
100%{{background-position:0% 50%;}}
}}

.container{{
width:90%;
max-width:1200px;
margin:auto;
padding:40px;
}}

h1{{
text-align:center;
font-size:42px;
}}

.grid{{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
gap:20px;
margin-top:40px;
}}

.card{{
background:rgba(255,255,255,.15);
backdrop-filter:blur(15px);
padding:25px;
border-radius:20px;
transition:.3s;
box-shadow:0 8px 20px rgba(0,0,0,.3);
}}

.card:hover{{
transform:translateY(-8px);
}}

.value{{
font-size:26px;
font-weight:bold;
margin-top:10px;
}}

</style>

</head>

<body>

<div class="container">

<h1>🚀 DevOps Dashboard</h1>

<div class="grid">

<div class="card">
Hostname
<div class="value">{hostname}</div>
</div>

<div class="card">
Version
<div class="value">{APP_VERSION}</div>
</div>

<div class="card">
Namespace
<div class="value">{namespace}</div>
</div>

<div class="card">
Docker Tag
<div class="value">{image}</div>
</div>

<div class="card">
Jenkins Build
<div class="value">{build}</div>
</div>

<div class="card">
Current Time
<div class="value">{datetime.now().strftime("%H:%M:%S")}</div>
</div>

</div>

</div>

</body>
</html>
"""

@app.route("/health")
def health():
    return {"status":"healthy"}

@app.route("/info")
def info():
    return {
        "version":APP_VERSION,
        "hostname":socket.gethostname(),
        "time":str(datetime.now())
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
