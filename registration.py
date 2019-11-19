
class Registration:
    """
        a similar implementation of the corresponding Spring Boot Admin class
        c.f,. https://github.com/codecentric/spring-boot-admin/blob/master/spring-boot-admin-server/src/main/java/de/codecentric/boot/admin/server/domain/values/Registration.java
    """

    name = None
    managementUrl = None
    healthUrl = None
    serviceUrl = None
    source = None
    metadata = {}

    def __init__(self, name, healthUrl, source=None, managementUrl=None, serviceUrl=None, metadata={}):
        self.name = name
        self.managementUrl = managementUrl
        self.healthUrl = healthUrl
        self.serviceUrl = serviceUrl
        self.source = source
        self.metadata = metadata
