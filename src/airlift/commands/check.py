import logging
from airlift.config.config import REQUIRED_SOFTWARE_PATH
import yaml
import subprocess
from halo import Halo


def check_installs():
    """Checks all required installs and fails if they don't exist on the host machine"""
    logging.debug("Checking pre-requisite installs")
    with open(REQUIRED_SOFTWARE_PATH, "r") as stream:
        required_software = yaml.safe_load(stream)
        for key in required_software:
            with Halo(text=f"Checking `{key}` installation", spinner="dots") as spinner:
                logging.debug(f"Running command {required_software[key]}")
                spinner.start()
                process = subprocess.Popen(
                    required_software[key].split(" "),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                stdoutdata, stderrdata = process.communicate()
                status = process.returncode
                logging.info(f"Command returned status code of: {status}")
                if status != 0:
                    spinner.fail()
                    logging.error(f"Failed to find command for `{key}`")
                    logging.error(stdoutdata.decode("unicode-escape").lstrip("\n"))
                    exit(1)
                else:
                    spinner.succeed()


def check():
    check_installs()
