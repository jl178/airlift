from halo import Halo
import logging
from airlift.utils.kubernetes import KubernetesUtils
from airlift.config.config import NAME
import sys


def get_logs(args):
    """
    Gets logs from the Airlift cluster
    """
    prompt = f"Getting logs for {args.component}" if not args.follow else ""
    with Halo(text=prompt, spinner="dots") as spinner:
        spinner.start()
        try:
            logs = KubernetesUtils.get_logs(
                selector=args.selector,
                selector_value=args.component,
                namespace=NAME,
                tail_lines=args.tail,
                follow=args.follow,
            )
            sys.stdout.write(logs)
        except RuntimeError as e:
            spinner.fail()
            logging.error(str(e))
            exit(1)
        spinner.succeed()


def get_events(args):
    """
    Gets the events from the Airlift cluster
    """
    with Halo(text=f"Getting Events for {args.component}", spinner="dots") as spinner:
        spinner.start()
        try:
            logs = KubernetesUtils.get_events(
                selector=args.selector,
                selector_value=args.component,
                namespace=NAME,
            )
            sys.stdout.write(logs)
        except RuntimeError as e:
            spinner.fail()
            logging.error(str(e))
            exit(1)
        spinner.succeed()


def logs(args):
    """
    Entrypoint for the logs command
    """
    if args.events:
        get_events(args)
    else:
        get_logs(args)
