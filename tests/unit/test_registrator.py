"""Tests for registrator.Registrator.callAdminServer with requests faked.

We never start the thread's infinite run() loop; we call callAdminServer
directly and assert it builds the right request and swallows failures.
"""
import json
from unittest.mock import MagicMock, patch

from registration import Registration
from registrator import Registrator


def _registrator():
    reg = Registration(name="svc", healthUrl="http://h/health", serviceUrl="http://h")
    return Registrator("http://admin", "user", "pass", reg, interval=1)


def test_admin_url_gets_instances_suffix():
    r = _registrator()
    assert r.adminServerURL == "http://admin/instances"


def test_call_admin_server_posts_registration_without_none_values():
    r = _registrator()
    with patch("registrator.requests.post") as post:
        post.return_value = MagicMock(status_code=200, __bool__=lambda self: True)
        r.callAdminServer()
    assert post.called
    sent = json.loads(post.call_args.kwargs["data"])
    # None-valued fields (managementUrl, source) are stripped from the payload
    assert "managementUrl" not in sent
    assert sent["name"] == "svc"


def test_call_admin_server_handles_failure_response():
    r = _registrator()
    with patch("registrator.requests.post") as post:
        post.return_value = MagicMock(status_code=500, __bool__=lambda self: False)
        # must not raise even though the server reported failure
        r.callAdminServer()


def test_call_admin_server_swallows_exceptions():
    r = _registrator()
    with patch("registrator.requests.post", side_effect=RuntimeError("network down")):
        # the broad except in callAdminServer keeps the thread alive
        r.callAdminServer()
