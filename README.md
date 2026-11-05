# API Test Automation Framework

A data-driven REST API test framework in **Python (Pytest + Requests)** with
response validators, HTML reporting, a **GitHub Actions** CI pipeline, and an
optional **LLM-based test-case generator** (Gemini).

## Highlights

- **Data-driven tests**: 29 test cases in JSON (positive, negative, boundary, missing fields,
  invalid datatypes, invalid headers, performance) run through one parametrized Pytest test.
- **Reusable validators**: status code, response time, JSON validity, headers, required fields,
  datatypes, business rules.
- **OpenAPI-style specification** (`data/api_specification.py`) describing endpoints,
  parameters, request schemas and responses; the contract the tests and the LLM generator work from.
- **Local mock server** (`mock_server/`, Flask) that enforces that contract, so negative tests
  (HTTP 400/405/415) are real and the suite is deterministic with no network dependency.
- **LLM test generation** (optional): `python -m utils.llm_test_generator` generates cases from the
  specification, validates their shape, and writes `data/generated_test_cases.json`.
- **CI/CD**: GitHub Actions installs dependencies, runs the suite and uploads the HTML report.

## Project structure

```text
.github/workflows/api-test-pipeline.yml   CI pipeline
data/api_specification.py                 OpenAPI-style API contract
data/test_cases.json                      Reviewed baseline test cases
mock_server/app.py                        Flask mock of the /posts API
tests/conftest.py                         Fixtures (starts the mock server, API client)
tests/test_api_endpoints.py               Parametrized API test
utils/api_client.py                       HTTP client
utils/validators.py                       Response validators
utils/llm_test_generator.py               Optional LLM test-case generator
reports/                                  Execution summary + generated HTML report
```

## Run it

```bash
pip install -r requirements.txt
pytest                      # runs against the local mock server
```

The HTML report is written to `reports/api_test_report.html`.

**Against another API** (for example a staging deployment):

```bash
API_BASE_URL=https://your-api.example.com pytest
```

**Generate new test cases with an LLM** (optional):

```bash
pip install -r requirements-llm.txt
export GOOGLE_API_KEY=your_key
python -m utils.llm_test_generator   # writes data/generated_test_cases.json
pytest                               # uses the generated file when present
```

Review generated cases before trusting them: LLMs sometimes pick wrong expected status codes.
Delete `data/generated_test_cases.json` to go back to the baseline set.

## Design notes

- **Why a mock server?** `jsonplaceholder.typicode.com` is a fake API that accepts almost any input and
  never returns 400, so validation tests cannot pass against it. Running those cases against it
  fails by design; the mock enforces the specification instead.
- **Why cache LLM output?** Generated tests are non-deterministic (case counts and expectations
  change between runs). The suite runs from a reviewed JSON file so CI is reproducible, and
  generation is an explicit, separate step.

## Possible next steps

- Load the contract from a real `openapi.yaml` and validate responses with a schema library.
- Add authentication, pagination and rate-limit scenarios.
- Run the same suite against a containerized service (Docker) in CI.
