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
