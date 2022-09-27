import json
import base64
import requests as r
import gisImport.helper as h
import random

class Collect:

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def CollectServerHomeData(self, url):
        server_json = r.get(url=url+"?f=pjson").json()
        if server_json['folders'] is None:
            pass
        else:
            folders =server_json['folders']
        print("Folders List: " +str(folders))

        if server_json['services'] is None:
            pass
        else:
            services = server_json['services']
        print("Services List: " +str(services))

        return {"folders":folders, "services":services}

    def CreateCompleteServerData(self, gis_url, folders_list):
        complete_json={}
        folders=folders_list
        for folder in folders:
            complete_json[folder]=""
            url = gis_url+"/"+folder+"?f=pjson"
            try:
                print("*** FOLDER URL: " + url)
                folder_response =r.get(url=url)
            except Exception as e:
                print(e)
                pass
            # may have to buil in error catching for creating folder_services
            try:
                folder_services = folder_response.json()['services']
            except Exception as e:
                print(e)
                pass
            else:
                #Is this necessary?
                complete_json[folder]=folder_services

                # now indented to run dependent ont he outcome of the last if: else: block
                for service in complete_json[folder]:
                #print(service)
                    service_url = url.replace("?f=pjson","/"+service['name'].split("/")[1])+"/"+service['type']+"?f=pjson"
                    print("*** SERVICE URL: : " + service_url)
                    try:
                        service_response = r.get(url=service_url)
                    except Exception as e:
                        print(e)
                        pass
                    else:
                    #clean this up
                        service_json= service_response.json()
                        service['metadata']=service_json
                    if service['metadata'].get('layers') is None:
                        pass 
                    else:
                        layers=service['metadata']['layers']
                        for layer in layers:
                            print(str(layer))
                            layer_url = service_url.replace("?f=pjson","/"+str(layer['id']))+"?f=pjson"
                            print("***LAYER URL: "+layer_url)
                            layer_metadata = r.get(layer_url).json()
                            layer['detailed_layer_metadata']=layer_metadata
                print(str(folder) + " COMPLETED")
       #on the ec2 server ./gisImport/tests/server_payload_test.json works for some reason
        h.write_results("./gisImport/tests/server_payload_test.json",complete_json)
        return complete_json

    def CreateFolderUploadFile(self, gis_server_data, community):
        
        asset_list=[]
        folder_list=[]
        target_pattern = h.get_template("folder")

        for key, value in gis_server_data.items():
            folder_list.append(key)

        for i in folder_list:
            target_pattern['identifier']['name'] = h.remove_quotes(i)
            target_pattern['identifier']['community']['name']=community
            new_pattern = json.dumps(target_pattern)
            asset_list.append(json.loads(new_pattern))

        h.write_results('./gisImport/uploads/folder-uploads.json', asset_list)

    def CreateServiceUploadFile(self, gis_server_data, community):
        
        asset_list=[]
        folder_list=[]
        target_pattern = h.get_template("schema")
        
        for key, value in gis_server_data.items():
            folder_list.append(key)

        for folder in folder_list:
            data=gis_server_data[folder]
            for i in range(0, len(data)):
                target_pattern['identifier']['name']=h.error_pass(h.remove_quotes(data[i]['name'] +" - "+ data[i]['type']))
                target_pattern['attributes']['Description'][0]['value']=h.escape_char_sub(h.error_pass(h.remove_quotes(data[i]['metadata']['serviceDescription'])))
                # need to figure out how to remove escape characters in the descriptions 
                target_pattern['identifier']['domain']['name']=folder
                target_pattern['identifier']['domain']['community']['name']=community
                new_pattern = json.dumps(target_pattern)
                asset_list.append(json.loads(new_pattern))
        
        h.write_results('./gisImport/uploads/schema-uploads.json', asset_list)

    def CreateLayerUploadFile(self, gis_server_data, community):
        
        asset_list=[]
        folder_list=[]
        target_pattern = h.get_template("table")

        for key, value in gis_server_data.items():
            folder_list.append(key)
        
        for folder in folder_list:
            data= gis_server_data[folder]
            for i in range(0, len(data)):
                if data[i]['metadata'].get('layers') is None:
                    pass
                else:
                    layer_data = data[i]['metadata']['layers']
                    for layer in layer_data:
                        #write_to_file(" ***FOLDER: " + folder + " ***SERVICE: " + data[i]['name']+ " ***LAYER: "+ layer['name'])
                        target_pattern['identifier']['name']=h.remove_quotes(folder + " -> "+data[i]['name'] +" -> " +data[i]['type'] +" -> "+ layer['name'])
                        target_pattern['relations']['00000000-0000-0000-0000-000000007043:SOURCE'][0]['name']\
                            =h.remove_quotes(data[i]['name'] +" - "+ data[i]['type'])
                        target_pattern['relations']['00000000-0000-0000-0000-000000007043:SOURCE'][0]['domain']['name']\
                            =folder
                        target_pattern['identifier']['domain']['name']=folder
                        target_pattern['identifier']['domain']['community']['name']=community
                        target_pattern['relations']['00000000-0000-0000-0000-000000007043:SOURCE'][0]['domain']['community']['name']=community
                        target_pattern['attributes']['dd04ec97-3aff-4d89-b3f1-99d3df82d41e'][0]['value']= layer['detailed_layer_metadata']['type']
                        new_pattern = json.dumps(target_pattern)
                        asset_list.append(json.loads(new_pattern))
                        # for some reason the schema DCGIS_DATA/WARD_TEST - MapServer was in my code but not in the platform (revisit this)

        h.write_results('./gisImport/uploads/table-uploads.json', asset_list)
    
    def CreateFieldUploadFile(self, gis_server_data, community):
        
        asset_list=[]
        folder_list=[]
        target_pattern = h.get_template("field")

        for key, value in gis_server_data.items():
            folder_list.append(key)
        
        for folder in folder_list:
            data= gis_server_data[folder]
            for i in range(0, len(data)):
                if data[i]['metadata'].get('layers') is None:
                    pass
                else:
                    layer_data = data[i]['metadata']['layers']
                    for layer in range(0,len(layer_data)):
                        if layer_data[layer]['detailed_layer_metadata'].get('fields') is None:
                            pass
                        else:
                            fields = layer_data[layer]['detailed_layer_metadata']['fields']
                            layer=layer_data[layer]
                            for field in fields:
                                #print(field['name'])
                                target_pattern['identifier']['name']=h.error_pass(h.remove_quotes(layer['name'] + " -> " + field['name'] + str(random.random())[2:7]))
                                target_pattern['identifier']['domain']['name']=folder
                                target_pattern['relations']['00000000-0000-0000-0000-000000007042:TARGET']\
                                    [0]['domain']['name']=folder
                                target_pattern['relations']['00000000-0000-0000-0000-000000007042:TARGET']\
                                    [0]['name'] =h.error_pass(h.remove_quotes(folder + " -> "+data[i]['name'] +" -> " +data[i]['type'] +" -> "+ layer['name']))
                                target_pattern['identifier']['domain']['community']['name']=community
                                target_pattern['relations']['00000000-0000-0000-0000-000000007042:TARGET'][0]['domain']['community']['name']=community
                                new_pattern = json.dumps(target_pattern)
                                asset_list.append(json.loads(new_pattern))
        
        h.write_results('./gisImport/uploads/field-uploads.json', asset_list)
        
