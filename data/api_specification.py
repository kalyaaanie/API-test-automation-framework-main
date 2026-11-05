# ============================================================
# REALISTIC API SPECIFICATION
# ------------------------------------------------------------
# This specification acts like a simplified Swagger/OpenAPI
# contract which the LLM uses to generate intelligent
# API test scenarios dynamically.
# ============================================================

api_specification = {

    "/posts": {

        "GET": {

            "description": "Retrieve posts",

            "query_params": {

                "userId": {
                    "type": "integer",
                    "required": False,
                    "minimum": 1
                }
            },

            "responses": {

                "200": {

                    "description": "Successful retrieval",

                    "schema": {

                        "type": "array",

                        "items": {

                            "id": {
                                "type": "integer"
                            },

                            "title": {
                                "type": "string"
                            },

                            "body": {
                                "type": "string"
                            },

                            "userId": {
                                "type": "integer"
                            }
                        }
                    }
                }
            }
        },

        "POST": {

            "description": "Create new post",

            "headers": {

                "Content-Type": {
                    "type": "string",
                    "required": True,
                    "allowed_values": [
                        "application/json"
                    ]
                }
            },

            "request_body": {

                "required_fields": [
                    "title",
                    "body",
                    "userId"
                ],

                "schema": {

                    "title": {
                        "type": "string",
                        "min_length": 3,
                        "max_length": 100
                    },

                    "body": {
                        "type": "string",
                        "min_length": 5
                    },

                    "userId": {
                        "type": "integer",
                        "minimum": 1
                    }
                }
            },

            "responses": {

                "201": {

                    "description": "Post created successfully",

                    "schema": {

                        "id": {
                            "type": "integer"
                        },

                        "title": {
                            "type": "string"
                        },

                        "body": {
                            "type": "string"
                        },

                        "userId": {
                            "type": "integer"
                        }
                    }
                },

                "400": {
                    "description": "Invalid payload"
                }
            }
        }
    }
}
