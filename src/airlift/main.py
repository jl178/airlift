"""
This is the `airlift` CLI which can be used to spin up a local Airflow environment for development & testing.
It uses Helm and Kind underneath the hood to spin up the service. run `airlift -h` to get started 
"""

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from airlift.commands.run_dag import run_dag
from airlift.config.config import (
    DEFAULT_AIRLIFT_CONFIG_FILE,
    FINAL_CONFIG_VALUES_FILE_PATH,
    FINAL_DOCKERFILE_PATH,
    FINAL_HELM_VALUES_FILE_PATH,
    FINAL_CLUSTER_CONFIG_FILE_PATH,
)


import argparse
from airlift.commands.remove import remove
from airlift.commands.status import status
from airlift.commands.pause import pause, unpause
from airlift.utils.parser import ParserUtils
import logging
from airlift.commands.import_variables import import_variables
from airlift.commands.start import start
from airlift.commands.check import check
from airlift.utils.file import FileUtils
from dotmap import DotMap
from airlift.utils.airlift import AirliftUtils


def set_logger(level: str):
    """
    Sets the logging level
    Args:
        level: The level to log at
    """
    logging.basicConfig(format="%(levelname)s: %(message)s", level=level)


def get_args(parser_utils: ParserUtils) -> DotMap:
    """
    Parses the command line arguments & merges them with the Airlift config file.
    Args:
        parser_utils: The parser utilities which contain the arguments & argparse parser

    Returns: A DotMap which has the command line arguments

    """
    args = parser_utils.get_parsed_args()
    args = DotMap(args)
    if args.airlift_config_file:
        AirliftUtils.create_config_file(
            DEFAULT_AIRLIFT_CONFIG_FILE,
            args.airlift_config_file,
            FINAL_CONFIG_VALUES_FILE_PATH,
        )
        airlift_config = FileUtils.yaml_to_dict(FINAL_CONFIG_VALUES_FILE_PATH)
        dict_args = args.toDict()
        dict_args.update(airlift_config)
        args = DotMap(dict_args)
    if args.subcommand == "start":
        args.extra_volume_mounts = parser_utils.convert_list_of_dicts(
            args.extra_volume_mounts
        )
    return args


def cleanup():
    """
    Removes all files created via Airlift
    """
    FileUtils.remove_file(FINAL_CLUSTER_CONFIG_FILE_PATH)
    FileUtils.remove_file(FINAL_CONFIG_VALUES_FILE_PATH)
    FileUtils.remove_file(FINAL_HELM_VALUES_FILE_PATH)
    FileUtils.remove_file(FINAL_DOCKERFILE_PATH)


def main(args=None):
    """
    Entrypoint
    """
    cleanup()
    parser = argparse.ArgumentParser(
        prog="airlift",
        description=__doc__,
        epilog="See README.md for more info and examples.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser_utils = ParserUtils(args, parser)
    args = get_args(parser_utils)
    set_logger(args.log_level)
    if args.subcommand == "start":
        check()
        start(args)
    elif args.subcommand == "check":
        check()
    elif args.subcommand == "pause":
        pause(args)
    elif args.subcommand == "unpause":
        unpause(args)
    elif args.subcommand == "remove":
        remove()
    elif args.subcommand == "status":
        status(args, 0)
    elif args.subcommand == "import_variables":
        import_variables(args)
    elif args.subcommand == "run_dag":
        run_dag(args)
    else:
        logging.error(
            f"Invalid command {args.subcommand}. Run `airlift -h` for a list of valid commands"
        )
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
