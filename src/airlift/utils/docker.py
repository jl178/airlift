from airlift.utils.command import CommandUtils


class DockerUtils:
    @staticmethod
    def build(dockerfile_path: str, tag: str) -> None:
        """
        Builds a Docker image
        Args:
            dockerfile_path: The path to the Dockerfile
            tag: The tag to tag the image with
        """
        command = f"docker build {dockerfile_path} -t {tag}"
        status, stdoutdata, stderrdata = CommandUtils.run_command(command)
        if status != 0:
            raise RuntimeError(f"Failed to build image:\n{stdoutdata}\n\n{stderrdata}")

    @staticmethod
    def remove_image(image_name: str, tag: str = "latest"):
        """
        Removes a Docker Image
        Args:
            image_name: The image name to remove
            tag: The image tag to remove. Defaults to latest
        """
        command = f"docker image rm {image_name}:{tag}"
        status, stdoutdata, stderrdata = CommandUtils.run_command(command)
        if status != 0:
            raise RuntimeError(f"Failed to delete image:\n{stdoutdata}\n\n{stderrdata}")

    @staticmethod
    def pause(container_name: str):
        """
        Pauses a Docker container
        Args:
            container_name: The name of the container to pause
        """
        command = f"docker pause {container_name}"
        status, stdoutdata, stderrdata = CommandUtils.run_command(command)
        if status != 0:
            raise RuntimeError(
                f"Failed to pause container:\n{stdoutdata}\n\n{stderrdata}"
            )

    @staticmethod
    def unpause(container_name: str):
        """
        Unpauses a docker container
        Args:
            container_name: The container name to unpause
        """
        command = f"docker unpause {container_name}"
        status, stdoutdata, stderrdata = CommandUtils.run_command(command)
        if status != 0:
            raise RuntimeError(
                f"Failed to unpause container:\n{stdoutdata}\n\n{stderrdata}"
            )
