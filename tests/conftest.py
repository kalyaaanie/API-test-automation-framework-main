"""Shared fixtures.

By default the suite runs against the local mock server (deterministic, no
network needed). Set API_BASE_URL to run against any other deployment, e.g.:

    API_BASE_URL=https://jsonplaceholder.typicode.com pytest

Note: jsonplaceholder does not validate input, so the negative (4xx) cases are
expected to fail against it. That is a limitation of that fake API.
"""

import os
import threading

import pytest
from werkzeug.serving import make_server

from mock_server.app import create_app
from utils.api_client import APIClient


@pytest.fixture(scope="session")
def base_url():
    external = os.getenv("API_BASE_URL")
    if external:
        yield external.rstrip("/")
        return

    server = make_server("127.0.0.1", 0, create_app())  # port 0 = any free port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)


@pytest.fixture(scope="session")
def api_client(base_url):
    return APIClient(base_url)
