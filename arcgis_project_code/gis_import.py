import sys
import time
from flask import Flask, request
from gisImport import Collector, Loader, helper

app = Flask(__name__)

@app.route('/')
def load_gis():
    gis_server = request.args['gis_server']
    dgc_url = request.args['dgc']
    community = request.args['community']
    folders = request.args['folders']
    #print(gis_server+" " + dgc_url, +" " + community + " " + folders)
    c = Collector.Collect()
    ld= Loader.LoadData()

    server_json= c.CollectServerHomeData(gis_server)

    complete_json_test =c.CreateCompleteServerData(gis_server, [folders])

    print("Creating Folder Upload File")
    c.CreateFolderUploadFile(complete_json_test, community)
    
    print("Creating Schema Upload File")
    c.CreateServiceUploadFile(complete_json_test, community)
    
    print("Creating Layer upload file")
    c.CreateLayerUploadFile(complete_json_test, community)
    
    print("Creating field upload file")
    c.CreateFieldUploadFile(complete_json_test, community)

    # Upload the files
    print("Beginning File Uploads")
    print("Beginning Folder Uploads")
    ld.upload_assets(dgc_url, 
    './gisImport/uploads/folder-uploads.json')
    print("Beginning schema Uploads")
    ld.upload_assets(dgc_url, 
    './gisImport/uploads/schema-uploads.json')
    print("Beginning table Uploads")
    ld.upload_assets(dgc_url, 
    './gisImport/uploads/table-uploads.json')    
    print("Beginning field Uploads")
    ld.upload_assets(dgc_url, 
    './gisImport/uploads/field-uploads.json')


    return "Hello World "+ gis_server + " " + dgc_url + " " + community

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

# if __name__=='__main__':
# Need to build in a Wait for Job to Finish capability - wrapper function?
    # gis_server= args.gis_server
    # dgc_url=args.dgc_url
    # community=args.community
    # print(gis_server, dgc_url, community)

    # gis_server = sys.argv[1]
    # dgc_url = sys.argv[2]
    # community = sys.argv[3]
    # # domain= sys.argv[4]

    # c = Collector.Collect()
    # ld= Loader.LoadData()

    # # gis_server = "https://maps2.dcgis.dc.gov/dcgis/rest/services"
    # # dgc_url = 'https://wconnellycollibracloud.collibra.com'
    # # community="ArcGIS - Server"
    
    # server_json= c.CollectServerHomeData(gis_server)

    # # Collect all metadata from the folders in the top level of the ArcGIS Server home page -
    # #  for complete data use server_json['folders']
    # complete_json_test =c.CreateCompleteServerData(gis_server, server_json['folders'])

    # # Run this to make sure the json has been correctly created
    # # complete_json_test['DDOE'][1]['metadata']['layers'][0]['detailed_layer_metadata']['fields']

    # # Create the upload files
    # print("Creating Folder Upload File")
    # c.CreateFolderUploadFile(complete_json_test, community)
    
    # print("Creating Schema Upload File")
    # c.CreateServiceUploadFile(complete_json_test, community)
    
    # print("Creating Layer upload file")
    # c.CreateLayerUploadFile(complete_json_test, community)
    
    # print("Creating field upload file")
    # c.CreateFieldUploadFile(complete_json_test, community)

    # # Upload the files
    # print("Beginning File Uploads")
    # print("Beginning Folder Uploads")
    # ld.upload_assets(dgc_url, 
    # 'uploads/folder-uploads.json')
    # print("Beginning schema Uploads")
    # ld.upload_assets(dgc_url, 
    # 'uploads/schema-uploads.json')
    # print("Beginning table Uploads")
    # ld.upload_assets(dgc_url, 
    # 'uploads/table-uploads.json')    
    # print("Beginning field Uploads")
    # ld.upload_assets(dgc_url, 
    # 'uploads/field-uploads.json')


    # # for service in services:
    # #     service_url = gis_server[:-2] + "/" + service['name']+"/"+service['type'] + "?f=pjson"
    # #     service_response = r.get(service_url)
    # #     service_json = service_response.json()
    # #     print(service_json)

    # #     for layer in service_json['layers']:
    # #         layer_url = service_url.replace("?f=pjson","/"+str(layer['id']))+"?f=pjson"
    # #         layer_metadata = r.get(layer_url).json()
    # #         print(layer_metadata)