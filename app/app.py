from flask import Flask, jsonify
import socket
from datetime import datetime
import os
import subprocess

app = Flask(__name__)

APP_VERSION = "3.0.0"


def run_cmd(cmd):
    try:
        return subprocess.check_output(
            cmd,
            shell=True,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
    except:
        return "N/A"


def get_hostname():
    return socket.gethostname()


def get_namespace():
    return os.getenv("KUBERNETES_NAMESPACE", "default")


def get_image_tag():
    return os.getenv("IMAGE_TAG", "latest")


def get_build():
    return os.getenv("BUILD_NUMBER", "Unknown")


def get_node():
    return run_cmd("kubectl get pod $(hostname) -o jsonpath='{.spec.nodeName}'")


def get_pod_count():
    return run_cmd("kubectl get pods --no-headers | wc -l")


def get_running_pods():
    return run_cmd("kubectl get pods --no-headers | grep Running | wc -l")


def get_service_count():
    return run_cmd("kubectl get svc --no-headers | wc -l")


def get_deployment_count():
    return run_cmd("kubectl get deploy --no-headers | wc -l")


def get_node_count():
    return run_cmd("kubectl get nodes --no-headers | wc -l")


def get_cluster_health():
    result = run_cmd("kubectl get pods --no-headers")

    if result == "N/A":
        return "Unknown"

    if "CrashLoopBackOff" in result:
        return "Degraded"

    if "Error" in result:
        return "Error"

    return "Healthy"


def get_cpu():
    return run_cmd("kubectl top pod $(hostname) --no-headers | awk '{print $2}'")


def get_memory():
    return run_cmd("kubectl top pod $(hostname) --no-headers | awk '{print $3}'")


def get_restart_count():
    return run_cmd(
        "kubectl get pod $(hostname) -o jsonpath='{.status.containerStatuses[0].restartCount}'"
    )


def get_pod_status():
    return run_cmd(
        "kubectl get pod $(hostname) -o jsonpath='{.status.phase}'"
    )


@app.route("/api/dashboard")
def dashboard():

    return jsonify({

        "hostname": get_hostname(),

        "version": APP_VERSION,

        "namespace": get_namespace(),

        "docker_tag": get_image_tag(),

        "jenkins_build": get_build(),

        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "node": get_node(),

        "cluster_health": get_cluster_health(),

        "pod_status": get_pod_status(),

        "restart_count": get_restart_count(),

        "cpu": get_cpu(),

        "memory": get_memory(),

        "pods": get_pod_count(),

        "running": get_running_pods(),

        "deployments": get_deployment_count(),

        "services": get_service_count(),

        "nodes": get_node_count()

    })


@app.route("/health")
def health():

    return jsonify({

        "status": "healthy",

        "time": str(datetime.now())

    })


@app.route("/info")
def info():

    return jsonify({

        "hostname": get_hostname(),

        "version": APP_VERSION,

        "namespace": get_namespace(),

        "docker_tag": get_image_tag(),

        "build": get_build()

    })


@app.route("/")
def home():

    return """
<!DOCTYPE html>

<html>

<head>

<title>DevOps Dashboard API</title>

<style>

body{
background:#0f172a;
color:white;
font-family:Arial;
text-align:center;
padding-top:100px;
}

a{
color:#38bdf8;
font-size:22px;
text-decoration:none;
}

</style>

</head>

<body>

<h1>🚀 DevOps Dashboard Backend</h1>

<p>Backend is running.</p>

<p><a href="/api/dashboard">Open Dashboard API</a></p>

</body>

</html>

"""


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
