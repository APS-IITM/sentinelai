def safe_dict(obj):
    """
    Ensures anything (Pydantic / object / dict) becomes JSON-safe dict.
    """
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json")

    if isinstance(obj, dict):
        return obj

    return {"value": str(obj)}