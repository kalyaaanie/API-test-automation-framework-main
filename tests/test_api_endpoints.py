"""Data-driven API tests.

Flow: load test cases -> send request -> validate response.

Test cases come from data/test_cases.json (a reviewed baseline). To generate
a fresh set with an LLM from the API specification, run:

    python -m utils.llm_test_generator

which rewrites data/generated_test_cases.json; the suite uses that file
automatically when it exists (see load_test_cases below).
"""

import json
import time
from pathlib import Path

import pytest

from utils.validators import ResponseValidator

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_test_cases():
    generated = DATA_DIR / "generated_test_cases.json"
    path = generated if generated.exists() else DATA_DIR / "test_cases.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


TEST_CASES = load_test_cases()


@pytest.mark.parametrize(
    "test_case", TEST_CASES, ids=[tc["test_name"] for tc in TEST_CASES]
)
def test_api_endpoints(api_client, test_case):
    start = time.perf_counter()
    response = api_client.send_request(test_case)
    response_time_ms = (time.perf_counter() - start) * 1000

    ResponseValidator.validate_status_code(response, test_case["expected_status_code"])
    ResponseValidator.validate_response_time(
        response_time_ms, test_case.get("max_response_time_ms", 2000)
    )
    ResponseValidator.validate_json_response(response)
    ResponseValidator.validate_headers(response)

    payload = response.json()

    if isinstance(payload, dict):
        if response.status_code in (200, 201):
            ResponseValidator.validate_required_fields(payload, ["id"])

        schema = {}
        for field, type_name in (
            ("id", "integer"),
            ("title", "string"),
            ("body", "string"),
            ("userId", "integer"),
        ):
            if field in payload:
                schema[field] = type_name
        if schema:
            ResponseValidator.validate_datatypes(payload, schema)

        ResponseValidator.validate_business_rules(payload)

    elif isinstance(payload, list):
        for item in payload:
            ResponseValidator.validate_required_fields(
                item, ["id", "title", "body", "userId"]
            )
            ResponseValidator.validate_datatypes(
                item,
                {"id": "integer", "title": "string", "body": "string", "userId": "integer"},
            )
