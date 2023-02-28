"""Target class with methods"""
import requests
from .db import add_result


class Target:
    """class for testing target"""
    def __init__(
        self,
        target_id: str,
        address: str,
        rtt_limit: int,
        must_include: str,
    ):
        self.target_id = target_id
        self.address = address
        self.rtt_limit = rtt_limit
        self.must_include = must_include

    def __repr__(self) -> str:
        """string representation for Target object"""
        rep = f"""Target id: {self.target_id}\nURL address: {self.address}\n
        RTT limit: {self.rtt_limit}\nMust include: {self.must_include}"""
        return rep

    def test(self):
        """method for running RTT and content testing for Target"""
        response = requests.get(self.address, timeout=5)
        rtt = round(1000 * response.elapsed.total_seconds())
        content_found = self.must_include in response.text
        passed = content_found and rtt < self.rtt_limit
        add_result(self.target_id, passed, rtt, content_found)
        if passed:
            print(f"Status of {self.target_id}: passed\n")
        else:
            print(
                f"Status of {self.target_id}: failed\nRTT check:{rtt<self.rtt_limit}\n"
                f"Content found: {bool(content_found)}\n"
            )
