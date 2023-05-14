import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
REQUIRED_SOFTWARE_PATH = os.path.join(BASE_DIR, "airlift/required_software.yaml")
DEFAULT_AIRLIFT_CONFIG_FILE = os.path.join(BASE_DIR, "airlift/config.yaml")
DEFAULT_HELM_CONFIG_FILE = os.path.join(BASE_DIR, "helm/values.yaml")
DEFAULT_CLUSTER_CONFIG_FILE = os.path.join(BASE_DIR, "kind/cluster.yaml")
FINAL_HELM_VALUES_FILE_PATH = os.path.join(BASE_DIR, "helm/final_values.yaml")
FINAL_CONFIG_VALUES_FILE_PATH = os.path.join(BASE_DIR, "airlift/final_config.yaml")
FINAL_CLUSTER_CONFIG_FILE_PATH = os.path.join(BASE_DIR, "kind/final_cluster.yaml")
CHART_VERSION = "1.9.0"
CHART_REPO = "apache-airflow"
CHART_URL = "https://airflow.apache.org"
NAME = "airlift"
DEFAULT_DOCKERFILE_PATH = os.path.join(BASE_DIR, "docker/Dockerfile")
FINAL_DOCKERFILE_PATH = os.path.join(BASE_DIR, "docker/final/Dockerfile")
DEFAULT_DOCKER_IMAGE = "apache/airflow:2.3.2-python3.7"
DEFAULT_WEBSERVER_PORT = 8080
DEFAULT_USER = "admin"
