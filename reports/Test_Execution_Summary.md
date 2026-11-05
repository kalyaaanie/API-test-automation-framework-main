# Test Execution Summary

Run against the local mock server (`pytest`, Python 3.13, Pytest 9).

| Metric | Result |
|---|---|
| Total tests | 29 |
| Passed | 29 |
| Failed | 0 |

## Coverage by category

| Category | What is checked |
|---|---|
| Positive | Valid GET and POST requests return 200/201 with a valid schema |
| Boundary | Title length 2/3/100/101, body length 4/5, userId 0/1/-1/9999 |
| Missing fields | Missing title, body, userId; empty payload; null title |
| Invalid datatypes | String/integer/boolean in the wrong fields |
| Invalid headers | Wrong Content-Type returns 415 |
| Negative | Unsupported method returns 405; unknown endpoint returns 404 |
| Performance | Response time within the configured budget |

## Notes

- Earlier runs against `jsonplaceholder.typicode.com` showed failures on negative cases
  (it returned 200/201 where 400 was expected) because that service does not validate input.
  The suite now defaults to a local mock that enforces the API specification.
- Running `pytest` also writes the HTML report to `reports/api_test_report.html`.
