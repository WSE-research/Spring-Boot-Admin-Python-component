from flask import Blueprint, Flask, render_template, jsonify, request

myservice = Blueprint('myservice', __name__, template_folder='templates')

"""
    simple endpoints to show the external definition of a custom service
"""


@myservice.route("/", methods=['GET'])
def index():
    """an examplary GET endpoint returning "hello world2 (String)"""
    print(request.host_url)
    return "Hello, World!"


@myservice.route("/", methods=['POST'])
def indexJson():
    """a POST endpoint returning a hello world JSON"""
    data = {'Hello': 'World'}
    return jsonify(data)
