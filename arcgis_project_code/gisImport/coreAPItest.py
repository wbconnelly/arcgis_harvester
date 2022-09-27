import requests as r
import base64


username=base64.b64decode('RGF0YUxha2VBZG1pbg=='\
            .encode('utf-8'))\
                .decode('utf-8')

password=base64.b64decode('Y29sbGlicmFkYXRhY2l0aXplbnM='\
            .encode('utf-8'))\
                .decode('utf-8')

url = "https://wconnellycollibracloud.collibra.com/rest/2.0/assets?typeId=00000000-0000-0000-0000-000000011001"

response = r.get(
        url, 
        auth=(username, password)
    )

print(response .json())