from functools import lru_cache

import geocoder


@lru_cache(maxsize=1)
def get_location() -> dict[str, str] | None:
    """
    Get the location of the machine

    Returns:
        dict: The location of the machine in JSON format.
    """
    try:
        location = geocoder.ip("me")
    except Exception:
        return None
    return location.json
