from flask import Flask, jsonify
import socket
from datetime import datetime
import os

from kubernetes import client, config


app = Flask(__name__)

APP_VERSION = "3.0.0"


# Load Kubernetes configuration from inside the pod
try:
    config.load_incluster_config()

    v1 = client.CoreV1Api()
    apps = client.AppsV1Api()

    kubernetes_available = True

except Exception as e:
    v1 = None
    apps = None
    kubernetes_available = False


def get_hostname():
    return socket.gethostname()


def get_namespace():
    return os.getenv("KUBERNETES_NAMESPACE", "default")


def get_image_tag():
    return os.getenv("IMAGE_TAG", "latest")


def get_build():
    return os.getenv("BUILD_NUMBER", "Unknown")


def get_node():

    if not kubernetes_available:
        return "N/A"

    try:
        pod = v1.read_namespaced_pod(
            name=get_hostname(),
            namespace=get_namespace()
        )

        return pod.spec.node_name

    except Exception:
        return "N/A"


def get_pod_count():

    if not kubernetes_available:
        return 0

    try:
        pods = v1.list_namespaced_pod(
            namespace=get_namespace()
        )

        return len(pods.items)

    except Exception:
        return 0


def get_running_pods():

    if not kubernetes_available:
        return 0

    try:
        pods = v1.list_namespaced_pod(
            namespace=get_namespace()
        )

        return len([
            pod for pod in pods.items
            if pod.status.phase == "Running"
        ])

    except Exception:
        return 0


def get_service_count():

    if not kubernetes_available:
        return 0

    try:
        services = v1.list_namespaced_service(
            namespace=get_namespace()
        )

        return len(services.items)

    except Exception:
        return 0


def get_deployment_count():

    if not kubernetes_available:
        return 0

    try:
        deployments = apps.list_namespaced_deployment(
            namespace=get_namespace()
        )

        return len(deployments.items)

    except Exception:
        return 0


def get_node_count():

    if not kubernetes_available:
        return 0

    try:
        nodes = v1.list_node()

        return len(nodes.items)

    except Exception:
        return 0


def get_cluster_health():

    if not kubernetes_available:
        return "Unknown"

    try:
        pods = v1.list_namespaced_pod(
            namespace=get_namespace()
        )

        for pod in pods.items:

            if pod.status.phase in ["Failed", "Unknown"]:
                return "Degraded"

        return "Healthy"

    except Exception:
        return "Unknown"


def get_pod_status():

    if not kubernetes_available:
        return "N/A"

    try:
        pod = v1.read_namespaced_pod(
            name=get_hostname(),
            namespace=get_namespace()
        )

        return pod.status.phase

    except Exception:
        return "N/A"


def get_restart_count():

    if not kubernetes_available:
        return 0

    try:
        pod = v1.read_namespaced_pod(
            name=get_hostname(),
            namespace=get_namespace()
        )

        return pod.status.container_statuses[0].restart_count

    except Exception:
        return 0


def get_cpu():
    pod = get_hostname()
    return run_cmd(
        f"kubectl top pod {pod} --no-headers | awk '{{print $2}}'"
    )


def get_memory():
    pod = get_hostname()
    return run_cmd(
        f"kubectl top pod {pod} --no-headers | awk '{{print $3}}'"
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
