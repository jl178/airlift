from halo import Halo
import logging
from airlift.utils.docker import DockerUtils
from airlift.utils.kind import KindUtils
from airlift.config.config import NAME


def delete_cluster():
    """
    Deletes the Airlift cluster
    """
    with Halo(text=f"Deleting Cluster", spinner="dots") as spinner:
        logging.info(f"Running delete cluster command")
        spinner.start()
        try:
            if not KindUtils.cluster_exists(NAME):
                raise RuntimeError(f"Cluster {NAME} does not exist")
            KindUtils.delete_cluster(NAME)
        except RuntimeError as e:
            spinner.fail()
            logging.error(str(e))
            exit(1)
        spinner.succeed()


def remove_image():
    """Removes the Airlift docker image"""
    with Halo(text=f"Removing Image", spinner="dots") as spinner:
        logging.info(f"Running remove image command")
        spinner.start()
        try:
            DockerUtils.remove_image(NAME)
        except RuntimeError as e:
            spinner.fail()
            logging.error(str(e))
            exit(1)
        spinner.succeed()


def remove():
    delete_cluster()
    remove_image()
