"""Optional: generate API test cases from the API specification with an LLM.

Usage (needs `pip install -r requirements-llm.txt` and GOOGLE_API_KEY set):

    python -m utils.llm_test_generator

Writes data/generated_test_cases.json. REVIEW the output before committing:
LLMs get expected status codes wrong, so generated cases are validated for
shape here and should be sanity-checked by a human (or against the real API).
"""

import json
import os
from pathlib import Path

from data.api_specification import api_specification

OUTPUT_FILE = Path(__file__).resolve().parent.parent / "data" / "generated_test_cases.json"
REQUIRED_KEYS = {"test_name", "method", "endpoint", "expected_status_code"}

PROMPT = """You are an expert API automation engineer.

Generate realistic API test cases as a JSON array covering: positive scenarios,
negative scenarios, boundary values, missing mandatory fields, invalid
datatypes, invalid headers, performance, and business rules.

Each item must contain: test_name, category, method, endpoint, headers,
query_params, body, expected_status_code. Use unique snake_case test_name values.
Base expectations strictly on the specification below.

API specification:
{spec}

Output ONLY the JSON array."""


def _strip_code_fences(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else ""
        text = text.rsplit("```", 1)[0]
    return text.strip()


def validate_cases(cases):
    """Reject malformed LLM output early with a clear message."""
    if not isinstance(cases, list) or not cases:
        raise ValueError("LLM output must be a non-empty JSON array")
    names = set()
    for i, case in enumerate(cases):
        missing = REQUIRED_KEYS - set(case)
        if missing:
            raise ValueError(f"Case {i} is missing keys: {sorted(missing)}")
        if case["test_name"] in names:
            raise ValueError(f"Duplicate test_name: {case['test_name']}")
        names.add(case["test_name"])
    return cases


def generate_test_cases(spec=api_specification):
    import google.generativeai as genai  # imported lazily: only needed here

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Set GOOGLE_API_KEY to generate test cases with the LLM.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-flash-latest")
    response = model.generate_content(PROMPT.format(spec=json.dumps(spec, indent=2)))
    return validate_cases(json.loads(_strip_code_fences(response.text)))


if __name__ == "__main__":
    cases = generate_test_cases()
    OUTPUT_FILE.write_text(json.dumps(cases, indent=2), encoding="utf-8")
    print(f"Wrote {len(cases)} generated test cases to {OUTPUT_FILE}")
