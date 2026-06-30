"""Endpoint tests for the Flask app and the myservice blueprint."""
import app as app_module

client = app_module.app.test_client()


def test_health_returns_alive():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.data == b"alive"


def test_about_renders_without_configuration():
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b"<html" in resp.data


def test_blueprint_index_get():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.data == b"Hello, World!"


def test_blueprint_index_post_returns_json():
    resp = client.post("/")
    assert resp.status_code == 200
    assert resp.get_json() == {"Hello": "World"}
