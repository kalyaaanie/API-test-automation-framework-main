"""API client: executes a test case (dict) as an HTTP request."""

import os

import requests

DEFAULT_TIMEOUT = 10  # seconds


class APIClient:
    def __init__(self, base_url=None):
        self.base_url = (base_url or os.getenv("API_BASE_URL", "")).rstrip("/")

    def send_request(self, test_case):
        method = test_case["method"].upper()
        url = f"{self.base_url}{test_case['endpoint']}"

        # Only send a JSON body for methods that carry one
        body = test_case.get("body") if method in ("POST", "PUT", "PATCH") else None

        return requests.request(
            method=method,
            url=url,
            headers=test_case.get("headers") or {},
            params=test_case.get("query_params") or {},
            json=body,
            timeout=DEFAULT_TIMEOUT,
        )
