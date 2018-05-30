import os
import csv
import json
import time
import sys
os.chdir(os.path.dirname(os.path.realpath(__file__)))
pathway=os.path.dirname(os.path.realpath(__file__))
fpath=os.path.join(pathway,'idpl.csv')

def id2footprint(indir,inputfile,item,asset,export):
    if (indir==None and inputfile==None):
        inputfile=os.path.join(os.path.dirname(os.path.realpath(__file__)),'idpl.csv')
        with open(inputfile,'r') as f:
            numline = len(f.readlines())
        with open(inputfile,'r') as f:
            reader = csv.DictReader(f)
            l=[]
            for i,line in enumerate(reader):
                print("Processing "+str(i+1)+" of "+str(numline-1))
                l.append(line['id'])
            pjson={"type": "AndFilter","config": [{"type": "StringInFilter","field_name": "id","config": []}]}
            pjson['config'][0]['config']=l
            json_data = json.dumps(pjson)
            with open('pjson.json', 'w') as outfile:
                json.dump(pjson, outfile)
            time.sleep(2)
            try:
                print("")
                os.system("planet data search --item-type "+str(item)+" --asset-type "+str(asset)+' --filter-json "'+os.path.join(pathway,"pjson.json")+'" --limit 10000 >"'+export+'"')
                print("Footprints Exported to "+str(export))
            except Exception as e:
                print(e)
    elif (indir!=None and inputfile==None):
        for filename in os.listdir(indir):
            if filename.endswith('.csv'):
                fpath=os.path.join(indir,filename)
                inputfile=fpath
                export=os.path.join(indir,os.path.basename(filename).split('.')[0]+'_footprint.geojson')
                with open(inputfile,'r') as f:
                    numline = len(f.readlines())
                with open(inputfile,'r') as f:
                    reader = csv.DictReader(f)
                    l=[]
                    for i,line in enumerate(reader):
                        print("Processing "+str(i+1)+" of "+str(numline-1))
                        l.append(line['id'])
                    pjson={"type": "AndFilter","config": [{"type": "StringInFilter","field_name": "id","config": []}]}
                    pjson['config'][0]['config']=l
                    json_data = json.dumps(pjson)
                    with open('pjson.json', 'w') as outfile:
                        json.dump(pjson, outfile)
                    time.sleep(2)
                    try:
                        os.system("planet data search --item-type "+str(item)+" --asset-type "+str(asset)+' --filter-json "'+os.path.join(pathway,"pjson.json")+'" --limit 10000 >"'+export+'"')
                        print("Footprints Exported to "+str(export))
                        print("")
                    except Exception as e:
                        print(e)
    else:
        with open(inputfile,'r') as f:
            numline = len(f.readlines())
        with open(inputfile,'r') as f:
            reader = csv.DictReader(f)
            l=[]
            for i,line in enumerate(reader):
                print("Processing "+str(i+1)+" of "+str(numline-1))
                l.append(line['id'])
            pjson={"type": "AndFilter","config": [{"type": "StringInFilter","field_name": "id","config": []}]}
            pjson['config'][0]['config']=l
            json_data = json.dumps(pjson)
            with open('pjson.json', 'w') as outfile:
                json.dump(pjson, outfile)
            time.sleep(2)
            try:
                print("")
                os.system("planet data search --item-type "+str(item)+" --asset-type "+str(asset)+' --filter-json "'+os.path.join(pathway,"pjson.json")+'" --limit 10000 >"'+export+'"')
                print("Footprints Exported to "+str(export))
            except Exception as e:
                print(e)
