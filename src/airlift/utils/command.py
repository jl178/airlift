import subprocess
import logging
import sys


class CommandUtils:
    @staticmethod
    def run_command(command: str, stream_output: bool = False) -> tuple[int, str, str]:
        """
        Runs a CLI command.
        Args:
            command: The command to execute at the console

        Returns: The return code, the stdout data, and the stderr data

        """
        if stream_output:
            CommandUtils._stream_command(command)
            return (0, "Logs streamed successfully", "")
        else:
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

    @staticmethod
    def _stream_command(command: str) -> None:
        """
        Streams a commands output to stdout until a keyboard interrupt is received.
        Args:
            command: The command to run in the terminal
        """
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        try:
            for line in process.stdout:  # pyright: ignore
                sys.stdout.write(line.decode("utf-8"))
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received.")
