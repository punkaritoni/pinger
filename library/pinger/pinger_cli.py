"""CLI tool for testing targets"""
import sys
import argparse
import signal
from .pinger import get_all_targets, monitor
from .db import create_target, remove_target, find_results_by_target

def handler(signum, frame):
    """Handle ctrl+c silently"""
    del signum, frame
    print("Good bye!")
    sys.exit(1)

def list_targets():
    """List all targets"""
    targets = get_all_targets()
    if not targets:
        print("You don't yet have any targets configured!")
    else:
        for target in targets:
            print(f"{target}\n")


def add_target():
    """Add new target"""
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name or ID to identify target")
    parser.add_argument("url", help="URL used for testing. Format: https://abc.com")
    parser.add_argument("limit", help="RTT limit in milliseconds (int)")
    parser.add_argument("include", help="String that must be included in URL.")
    args = parser.parse_args()
    create_target(args.name, args.url, args.limit, args.include)


def delete_target():
    """Delete existing target"""
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name or ID to identify target")
    args = parser.parse_args()
    remove_target(args.name)


def show_results():
    """Show all results by target id. Optinally show only failed results"""
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name or ID to identify target")
    parser.add_argument(
        "-f", "--failed", help="Name or ID to identify target", action="store_false"
    )
    args = parser.parse_args()
    results = find_results_by_target(args.name, args.failed)
    for result in results:
        print(result)


def monitor_all():
    """Periodically execute testing for all targets"""
    monitor()

signal.signal(signal.SIGINT, handler)

if __name__ == "__main__":
    globals()[sys.argv[1]]()
