import requests
import base64

def make_request(endpoint):
    username=base64.b64decode('RGF0YUxha2VBZG1pbg=='\
    .encode('utf-8')).decode('utf-8')

    password=base64.b64decode('Y29sbGlicmFkYXRhY2l0aXplbnM='\
    .encode('utf-8')).decode('utf-8')
    
    response = requests.get(
        endpoint, 
        auth=(username, password))

    return response.json()