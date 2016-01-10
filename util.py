"""General utilities."""


def get_attributes(obj):
    """Retrieve all attributes from an object."""
    return [getattr(obj, _) for _ in dir(obj)]


def get_attributes_names(obj):
    """Retrieve all public attributes names from an object."""
    attributes = [attrs if not attrs.startswith('__') else None
                  for attrs in dir(obj)]
    return list(filter(None, attributes))
