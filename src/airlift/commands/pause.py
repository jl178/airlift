from halo import Halo
import logging
from airlift.utils.docker import DockerUtils
from airlift.config.config import NAME


def pause_container():
    """Pauses the Airlift service"""
    with Halo(text=f"Pausing Service", spinner="dots") as spinner:
        spinner.start()
        try:
            DockerUtils.pause(NAME + "-control-plane")
        except RuntimeError as e:
            spinner.fail()
            logging.error(str(e))
            exit(1)
        spinner.succeed()


def unpause_container():
    """Unpauses the Airlift service"""
    with Halo(text=f"Unpausing Service", spinner="dots") as spinner:
        spinner.start()
        try:
            DockerUtils.unpause(NAME + "-control-plane")
        except RuntimeError as e:
            spinner.fail()
            logging.error(str(e))
            exit(1)
        spinner.succeed()


def pause(args):
    pause_container()


def unpause(args):
    unpause_container()
