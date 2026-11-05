# ============================================================
# ADVANCED API RESPONSE VALIDATORS
# ------------------------------------------------------------
# Performs intelligent validations:
#
# 1. Status code validation
# 2. JSON validation
# 3. Header validation
# 4. Response schema validation
# 5. Datatype validation
# 6. Required field validation
# 7. Response body validation
# 8. Business rule validation
# 9. Response time validation
# ============================================================

import pytest
import json

class ResponseValidator:

    # ========================================================
    # STATUS CODE VALIDATION
    # ========================================================
    @staticmethod
    def validate_status_code(response, expected_status):

        assert response.status_code == expected_status, (
            f"Expected status code {expected_status}, "
            f"but got {response.status_code}"
        )

    # ========================================================
    # RESPONSE TIME VALIDATION
    # ========================================================
    @staticmethod
    def validate_response_time(response_time, threshold=2000):

        assert response_time < threshold, (
            f"Response time exceeded threshold. "
            f"Actual: {response_time} ms"
        )

    # ========================================================
    # JSON RESPONSE VALIDATION
    # ========================================================
    @staticmethod
    def validate_json_response(response):

        try:
            response.json()

        except json.JSONDecodeError:
            pytest.fail("Response is not valid JSON")

    # ========================================================
    # HEADER VALIDATION
    # ========================================================
    @staticmethod
    def validate_headers(response):

        assert "Content-Type" in response.headers, (
            "Content-Type header missing"
        )

        assert "application/json" in response.headers["Content-Type"], (
            "Invalid Content-Type"
        )

    # ========================================================
    # REQUIRED FIELD VALIDATION
    # ========================================================
    @staticmethod
    def validate_required_fields(response_json, required_fields):

        for field in required_fields:

            assert field in response_json, (
                f"Missing required field: {field}"
            )

    # ========================================================
    # DATATYPE VALIDATION
    # ========================================================
    @staticmethod
    def validate_datatypes(response_json, schema):

        type_mapping = {
            "integer": int,
            "string": str,
            "array": list,
            "object": dict
        }

        for field, expected_type in schema.items():

            if field not in response_json:

                pytest.fail(f"{field} missing in response")

            assert isinstance(
                response_json[field],
                type_mapping[expected_type]
            ), (
                f"{field} datatype mismatch. "
                f"Expected {expected_type}"
            )

    # ========================================================
    # RESPONSE BODY VALIDATION
    # ========================================================
    @staticmethod
    def validate_response_body(response_json, expected_values):

        for key, expected_value in expected_values.items():

            assert response_json[key] == expected_value, (
                f"{key} mismatch"
            )

    # ========================================================
    # BUSINESS RULE VALIDATION
    # ========================================================
    @staticmethod
    def validate_business_rules(response_json):

        # ----------------------------------------------------
        # ID should always be positive
        # ----------------------------------------------------
        if "id" in response_json:

            assert response_json["id"] > 0

        # ----------------------------------------------------
        # Title should not be empty
        # ----------------------------------------------------
        if "title" in response_json:

            assert len(response_json["title"]) > 0

        # ----------------------------------------------------
        # userId should be positive
        # ----------------------------------------------------
        if "userId" in response_json:

            assert response_json["userId"] > 0

