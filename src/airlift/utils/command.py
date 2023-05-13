import subprocess


class CommandUtils:
    @staticmethod
    def run_command(command: str) -> tuple[int, str, str]:
        """
        Runs a CLI command.
        Args:
            command: The command to execute at the console

        Returns: The return code, the stdout data, and the stderr data

        """
        process = subprocess.Popen(
            command.split(" "),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdoutdata, stderrdata = process.communicate()
        return (
            process.returncode,
            stdoutdata.decode("unicode-escape"),
            stderrdata.decode("unicode-escape"),
        )
