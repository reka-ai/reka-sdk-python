"""Wrapper around requests, handling authentication, reka server, and exceptions."""

import json
import logging
from typing import Any, Dict, Optional, cast

import requests

import reka.v2 as rekav2
from reka.v2.errors import AuthError


def make_request(
    method: str,
    endpoint: str,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Optional[str]]] = None,
    json: Any = None,
    files: Any = None,
) -> Dict[str, Any]:
    """Wrapper around requests, handling authentication, reka server, and exceptions."""
    headers = headers or {}
    if rekav2.API_KEY is None:
        raise AuthError(
            reason='Reka API key not set. Set in code with `rekav2.API_KEY = "your-key"`, '
            'or using the environment variable `export REKA_API_KEY="your-key"`.'
        )

    headers["X-Api-Key"] = rekav2.API_KEY

    try:
        response = requests.request(
            method=method,
            url=f"{rekav2._SERVER}/{endpoint}",
            headers=headers,
            data=data,
            files=files,
            json=json,
        )
        logging.debug(f"Received response {response.text}.")
        response.raise_for_status()
    except requests.HTTPError as e:
        # Include the server response in the exception text to help with debugging:
        e.args = (
            f"{e.args[0]} Server response: '{_get_response_error_detail(response.text)}'",
            *e.args[1:],
        )
        logging.error(f"HTTPError {e} occurred handling request.")
        raise
    except requests.exceptions.RequestException as e:
        logging.error(f"Error {e} occurred handling request.")
        raise

    if "application/json" not in response.headers.get("Content-Type", ""):
        logging.error(f"No JSON returned by server. Server response: {response.text}")
        raise ValueError("Expected JSON response")

    return cast(Dict[str, Any], response.json())


def _get_response_error_detail(response_text: str) -> str:
    """Tries to parse the response as JSON and extract the 'detail' key. Defaults to returning original text."""
    try:
        return cast(str, json.loads(response_text)["detail"])
    except (json.JSONDecodeError, KeyError):
        return response_text
