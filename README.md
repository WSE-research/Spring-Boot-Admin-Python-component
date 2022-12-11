# Python/Flask Web Service Component connecting to Spring Boot Admin

[Spring Boot Admin](https://github.com/codecentric/spring-boot-admin "Spring Boot Admin GitHub repository") is a great tool implemented to provide an admin interface for [Spring Boot<sup>®</sup>](http://projects.spring.io/spring-boot/ "Official Spring-Boot website") applications. However, in a world driven by microservices, other programming languages than Java might also be used to develop components. 

This project provides a simple executable template of a Python Flask application, registering itself as a component to a Spring Boot Admin server. Thereafter, it's monitored by the Spring Boot Admin server (alive status) that also provides access to the shared meta information. Your advantage: Spring Boot and Python applications are monitored using the same tool.


![Python v3.6](https://img.shields.io/badge/python-v3.6-brightgreen) ![Flask v1](https://img.shields.io/badge/flask-v1-brightgreen) [![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)


## Getting Started 

### Prepare the Project

```sh
git clone git@github.com:WSE-research/Spring-Boot-Admin-Python-component.git
cd Spring-Boot-Admin-Python-component
pip install -r requirements.txt
```

### Set up your Service

Copy the template configuration file [app.conf](./app.conf) to create a custom configuration file (e.g., `cp app.conf app.local.conf`). 

Edit your custom configuration file (e.g., `app.local.conf`) and define your environment values. 
Thereafter, the file might look like this:

```ini
[ServiceConfiguration]
springbootadminserverurl = http://localhost:8080/
springbootadminserveruser = admin
springbootadminserverpassword = admin
servicename = myname
serviceport = 5000
servicehost = http://127.0.0.1
servicedescription = my component is doing some magic
```

### Run the Service 

A typical start of the service using the previously defined custom configuration `app.local.conf` might be done via:

```sh
python3 app.py -c app.local.conf
```

Now, check your Spring Boot Admin server UI. 
There should be a component visible having the same name as you had defined in your configuration file.


### Test the Service 

The service template already provides some endpoints. 
For example, a GET endpoint is available at the route `/`. 
If you have defined you run your service at `http://127.0.0.1` (servicehost) and port `5000` (serviceport), then you can open http://127.0.0.1:5000/ using your web browser. 
The response will be `Hello, World!` as defined in [myservice.py](./myservice.py).

Additionally, a basic HTML file is provided using the data defined in the configuration file. 
Following the previously mentioned exemplary configuration, it would be available at: http://127.0.0.1:5000/about

## Customize your Service

### Project Structure

The following files are contained in the project. 

```
.
├── app.conf
├── app.py
├── configuration.py
├── myservice.py
├── registration.py
├── registrator.py
├── requirements.txt
└── templates
    └── about.html
```

Typically, only the file `myservice.py` will be customized. 

### Implement your own Service Functionality

Implementing a customized service is possible using the Flask functionality. 
See the [Flask documentation](https://palletsprojects.com/p/flask/) for details.



## Features

The template service provides the following functionality:
 * calls the Spring Boot Admin server iteratively (by default: every 10 seconds)
   * some metadata is sent to the server, too
 * provides a health interface available at `/health` which will be called by Spring Boot Admin server (callback)
   * the endpoint is used by the Spring Boot Admin server to check if the component is still available
 * provides an HTML page (available at `/about`) containing information about the component (see [templates/about.html](templates/about.html))
   * the presented data is taking from the (custom) config file

## Contributing 

You might:
 * create a pull request (c.f., https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request)
 * [create an issue](./issues/new) to let us know about problems or feature requests
 * ...
