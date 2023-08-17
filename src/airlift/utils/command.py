import subprocess
import logging


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
            return (CommandUtils._stream_command(command), "", "")
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
    def _stream_command(command: str):
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            # Print stdout and stderr as they come in
            while True:
                output = process.stdout.readline()
                if output:
                    print(output.strip())
                error = process.stderr.readline()
                if error:
                    logging.error(error.strip())
                # Break the loop once process is done
                return_code = process.poll()
                if return_code is not None:
                    for output in process.stdout.readlines():
                        print(output.strip())
                    for error in process.stderr.readlines():
                        logging.error(error.strip())
                    break
            return return_code
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed with error: {e}")
            return e.returncode
