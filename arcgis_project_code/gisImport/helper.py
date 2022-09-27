import re
import json
import base64
import requests as r

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
    response_json = response.json()
    # if response_json.get('state') is None:
    #     state="Ongoing"
    # else:
    #     state= response_json['state']

    return response_json

def escape_char_sub(s):
    str = re.sub('[^A-Za-z0-9]+', ' ', s)
    return str

def write_results(file, json_data):
    with open(file, 'w') as f:
        f.write(str(json_data).replace("'",'"'))
    return "data written to file:"+ file

def get_template(template):
    paths ={"folder":"./gisImport/templates/import-folder-template.json",
    "schema":"./gisImport/templates/import-schema-template.json",
    "table":"./gisImport/templates/import-table-template.json",
    "field":"./gisImport/templates/import-field-template.json"}

    with open(paths[template], 'r') as f:
        target_pattern = json.loads(f.read())[0]
    return target_pattern

def error_pass(v):
    try:
        x=v
    except KeyError:
        x = ""
    return x

def remove_quotes(s):
    string= s.replace('"',"").replace("'","")
    return string