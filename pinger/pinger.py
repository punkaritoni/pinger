"""Generic functions for testing"""
from typing import List
import time
from .db import find_all_targets
from .target import Target


def get_all_targets() -> List[Target]:
    """Returns list of target objects"""
    targets = []
    for entry in find_all_targets():
        target = Target(
            entry["_id"], entry["address"], entry["rtt_limit"], entry["must_include"]
        )
        targets.append(target)
    return targets


def monitor():
    """Periodically executes testing for all targets"""
    targets = get_all_targets()
    while True:
        for target in targets:
            target.test()
        time.sleep(1)
