from dotmap import DotMap
import logging
from halo import Halo
from airlift.utils.airflow import AirflowUtils
from airlift.config.config import DEFAULT_USER
from airlift.utils.file import FileUtils
import json


def import_variables(args: DotMap):
    """
    Imports the Airflow Variables
    Args:
        args: The command line args
    """
    with Halo(text=f"Importing Airflow Variables", spinner="dots") as spinner:
        logging.debug(f"Importing variables")
        spinner.start()
        try:
            data = FileUtils.read_file(args.variables_file)
            data = json.loads(data)
            for key in data:
                AirflowUtils.import_variable(
                    "localhost",
                    args.port,
                    DEFAULT_USER,
                    DEFAULT_USER,
                    key,
                    json.dumps(data[key]),
                )
        except Exception as e:
            spinner.fail()
            logging.error(str(e))
            exit(1)
        spinner.succeed()
