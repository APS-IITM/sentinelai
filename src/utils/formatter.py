import json


def pretty_json(data):
    return json.dumps(
        data,
        indent=4,
        default=str
    )


def normalize_response(response):
    """
    Standard MCP output format for AI layer
    """
    return {
        "success": response.get("status") == "success",
        "count": response.get("count", 0),
        "data": response.get("data", []),
        "error": response.get("message", None)
    }