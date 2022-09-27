import requests as r 
import base64
import json

def get_job_status(job_id):

    username=base64.b64decode('RGF0YUxha2VBZG1pbg=='\
        .encode('utf-8'))\
            .decode('utf-8')

    password=base64.b64decode('Y29sbGlicmFkYXRhY2l0aXplbnM='\
        .encode('utf-8'))\
            .decode('utf-8')

    url ="https://wconnellycollibracloud.collibra.com/rest/2.0/jobs/"+job_id

    response = r.get(
            url, 
            headers={"accept": "application/json"},
            auth=(username, password)        
        )

    return response.json()['state']




def outside(func):
    def inside(*args, **kwargs):
        print("a+b="+ func(*args, **kwargs))
    return inside


@outside
def add_two(a,b):
    return str(a+b)

add_two(3,4)