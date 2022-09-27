import json
import base64
import requests as r
import time
import gisImport.helper as h

def wait_for_job_finish(func):
    def checker(*args, **kwargs):
        job=func(*args, **kwargs)
        job_state=job['state']
        job_id=job['id']
        print ("JOB ID: " + job_id, "JOB STATE: "+ job_state)
        print("JOB STATUS: " + json.dumps(job_state))
        t=0
        while job_state=="WAITING":
            job_state=h.get_job_status(job_id)
            t+=1
            print("time is: " + str(t) + "seconds")
            print("JOB STATUS: "+ json.dumps(job_state))
            time.sleep(2)
        if job_state=="COMPLETED":
            print("JOB STATUS: " + json.dumps(job_state))
        elif job_state=="WAITING":
            print("JOB STATUS: "+ json.dumps(job_state))
        else:
            pass

    return checker

# def wait_for_job_finish(func):
#     def checker(*args, **kwargs):
#         job=func(*args, **kwargs)
#         print(str(job))
#         time.sleep(2)

#     return checker

class LoadData:

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)
        
        self.username=base64.b64decode('RGF0YUxha2VBZG1pbg=='\
            .encode('utf-8'))\
                .decode('utf-8')

        self.password=base64.b64decode('Y29sbGlicmFkYXRhY2l0aXplbnM='\
            .encode('utf-8'))\
                .decode('utf-8')


    @wait_for_job_finish
    def upload_assets(self, domain, assets_file):
        url = domain + "/rest/2.0/import/json-job"

        assets = {'file': open(str(assets_file), 'rb')}

        response = r.post(
                url, 
                auth=(self.username, self.password),
                files=assets
            )
        return response.json()