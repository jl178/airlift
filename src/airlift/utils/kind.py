from airlift.utils.command import CommandUtils


class KindUtils:
    @staticmethod
    def cluster_exists(cluster_name: str) -> bool:
        """
        Checks if a cluster already exists
        Args:
            cluster_name: The name of the cluster

        Returns: If the cluster already exists

        """
        status, stdoutdata, stderrdata = CommandUtils.run_command("kind get clusters")
        if status != 0:
            raise RuntimeError(
                f"Failed to get cluster status:\n{stdoutdata}\n\n{stderrdata}"
            )

        lines = stdoutdata.split("\n")
        for line in lines:
            if cluster_name == line.strip("\n"):
                return True
        return False

    @staticmethod
    def create_cluster(name: str, cluster_config_path: str) -> None:
        """
        Creates a cluster
        Args:
            name: The name of the cluster
            cluster_config_path: The path to the YAML config for the cluster
        """
        command = f"kind create cluster --config {cluster_config_path} --name {name}"
        status, stdoutdata, stderrdata = CommandUtils.run_command(command)
        if status != 0:
            raise RuntimeError(
                f"Failed to create cluster:\n{stdoutdata}\n\n{stderrdata}"
            )

    @staticmethod
    def delete_cluster(name: str) -> None:
        """
        Deletes a cluster
        Args:
            name: The name of the cluster to delete
        """
        command = f"kind delete cluster --name {name}"
        status, stdoutdata, stderrdata = CommandUtils.run_command(command)
        if status != 0:
            raise RuntimeError(
                f"Failed to delete cluster:\n{stdoutdata}\n\n{stderrdata}"
            )

    @staticmethod
    def load_image(cluster_name: str, image_name: str):
        """
        Loads a local docker image to a cluster
        Args:
            cluster_name: The cluster to load the image to
            image_name: The local docker image name to load to the cluster
        """
        command = f"kind --name {cluster_name} load docker-image {image_name}"
        status, stdoutdata, stderrdata = CommandUtils.run_command(command)
        if status != 0:
            raise RuntimeError(f"Failed to load image:\n{stdoutdata}\n\n{stderrdata}")
