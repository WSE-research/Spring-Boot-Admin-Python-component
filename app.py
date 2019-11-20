import logging
import argparse
from flask import Flask, render_template, jsonify, request
from datetime import datetime

from registration import Registration
from registrator import Registrator
from configuration import Configuration

from myservice import myservice


# default config file (use -c parameter on command line specify a custom config file)
configfile = "app.conf"

# endpoint for Web page containing information about the service
aboutendpoint = "/about"

# endpoint for health information of the service required for Spring Boot Admin server callback
healthendpoint = "/health"


# initialize Flask app and add the externalized service information
app = Flask(__name__)
app.register_blueprint(myservice)

# holds the configuration
configuration = None


@app.route(healthendpoint, methods=['GET'])
def health():
    """required health endpoint for callback of Spring Boot Admin server"""
    return "alive"

@app.route(aboutendpoint)
def about():
    """optional endpoint for serving a web page with information about the web service"""
    return render_template("about.html", configuration=configuration)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    # allow configuration of the configfile via command line parameters
    argparser = argparse.ArgumentParser(description='You might provide a configuration file, otherwise "%s" is used.' % (configfile) )
    argparser.add_argument('-c', '--configfile', action='store', dest='configfile', default=configfile, help='overwrite the default configfile "%s"' % (configfile))
    configfile = argparser.parse_args().configfile
    configuration = Configuration(configfile, ['springbootadminserverurl', 'springbootadminserveruser', 'springbootadminserverpassword', 'servicehost', 'serviceport', 'servicename', 'servicedescription'])
    try:
        configuration.serviceport = int(configuration.serviceport) # ensure an int value for the server port
    except Exception as e:
        logging.error("in configfile '%s': serviceport '%s' is not valid (%s)" % (configfile, configuration.serviceport, e) )

    # define metadata that will be shown in the Spring Boot Admin server UI
    metadata = {
        "start": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "description": configuration.servicedescription,
        "about": "%s:%d%s" % (configuration.servicehost, configuration.serviceport, aboutendpoint),
        "written in": "Python"
    }

    # initialize the registation object, to be send to the Spring Boot Admin server
    myRegistration = Registration(
        name=configuration.servicename, 
        healthUrl="%s:%d%s" % (configuration.servicehost, configuration.serviceport, healthendpoint), 
        metadata=metadata
    )
    
    # start a thread that will contact iteratively the Spring Boot Admin server
    registratorThread = Registrator(
        configuration.springbootadminserverurl, 
        configuration.springbootadminserveruser,
        configuration.springbootadminserverpassword, 
        myRegistration
    )
    registratorThread.start()

    # start the web service
    app.run(debug=True, port=configuration.serviceport)
