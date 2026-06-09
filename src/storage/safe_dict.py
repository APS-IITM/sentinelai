def safe_dict(obj):

    if hasattr(
        obj,
        "model_dump"
    ):
        return obj.model_dump(
            mode="json"
        )

    if isinstance(
        obj,
        dict
    ):
        return obj

    return {
        "value": str(obj)
    }