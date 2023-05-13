from airlift.utils.airflow import AirflowUtils
import logging
from halo import Halo
import time


def check_service_status(args, wait):
    """
    Checks the Airlift service status
    Args:
        args (): The command line args
        wait (): How long to sleep before checking the service
    """
    with Halo(
        text=f"Checking Webserver Status on Port {args.port}", spinner="dots"
    ) as spinner:
        spinner.start()
        time.sleep(wait)
        try:
            AirflowUtils.check_webserver_status(port=args.port)
        except RuntimeError as e:
            spinner.fail()
            logging.error(str(e))
            exit(1)
        spinner.succeed()


def status(args, wait=10):
    """
    Checks the status
    Args:
        args (): The command line args
        wait (): How long to sleep before checking the service
    """
    check_service_status(args, wait)
