from airlift.utils.command import CommandUtils


class KubernetesUtils:
    @staticmethod
    def port_forward(
        service_name: str, source_port: int, target_port: int, namespace: str
    ):
        """
        Forwards the port of a service locally
        Args:
            service_name: The service name in Kubernetes
            source_port: The source port
            target_port: The target port
            namespace: The namespace the service is running under
        """
        command = f"kubectl port-forward service/{service_name} {source_port}:{target_port} -n {namespace}"
        status, stdoutdata, stderrdata = CommandUtils.run_command(command)
        if status != 0:
            raise RuntimeError(
                f"Failed to create cluster:\n{stdoutdata}\n\n{stderrdata}"
            )

    @staticmethod
    def get_logs(
        selector: str,
        selector_value: str,
        namespace: str,
        follow: bool = False,
        tail_lines: int = -1,
    ):
        """
        Gets all logs for a pod(s), given a selector label and value. Optionally tails the logs
        Args:
            selector_value: The selector value to filter events for
            selector: The selector label to filter events for
            namespace: The namespace where the pod(s) are
            follow: Whether or not to follow the logs and stream them to stdout
            tail_lines: If not using follow, the number of lines to pull from the pod

        Raises:
            RuntimeError: Raises a runtime error if unable to get the logs

        Returns: The stdoutdata from the command, if not streaming. Otherwise, a standard success message

        """
        command = f"kubectl logs --prefix -l {selector}={selector_value} -n {namespace} {'--follow' if follow else ''} {'--tail='+ str(tail_lines) if not follow else ''}".rstrip(
            " "
        ).replace(
            "  ", " "
        )
        status, stdoutdata, stderrdata = CommandUtils.run_command(command, follow)
        if status != 0:
            raise RuntimeError(f"Failed to get logs:\n{stdoutdata}\n\n{stderrdata}")
        return stdoutdata

    @staticmethod
    def get_events(selector: str, selector_value: str, namespace: str) -> str:
        """
        Gets all the events for a pod, given a selector label and value
        Args:
            selector_value: The selector value to filter events for.
            selector: The selector label to filter events for
            namespace: The namespace of the pod

        Raises:
            RuntimeError: Raises a runtime error if unable to get the events

        Returns: The lines of text after the `Events` field in the K8S describe command.

        """
        command = f"kubectl describe pod --selector {selector}={selector_value} -n {namespace}".replace(
            "  ", " "
        )

        status, stdoutdata, stderrdata = CommandUtils.run_command(command)
        if status != 0:
            raise RuntimeError(f"Failed to get events:\n{stdoutdata}\n\n{stderrdata}")

        lines = stdoutdata.split("\n")
        for idx, line in enumerate(lines):
            if "Events" in line:
                return "\n" + "\n".join(lines[idx + 1 :])
        return ""
