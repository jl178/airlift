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
        import logging

        command = f"kubectl logs --prefix -l {selector}={selector_value} -n {namespace} {'--follow' if follow else ''} {'--tail='+ str(tail_lines) if not follow else ''}".rstrip(
            " "
        )
        logging.error(command)
        status, stdoutdata, stderrdata = CommandUtils.run_command(command, follow)
        if status != 0:
            raise RuntimeError(f"Failed to get logs:\n{stdoutdata}\n\n{stderrdata}")
        return stdoutdata

    @staticmethod
    def get_events(selector: str, selector_value, namespace: str) -> str:
        command = f"kubectl describe pod --selector {selector}={selector_value} -n {namespace} | grep -A20 Events"
        status, stdoutdata, stderrdata = CommandUtils.run_command(command)
        if status != 0:
            raise RuntimeError(f"Failed to get events:\n{stdoutdata}\n\n{stderrdata}")
        return stdoutdata
