"""End-to-end smoke test: the Flask app boots and serves its health + blueprint."""
import pytest

import app as app_module

pytestmark = pytest.mark.e2e


def test_app_boots_and_serves_endpoints():
    client = app_module.app.test_client()
    assert client.get("/health").data == b"alive"
    assert client.get("/").data == b"Hello, World!"
