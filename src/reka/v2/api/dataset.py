"""Dataset-related server interactions."""

from typing import Any, Dict, List, Optional, cast

from requests.exceptions import HTTPError

import reka.v2.api.driver as driver
from reka.v2.errors import DatasetError


def list_datasets() -> List[str]:
    """List all datasets available to the user of the `API_KEY`.

    Returns:
       List of dataset names.
    """
    resp = driver.make_request(
        method="get",
        endpoint="datasets",
    )
    return cast(List[str], resp)


def add_dataset(
    filepath: str,
    name: str,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    """Upload a dataset to run jobs on it later.

    NOTE: If the `name` is deemed inappropriate by the server, e.g. "../../etc/shadow", it will
    be changed to a secure name, which is returned in the response.

    Args:
        filepath: str, local path to a text file or a zipped collection of text files.
        name: str, what should the dataset be called
        description: Optional[str], optional metadata description

    Returns:
        Dictionary object representing what happened with the uploaded file.
    """
    form = {
        "dataset_name": name,
        "dataset_description": description,
    }

    with open(filepath, "rb") as f:
        resp = driver.make_request(
            method="post",
            endpoint="datasets",
            data=form,
            files={"file": f},
        )

    return resp


def delete_dataset(name: str) -> Dict[str, Any]:
    """Delete a dataset with a given name for the user of this API_KEY.

    Args:
        name: name of the dataset to delete.

    Returns: Dictionary object with keys `name` (*str*, the dataset name), `ok` (*bool•), and `info` (*str*).
    """
    try:
        return driver.make_request(
            method="delete",
            endpoint=f"datasets/{name}",
        )

    except HTTPError as e:
        if e.response.status_code == 404:
            raise DatasetError(underlying=e, reason="Unable to delete missing dataset.")

        else:
            raise DatasetError(underlying=e)
