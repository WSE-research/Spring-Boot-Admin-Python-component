"""Registration is a simple value object mirroring the Spring Boot Admin class."""
from registration import Registration


def test_stores_all_fields():
    reg = Registration(
        name="svc",
        healthUrl="http://h/health",
        serviceUrl="http://h",
        managementUrl="http://h/mgmt",
        source="http",
        metadata={"k": "v"},
    )
    assert reg.name == "svc"
    assert reg.healthUrl == "http://h/health"
    assert reg.serviceUrl == "http://h"
    assert reg.managementUrl == "http://h/mgmt"
    assert reg.metadata == {"k": "v"}


def test_optional_fields_default_to_none():
    reg = Registration(name="svc", healthUrl="http://h/health")
    assert reg.managementUrl is None
    assert reg.serviceUrl is None
    assert reg.source is None
