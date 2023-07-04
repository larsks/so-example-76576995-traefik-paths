import os
import requests
import pytest

from urllib3.util import connection


@pytest.fixture(autouse=True)
def force_address(monkeypatch):
    orig_create_connection = connection.create_connection
    override_host = os.environ.get("REQUESTS_FORCE_ADDRESS")

    def patch_create_connection(address, *args, **kwargs):
        host, port = address
        host = override_host if override_host is not None else host
        return orig_create_connection((host, port), *args, **kwargs)

    connection.create_connection = patch_create_connection


def whoami_to_dict(content: str) -> dict:
    lines = [line for line in content.splitlines() if line]
    return {k.rstrip(":"): v for k, v in [line.split(None, 1) for line in lines]}


@pytest.mark.parametrize(
    "url,hostname,path",
    (
        # fmt: off
        # Test that this url                         goes to        with this path
        #                                            this hostname
        #
        ("http://dev.mywebsite.io/api-server",       "api-server",  "/"),
        ("http://dev.mywebsite.io/api-server/a/b/c", "api-server",  "/a/b/c"),
        ("http://dev.mywebsite.io/",                 "theia",       "/"),
        ("http://dev.mywebsite.io/hermes",           "hermes",      "/"),
        ("http://dev.mywebsite.io/hermes/",          "hermes",      "/"),
        ("http://dev.mywebsite.io/hermes/a/b/c",     "hermes",      "/a/b/c"),
        ("http://dev.mywebsite.io/hermes2",          "hermes",      "/"),
        ("http://dev.mywebsite.io/hermes2/",         "hermes",      "/"),
        ("http://dev.mywebsite.io/hermes2/a/b/c",    "hermes",      "/a/b/c"),
        ("http://dev.mywebsite.io/hermes3",          "hermes",      "/"),
        ("http://dev.mywebsite.io/hermes3/",         "hermes",      "/"),
        ("http://dev.mywebsite.io/hermes3/a/b/c",    "hermes",      "/a/b/c"),
        # fmt: on
    ),
)
def test_urls(url, hostname, path):
    res = requests.get(url)
    assert res.status_code == 200
    attrs = whoami_to_dict(res.text)
    assert attrs["Hostname"].startswith(
        hostname
    ), f"hostname for {url} must contain {hostname}"
    assert "GET" in attrs
    assert attrs["GET"].split()[0] == path
