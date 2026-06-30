"""Tests for configuration.Configuration: parsing a config file and validating
that all demanded keys are present."""
import pytest

from configuration import Configuration

CONF = """[ServiceConfiguration]
springbootadminserverurl = http://localhost:8080
servicename = my-service
serviceport = 5000
servicehost = http://127.0.0.1
servicedescription = a test service
"""


def _write(tmp_path, text):
    path = tmp_path / "app.conf"
    path.write_text(text)
    return str(path)


def test_reads_values_as_attributes(tmp_path):
    cfg = Configuration(_write(tmp_path, CONF), [])
    assert cfg.servicename == "my-service"
    assert cfg.serviceport == "5000"
    assert cfg.springbootadminserverurl == "http://localhost:8080"


def test_passes_when_all_demanded_keys_present(tmp_path):
    cfg = Configuration(_write(tmp_path, CONF), ["servicename", "serviceport"])
    # all demanded keys were found, so none remain outstanding
    assert cfg.demandedConfigurationKeys == []


def test_raises_when_demanded_key_missing(tmp_path):
    with pytest.raises(Exception) as exc:
        Configuration(_write(tmp_path, CONF), ["servicename", "absent_key"])
    assert "absent_key" in str(exc.value)


def test_raises_when_config_file_missing(tmp_path):
    with pytest.raises(Exception) as exc:
        Configuration(str(tmp_path / "does-not-exist.conf"), [])
    assert "no configuration" in str(exc.value)
