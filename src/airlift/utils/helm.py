from airlift.utils.command import CommandUtils


class HelmUtils:
    @staticmethod
    def install(
        namespace: str,
        version: str,
        chart_repo: str,
        values_file_path: str = None,  # pyright: ignore
        value_overrides: list[str] = [],
    ) -> None:
        """
        Installs a helm chart on a Kubernetes cluster
        Args:
            namespace: The namespace to install under
            version: The version of the chart to install
            chart_repo: The repo name for the chart
            values_file_path: Any override values.yaml file
            value_overrides: Any --set params to append to the command
        """
        command = f"helm upgrade --install airflow {chart_repo}/airflow --version {version} --namespace {namespace} --create-namespace --values {values_file_path}{' --set '.join(value_overrides)}"
        status, stdoutdata, stderrdata = CommandUtils.run_command(command)
        if status != 0:
            raise RuntimeError(
                f"Failed to install helm chart:\n{stdoutdata}\n\n{stderrdata}"
            )

    @staticmethod
    def add_repo(repo_name: str, chart_url: str) -> None:
        """
        Adds a helm repo.
        Args:
            repo_name: The repo name to add
            chart_url: The chart URL for the repo.
        """
        command = f"helm repo add {repo_name} {chart_url}"
        status, stdoutdata, stderrdata = CommandUtils.run_command(command)
        if status != 0:
            raise RuntimeError(
                f"Failed to add helm repo:\n{stdoutdata}\n\n{stderrdata}"
            )
