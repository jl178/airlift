import logging
from halo import Halo
from airlift.config.config import DEFAULT_USER
from airlift.utils.airflow import AirflowUtils
import time


def run_dag(args):
    """
    Runs an Airflow DAG
    Args:
        args (): The command line arguments
    """
    with Halo(
        text=f"Triggering DAG `{args.post_start_dag_id}`", spinner="dots"
    ) as spinner:
        spinner.start()
        retries = 0
        error = None
        while retries <= int(args.dag_trigger_retries):
            try:
                AirflowUtils.run_dag(
                    "localhost",
                    args.port,
                    username=DEFAULT_USER,
                    password=DEFAULT_USER,
                    dag_id=args.post_start_dag_id,
                )
                spinner.succeed()
                return
            except Exception as e:
                error = e
                logging.warning(str(e))
                retries += 1
                time.sleep(int(args.dag_trigger_retry_wait))
        if retries >= int(args.dag_trigger_retries):
            spinner.fail()
            logging.error(str(error))
            exit(1)
