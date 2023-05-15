import argparse
from airlift.config.config import (
    CHART_VERSION,
    DEFAULT_DOCKERFILE_PATH,
    DEFAULT_DOCKER_IMAGE,
    DEFAULT_WEBSERVER_PORT,
)


class ParserUtils:
    def __init__(self, args, parser: argparse.ArgumentParser):
        self.args = args
        self.parser = parser
        self.subparser = parser.add_subparsers(dest="subcommand")
        self.__add_parser_args()
        self.__add_start_parser()
        self.__add_check_parser()
        self.__add_pause_parser()
        self.__add_remove_parser()
        self.__add_status_parser()
        self.__add_unpause_parser()
        self.__add_import_variables_parser()
        self.__add_run_dag_parser()

    def convert_list_of_dicts(self, values):
        list_vals = []
        for entry in values:
            dict_vals = {}
            for kv in entry.split(","):
                k, v = kv.split("=")
                dict_vals[k] = v
            list_vals.append(dict_vals)
        return list_vals

    def __add_parser_args(self) -> None:
        self.parser.add_argument("-l", "--log_level", default="ERROR")

    def __add_start_parser(self) -> None:
        start = self.subparser.add_parser(
            "start", description="Starts the Airflow service"
        )
        start.add_argument(
            "-d",
            "--dag_path",
            required=False,
            help="The ABSOLUTE path to the DAGs on your local machine. Mounted directly to the pod in the service for hot-reloading.",
        )
        start.add_argument(
            "-p",
            "--plugin_path",
            required=False,
            help="Optional ABSOLUTE path to plugins on your local machine. Mounted directly to the pod in the service for hot-reloading.",
        )
        start.add_argument(
            "-r",
            "--requirements_file",
            default=None,
            required=False,
            help="Optional path to the `requirements.txt` file which will be installed on the Airflow pod.",
        )
        start.add_argument(
            "-hf",
            "--helm_values_file",
            help="Optional ABSOLUTE path to a `values.yaml` file, which overrides default configs. Schema can be found here: https://github.com/airflow-helm/charts/blob/main/charts/airflow/values.yaml",
        )
        start.add_argument(
            "-v",
            "--helm_value",
            action="append",
            default=[],
            help="Optional list of values which override Helm values. Use this when you don't want to use a static file, like when adding credentials to connect to an external DB. Formatted as `attribute.subattribute=VALUE`",
        )
        start.add_argument(
            "-V",
            "--variables_file",
            help="ABSOLUTE path to a `variables.json` file which will be imported to Airflow after the service starts",
        )
        start.add_argument(
            "-c",
            "--airlift_config_file",
            help="Config file for airlift settings. See README.md in `config/airlift` for more details",
        )
        start.add_argument(
            "-m",
            "--extra_volume_mounts",
            action="append",
            default=[],
            help="Any extra volume mounts you wanted added to the container. For example, when mounting credentials to external cloud providers, like `.aws/`.",
        )
        start.add_argument(
            "-C",
            "--cluster_config_file",
            help="Optional cnfiguration file for the `kind` cluster.",
        )
        start.add_argument(
            "-ip",
            "--image_path",
            default=DEFAULT_DOCKERFILE_PATH,
            help="The path to the base image for the Dockerfile, if used.",
        )
        start.add_argument(
            "-i",
            "--image",
            default=DEFAULT_DOCKER_IMAGE,
            help=f"The base Docker image. Ignored if DEFAULT_DOCKERFILE_PATH is provided. Defaults to {DEFAULT_DOCKER_IMAGE}",
        )
        start.add_argument(
            "-hc",
            "--helm_chart_version",
            default=CHART_VERSION,
            help=f"The default Helm chart version. Defaults to {CHART_VERSION}.",
        )
        start.add_argument(
            "-P",
            "--port",
            default=DEFAULT_WEBSERVER_PORT,
            help=f"Override the default port exposed locally. Defaults to {DEFAULT_WEBSERVER_PORT}",
        )
        start.add_argument(
            "-D",
            "--post_start_dag_id",
            help="The DAG ID to run post service start. Helpful when you need to bootstrap the service with a DAG execution.",
        )
        start.add_argument(
            "-Dr",
            "--dag_trigger_retries",
            help="How many times to retry the DAG trigger operation. Time can vary between DAGs becoming available for execution in the UI. Defaults to 3.",
            default=3,
        )
        start.add_argument(
            "-Dw",
            "--dag_trigger_retry_wait",
            help="How long to wait before re-triggering the DAG in Airflow. Defaults to 10 seconds.",
            default=10,
        )
        start.add_argument(
            "-sr",
            "--status_retries",
            help="How many times to retry the service connection before failing. Defaults to 2.",
            default=2,
        )

    def __add_check_parser(self) -> None:
        self.subparser.add_parser(
            "check", description="Checks all pre-requisite software is installed"
        )

    def __add_pause_parser(self) -> None:
        self.subparser.add_parser("pause", description="Pauses the Airflow service")

    def __add_unpause_parser(self) -> None:
        self.subparser.add_parser("unpause", description="Unpauses the Airflow service")

    def __add_remove_parser(self) -> None:
        self.subparser.add_parser(
            "remove",
            description="Removes all containers/clusters related to the `airlift` service.",
        )

    def __add_status_parser(self) -> None:
        status = self.subparser.add_parser(
            "status",
            description="Checks the status of the service and whether or not it is reachable.",
        )
        status.add_argument(
            "-P",
            "--port",
            default=DEFAULT_WEBSERVER_PORT,
            help=f"The port to check the webserver on. Defaults to {DEFAULT_WEBSERVER_PORT}",
        )
        status.add_argument(
            "-sr",
            "--status_retries",
            help="How many times to retry the service connection before failing. Defaults to 2.",
            default=2,
        )

    def __add_import_variables_parser(self) -> None:
        import_variables = self.subparser.add_parser(
            "import_variables",
            description="Imports a `variables.json` file to a running Airflow instance.",
        )
        import_variables.add_argument(
            "-P",
            "--port",
            default=DEFAULT_WEBSERVER_PORT,
            help=f"The port the webserver is running on. Defaults to {DEFAULT_WEBSERVER_PORT}",
        )
        import_variables.add_argument(
            "-V",
            "--variables_file",
            help="ABSOLUTE path to a `variables.json` file which will be imported.",
        )

    def __add_run_dag_parser(self) -> None:
        run_dag = self.subparser.add_parser(
            "run_dag", description="Runs a DAG given an ID"
        )
        run_dag.add_argument(
            "-P",
            "--port",
            default=DEFAULT_WEBSERVER_PORT,
            help=f"The port the webserver is running on. Defaults to {DEFAULT_WEBSERVER_PORT}",
        )
        run_dag.add_argument(
            "-D",
            "--post_start_dag_id",
            help="The DAG ID to run.",
        )
        run_dag.add_argument(
            "-Dr",
            "--dag_trigger_retries",
            help="How many times to retry the DAG trigger operation. Time can vary between DAGs becoming available for execution in the UI. Defaults to 3.",
            default=3,
        )
        run_dag.add_argument(
            "-Dw",
            "--dag_trigger_retry_wait",
            help="How long to wait before re-triggering the DAG in Airflow. Defaults to 10 seconds.",
            default=10,
        )

    def get_parsed_args(self):
        args = self.parser.parse_args(self.args)
        return {tup[0]: tup[1] for tup in args._get_kwargs()}
