import threading
import time
import requests
import json
import logging
from requests.auth import AuthBase, HTTPBasicAuth


class Registrator(threading.Thread):
    """
        class running as thread to contact the Spring Boot Admin Server
    """

    jsonHeaders = {"Content-type": "application/json",
                   "Accept": "application/json"}
    adminServerURL = None
    adminServerUser = None
    adminServerPasswordregistration = None
    registration = None  # passed dict containing relevant information
    interval = None  # in seconds

    def __init__(self, adminServerURL, adminServerUser, adminServerPassword, registration, interval=10):
        threading.Thread.__init__(self)
        self.adminServerURL = adminServerURL + "/instances"
        self.adminServerUser = adminServerUser
        self.adminServerPassword = adminServerPassword
        self.registration = registration
        self.interval = interval
        logging.basicConfig(level=logging.DEBUG)

    def run(self):
        while True:
            self.callAdminServer()
            time.sleep(self.interval)

    def callAdminServer(self):
        try:
            # prepare POST request data (None values should not been send)
            requestData = {k: v for k, v in vars(
                self.registration).items() if v is not None}
            response = requests.post(url=self.adminServerURL, headers=self.jsonHeaders, data=json.dumps(
                requestData), auth=HTTPBasicAuth(self.adminServerUser, self.adminServerPassword))

            if response:
                logging.debug("registration: ok on %s (%d)" %
                              (self.adminServerURL, response.status_code))
            else:
                logging.warning("registration: failed at %s with HTTP status code %d" % (
                    self.adminServerURL, response.status_code))

        except Exception as e:
            logging.warning("registration: failed at %s with exception \"%s\"" % (
                self.adminServerURL, e))
