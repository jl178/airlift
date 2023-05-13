import logging
from halo import Halo
from airlift.config.config import DEFAULT_USER
from airlift.utils.airflow import AirflowUtils


def run_dag(args):
    """
    Runs an Airflow DAG
    Args:
        args (): The command line arguments
    """
    with Halo(
        text=f"Triggering DAG `{args.post_start_dag_id}`", spinner="dots"
    ) as spinner:
        logging.info(f"Running create cluster command")
        spinner.start()
        try:
            AirflowUtils.run_dag(
                "localhost",
                args.port,
                username=DEFAULT_USER,
                password=DEFAULT_USER,
                dag_id=args.post_start_dag_id,
            )
        except RuntimeError as e:
            spinner.fail()
            logging.error(str(e))
            exit(1)
        spinner.succeed()

    pass
