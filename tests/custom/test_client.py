import json
import os
import subprocess
import sys

import pytest
import reka


def test__version():
    assert isinstance(reka.__version__, str)


_CREDENTIAL_CONSUMER = r"""
import asyncio
import json
import os
import sys

import httpx
from reka.client import AsyncReka, Reka
from reka.core.api_error import ApiError

next_key, explicit_key, expected_key, asynchronous = json.loads(sys.argv[1])
if next_key is None:
    os.environ.pop("REKA_API_KEY", None)
else:
    os.environ["REKA_API_KEY"] = next_key
options = {} if explicit_key is None else {"api_key": explicit_key}
seen = []

def handle(request):
    seen.append(request.headers["X-Api-Key"])
    return httpx.Response(200, json=[])

async def check_async():
    async with httpx.AsyncClient(transport=httpx.MockTransport(handle)) as http:
        if expected_key is None:
            try:
                AsyncReka(httpx_client=http, **options)
            except ApiError:
                return
            raise AssertionError("Missing credentials must be rejected")
        client = AsyncReka(httpx_client=http, **options)
        assert await client.models.get() == []
        os.environ["REKA_API_KEY"] = "another-test-key"
        assert await client.models.get() == []
        assert seen == [expected_key, expected_key]

def check_sync():
    with httpx.Client(transport=httpx.MockTransport(handle)) as http:
        if expected_key is None:
            try:
                Reka(httpx_client=http, **options)
            except ApiError:
                return
            raise AssertionError("Missing credentials must be rejected")
        client = Reka(httpx_client=http, **options)
        assert client.models.get() == []
        os.environ["REKA_API_KEY"] = "another-test-key"
        assert client.models.get() == []
        assert seen == [expected_key, expected_key]

if asynchronous:
    asyncio.run(check_async())
else:
    check_sync()
"""


@pytest.mark.parametrize("asynchronous", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize(
    "initial_key,next_key,explicit_key,expected_key",
    [
        (None, "late-test-key", None, "late-test-key"),
        ("initial-test-key", "replacement-test-key", None, "replacement-test-key"),
        ("initial-test-key", None, None, None),
        (None, None, None, None),
        ("initial-test-key", "initial-test-key", None, "initial-test-key"),
        ("initial-test-key", "replacement-test-key", "explicit-test-key", "explicit-test-key"),
        (None, "late-test-key", "", ""),
    ],
)
def test_credentials_resolved_at_construction(
    initial_key, next_key, explicit_key, expected_key, asynchronous
):
    environment = os.environ.copy()
    if initial_key is None:
        environment.pop("REKA_API_KEY", None)
    else:
        environment["REKA_API_KEY"] = initial_key
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            _CREDENTIAL_CONSUMER,
            json.dumps([next_key, explicit_key, expected_key, asynchronous]),
        ],
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
