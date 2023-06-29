import os
import requests
import pytest

from urllib3.util import connection
from unittest import mock


@pytest.fixture(autouse=True)
def force_address(monkeypatch):
    orig_create_connection = connection.create_connection
    override_host = os.environ.get("REQUESTS_FORCE_ADDRESS")

    def patch_create_connection(address, *args, **kwargs):
        host, port = address
        host = override_host if override_host is not None else host
        return orig_create_connection((host, port), *args, **kwargs)

    connection.create_connection = patch_create_connection


@pytest.mark.parametrize(
    "url,hostname",
    (
        ("http://dev.mywebsite.io/api-server", "api-server"),
        ("http://dev.mywebsite.io/", "theia"),
        ("http://dev.mywebsite.io/hermes", "hermes"),
        ("http://dev.mywebsite.io/hermes/", "hermes"),
        ("http://dev.mywebsite.io/hermes/foo", "theia"),
        ("http://dev.mywebsite.io/hermes2", "hermes"),
        ("http://dev.mywebsite.io/hermes2/", "hermes"),
        ("http://dev.mywebsite.io/hermes2/foo", "theia"),
        ("http://dev.mywebsite.io/hermes3", "hermes"),
        ("http://dev.mywebsite.io/hermes3/", "hermes"),
        ("http://dev.mywebsite.io/hermes3/foo", "hermes"),
        ("http://dev.mywebsite.io/hermes113", "theia"),
        ("http://dev.mywebsite.io/hermes_was_a_dog", "theia"),
    ),
)
def test_urls(url, hostname):
    res = requests.get(url)
    assert res.status_code == 200
    hostname = res.text.splitlines()[0].split()[1]
    assert hostname.startswith(hostname)
