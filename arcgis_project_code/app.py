import json
from flask import Flask, request
import requests
import base64
from tester import make_request
import tester

app = Flask(__name__)

@app.route('/')
@app.route('/hello')
def HelloWorld():
    name = request.args['param']
    return "Hello World "+ name

@app.route('/request/')
def get_data():
    
    endpoint = request.args['url']
    response = make_request(endpoint)

    return response

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)