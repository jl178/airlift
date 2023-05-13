from requests.models import HTTPBasicAuth
from airlift.utils.command import CommandUtils
import requests
import json
from datetime import datetime


class AirflowUtils:
    @staticmethod
    def check_webserver_status(host: str = "http://localhost", port: int = 8080):
        """
        Checks the webserver status for Airflow
        Args:
            host: The host where Airflow is running. Defaults to localhost
            port: The port where Airflow is running. Defaults to 8080
        """
        command = f"curl {host}:{port} --connect-timeout 5 --max-time 5"
        status, stdoutdata, stderrdata = CommandUtils.run_command(command)
        if status != 0:
            raise RuntimeError(
                f"Failed to check service:\n{stdoutdata}\n\n{stderrdata}"
            )

    @staticmethod
    def import_variable(
        host: str, port: int, username: str, password: str, key: str, value: str
    ) -> None:
        """
        Given a key, value pair, import it to the Airflow Variables.
        Args:
            host: The host where Airflow is running
            port: The port where Airflow is running
            username: The username for Airflow
            password: The password for Airflow
            key: The key to store the variable under in Airflow
            value: The value of the Airflow variable
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = requests.post(
            auth=HTTPBasicAuth(username, password),
            headers=headers,
            url=f"http://{host}:{port}/api/v1/variables",
            data=json.dumps({"key": key, "value": value}),
        )
        response.raise_for_status()

    @staticmethod
    def run_dag(
        host: str, port: int, username: str, password: str, dag_id: str
    ) -> None:
        """
        Triggers a DAG Run for a given DAG on Airflow
        Args:
            host: The host where Airflow is running
            port:  The port where airflow is running
            username: The username for Airflow
            password: The password for Airflow
            dag_id: The DAG ID to trigger a run for.
        """
        AirflowUtils.unpause_dag(host, port, username, password, dag_id)
        date = datetime.utcnow().replace(microsecond=0).isoformat()
        data = {"dag_run_id": f"airlift_{date}"}
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = requests.post(
            auth=HTTPBasicAuth(username, password),
            headers=headers,
            data=json.dumps(data),
            url=f"http://{host}:{port}/api/v1/dags/{dag_id}/dagRuns",
        )
        response.raise_for_status()

    @staticmethod
    def unpause_dag(host: str, port: int, username: str, password: str, dag_id: str):
        """
        Unpauses a DAG from the Airflow UI
        Args:
            host: The host where Airflow is running
            port:  The port where Airflow is running
            username: Username for the Airflow service
            password: Password for the Airflow service
            dag_id: The DAG ID to unpause
        """
        data = {
            "is_paused": False,
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = requests.patch(
            auth=HTTPBasicAuth(username, password),
            headers=headers,
            data=json.dumps(data),
            url=f"http://{host}:{port}/api/v1/dags/{dag_id}",
        )
        response.raise_for_status()
