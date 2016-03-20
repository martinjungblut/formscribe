"""General utilities."""


def get_attributes(obj):
    """Retrieve all attributes from an object."""
    return [getattr(obj, _) for _ in dir(obj)]
