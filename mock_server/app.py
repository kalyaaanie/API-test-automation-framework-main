"""Local mock of the /posts API described in data/api_specification.py.

jsonplaceholder.typicode.com is a fake API: it accepts almost any payload and
never returns 400, so negative/validation tests can't pass against it. This
mock enforces the same contract as the specification so that every test
category (positive, negative, boundary, headers, schema) is meaningful and
runs deterministically, with no network dependency.
"""

from flask import Flask, jsonify, request

# 100 deterministic posts, 10 per user (same shape as jsonplaceholder)
POSTS = [
    {
        "userId": (i - 1) // 10 + 1,
        "id": i,
        "title": f"post title {i}",
        "body": f"post body text {i}",
    }
    for i in range(1, 101)
]


def _error(message, status):
    return jsonify({"error": message}), status


def create_app():
    app = Flask(__name__)

    @app.get("/posts")
    def list_posts():
        user_id = request.args.get("userId")
        if user_id is None:
            return jsonify(POSTS), 200
        try:
            user_id = int(user_id)
        except ValueError:
            return _error("userId must be an integer", 400)
        if user_id < 1:
            return _error("userId must be >= 1", 400)
        return jsonify([p for p in POSTS if p["userId"] == user_id]), 200

    @app.post("/posts")
    def create_post():
        if request.mimetype != "application/json":
            return _error("Content-Type must be application/json", 415)

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return _error("Body must be a JSON object", 400)

        for field in ("title", "body", "userId"):
            if field not in payload or payload[field] is None:
                return _error(f"Missing required field: {field}", 400)

        title, body, user_id = payload["title"], payload["body"], payload["userId"]

        if not isinstance(title, str) or not 3 <= len(title) <= 100:
            return _error("title must be a string of 3-100 characters", 400)
        if not isinstance(body, str) or len(body) < 5:
            return _error("body must be a string of at least 5 characters", 400)
        # bool is a subclass of int in Python, so exclude it explicitly
        if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id < 1:
            return _error("userId must be an integer >= 1", 400)

        created = {"id": len(POSTS) + 1, "title": title, "body": body, "userId": user_id}
        return jsonify(created), 201

    @app.errorhandler(404)
    def not_found(_):
        return _error("Not found", 404)

    @app.errorhandler(405)
    def method_not_allowed(_):
        return _error("Method not allowed", 405)

    return app


if __name__ == "__main__":
    create_app().run(port=5000)
