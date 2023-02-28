"""SQLITE operations for targets and results"""
import sqlite3
import datetime
import validators

DATABASE = "pinger.db"
connection = sqlite3.connect(DATABASE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS target (
                _id text unique,
                address text,
                rtt_limit integer,
                must_include text
                )"""
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS results (
                _id text,
                passed integer,
                rtt integer,
                content_found integer, 
                time timestamp
                )"""
)


def create_target(target_id, address, rtt_limit, must_include):
    """Add new target to DB"""
    try:
        assert validators.url(address), "Not a valid URL!"
        assert rtt_limit.isnumeric(), "RTT limit must be numeric!"
    except AssertionError as err:
        raise ValueError(f"Following target information incorrect: {err}") from err
    with connection:
        try:
            connection.execute(
                "INSERT INTO target VALUES (:_id, :address, :rtt_limit, :must_include)",
                {
                    "_id": target_id,
                    "address": address,
                    "rtt_limit": rtt_limit,
                    "must_include": must_include,
                },
            )
        except sqlite3.IntegrityError as err:
            raise sqlite3.IntegrityError(
                "Target with the same id already exists"
            ) from err


def remove_target(target_id):
    """Remove single target and its results from DB"""
    with connection:
        connection.execute("DELETE from target WHERE _id = :_id", {"_id": target_id})
        connection.execute("DELETE from results WHERE _id = :_id", {"_id": target_id})


def find_all_targets():
    """Fetch all targets from DB"""
    targets = []
    cursor.execute("SELECT * FROM target")
    for entry in cursor.fetchall():
        targets.append(dict(entry))
    return targets


def add_result(target_id, passed, rtt, fail_reason):
    """Add test reulst to DB"""
    with connection:
        connection.execute(
            "INSERT INTO results VALUES (:_id, :passed, :rtt, :content_found, :time)",
            {
                "_id": target_id,
                "passed": passed,
                "rtt": rtt,
                "content_found": fail_reason,
                "time": datetime.datetime.now(),
            },
        )


def find_results_by_target(target_id, failed=False):
    """Find all test results (optionally only failed ones) for single target"""
    results = []
    if failed:
        cursor.execute(
            "SELECT * FROM results WHERE _id = :_id AND passed = 0", {"_id": target_id}
        )
    else:
        cursor.execute("SELECT * FROM results WHERE _id = :_id", {"_id": target_id})
    for entry in cursor.fetchall():
        results.append(dict(entry))
    return results
