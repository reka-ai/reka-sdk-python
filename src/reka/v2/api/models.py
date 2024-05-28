"""Model-related server interactions."""

from typing import List, cast

import reka.api.driver as driver


def list_models() -> List[str]:
    """List all models available to the user of the `API_KEY`.

    Returns:
       List of model names.
    """
    resp = driver.make_request(
        method="get",
        endpoint="models",
    )
    return cast(List[str], resp)
