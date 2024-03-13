import logging
from dotmap import DotMap
from airlift.commands.import_variables import import_variables
from airlift.commands.run_dag import run_dag
from airlift.config.config import (
    NAME,
    DEFAULT_DOCKERFILE_PATH,
    FINAL_DOCKERFILE_PATH,
    CHART_REPO,
    CHART_URL,
    DEFAULT_CLUSTER_CONFIG_FILE,
    DEFAULT_HELM_CONFIG_FILE,
    FINAL_CLUSTER_CONFIG_FILE_PATH,
    FINAL_HELM_VALUES_FILE_PATH,
)
from airlift.utils.docker import DockerUtils
from airlift.utils.file import FileUtils
from halo import Halo
from airlift.utils.helm import HelmUtils
import yaml
from airlift.utils.kind import KindUtils
from airlift.commands.status import status
import os


def check_plugin_path(path: str):
    """
    Checks the Airflow plugins path for a venv folder, since it could cause scheduler issues.
    Args:
        path: the path to the plugins
    """
    if not os.path.exists(path):
        logging.warning(f"The path '{path}' does not exist.")
        return

    all_entries = os.listdir(path)
    # Filter the list to include only directories
    folders = [
        entry for entry in all_entries if os.path.isdir(os.path.join(path, entry))
    ]
    found = ["venv" in folder for folder in folders]

    if True in found:
        logging.warning(
            f"plugin_path contains a potential `venv` folder. This can have impact on the Airflow scheduler and may cause it not to function: {path}. It is recommended to move your virtual environment to a different folder."
        )


def generate_configs(args: DotMap):
    """
    Generates all the final config files for airlift
    Args:
        args: The command line args
    """
    logging.info("Generating Config Files")
    with Halo(text="Generating Config Files", spinner="squareCorners") as spinner:
        spinner.start()
        try:
            config_dict = [
                {
                    "merge_yaml": True,
                    "default_file_path": DEFAULT_HELM_CONFIG_FILE,
                    "final_file_path": FINAL_HELM_VALUES_FILE_PATH,
                    "override_data_path": args.helm_values_file,
                },
                {
                    "merge_yaml": True,
                    "default_file_path": DEFAULT_CLUSTER_CONFIG_FILE,
                    "final_file_path": FINAL_CLUSTER_CONFIG_FILE_PATH,
                    "override_data_path": args.cluster_config_file,
                },
                {
                    "merge_yaml": False,
                    "default_file_path": args.image_path,
                    "final_file_path": FINAL_DOCKERFILE_PATH,
                },
            ]
            for entry in config_dict:
                template = FileUtils.render_jinja(
                    file_path=entry["default_file_path"],
                    dag_path=args.dag_path,
                    plugin_path=args.plugin_path,
                    requirements_path=args.requirements_file,
                    base_image=args.image,
                    port=args.port,
                    extra_volume_mounts=args.extra_volume_mounts,
                )
                FileUtils.write_file(entry["final_file_path"], template)
                if entry["merge_yaml"] and entry["override_data_path"] is not None:
                    final_data = FileUtils.merge_yaml(
                        original_data=entry["final_file_path"],
                        override_data=entry["override_data_path"],
                    )
                    with open(entry["final_file_path"], "w+") as file:
                        yaml.dump(
                            final_data, file, default_flow_style=False, sort_keys=False
                        )
                else:
                    final_data = template
                    FileUtils.write_file(entry["final_file_path"], final_data)
                logging.debug(
                    f"Final Config File for {entry['default_file_path']}: \n{final_data}"
                )
            spinner.succeed()
        except Exception as e:
            spinner.fail()
            logging.error(f"Failed to generate config files due to error: {str(e)}")
            exit(1)


def create_cluster(args):
    """
    Creates the Kind cluster for Airlift

    """
    with Halo(text=f"Creating Cluster", spinner="dots") as spinner:
        logging.info(f"Running create cluster command")
        spinner.start()
        try:
            if not KindUtils.cluster_exists(NAME):
                KindUtils.create_cluster(NAME, FINAL_CLUSTER_CONFIG_FILE_PATH)
            else:
                spinner.info("Cluster Already Exists")
                logging.debug(f"Cluster already exists: {NAME}. Not creating.")
                return
            if args.dns_servers is not None:
                logging.info("Adding DNS servers to cluster")
                KindUtils.add_dns_servers(args.dns_servers)
        except RuntimeError as e:
            spinner.fail()
            logging.error(str(e))
            exit(1)
        spinner.succeed()


def load_image_to_cluster():
    """Loads the Airlift image to the Kind cluster"""
    with Halo(text=f"Importing Image to Cluster", spinner="dots") as spinner:
        logging.info(f"Running import image for kind cluster")
        spinner.start()
        try:
            KindUtils.load_image(NAME, NAME + ":latest")
        except RuntimeError as e:
            spinner.fail()
            logging.error(str(e))
            exit(1)
        spinner.succeed()


def build_image(args: DotMap):
    """
    Builds the Airlift docker image
    Args:
        args: The command line args
    """
    with Halo(text=f"Building Base Docker Image", spinner="dots") as spinner:
        logging.debug(f"Running docker build")
        spinner.start()
        split_path = FINAL_DOCKERFILE_PATH.split("/")
        requirements_path = "/".join(split_path[:-1]) + "/requirements.txt"
        try:
            if args.requirements_file is not None:
                FileUtils.copy_file(args.requirements_file, requirements_path)
            DockerUtils.build(
                "/".join(split_path[:-1])
                if args.image_path == DEFAULT_DOCKERFILE_PATH
                else args.image_path,
                NAME,
            )
            FileUtils.remove_file(requirements_path)
        except RuntimeError as e:
            spinner.fail()
            logging.error(str(e))
            exit(1)
        spinner.succeed()


def install_chart(args: DotMap):
    """
    Installs the Airflow helm chart
    Args:
        args: The command line args
    """
    with Halo(text=f"Starting Airflow Service", spinner="dots") as spinner:
        logging.debug(f"Installing Airflow Service")
        spinner.start()
        try:
            HelmUtils.add_repo(CHART_REPO, CHART_URL)
            HelmUtils.install(
                chart_repo=CHART_REPO,
                namespace=NAME,
                values_file_path=FINAL_HELM_VALUES_FILE_PATH,
                version=args.helm_chart_version,
                value_overrides=args.helm_value,
            )
        except RuntimeError as e:
            spinner.fail()
            logging.error(str(e))
            exit(1)
        spinner.succeed()
        logging.info("Installed Helm chart.")


def start(args: DotMap):
    """
    Starts the Airlift service
    Args:
        args: The command line args
    """
    if args.plugin_path:
        check_plugin_path(args.plugin_path)
    generate_configs(args)
    build_image(args)
    create_cluster(args)
    load_image_to_cluster()
    install_chart(args)
    status(args, 20)
    if args.variables_file is not None:
        import_variables(args)
    if args.post_start_dag_id is not None:
        run_dag(args)
