#get list of indicies\
#create new index based on old index
#reindex
import json
import urllib2
import requests

baseUrl = "http://10.3.2.156:31685/"

indices = urllib2.urlopen(baseUrl+"_cat/indices?h=i").read()
listOfIndices = indices.splitlines()

for indexname in listOfIndices:
    # skipdefault indicies
    if indexname.startswith("."):
        continue

    uniqueIndexUrl = baseUrl+indexname
    indexStructureString = urllib2.urlopen(uniqueIndexUrl).read()
    indexStructureJson = json.loads(indexStructureString)
    # set up indexcreation
    creationdate = indexStructureJson[indexname.strip()]["settings"]["index"]["creation_date"]
    del indexStructureJson[indexname.strip()]["settings"]["index"]["creation_date"]
    del indexStructureJson[indexname.strip()]["settings"]["index"]["version"]
    del indexStructureJson[indexname.strip()]["settings"]["index"]["uuid"]
    indexStructureJson[indexname.strip()]["mappings"]["_default_"]["_meta"] = {}
    indexStructureJson[indexname.strip()]["mappings"]["_default_"]["_meta"]["creation_date"] = creationdate

    finalIndexCreation = indexStructureJson[indexname.strip()]
    finalIndexCreationJson = json.dumps(finalIndexCreation)

    #create new index
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(baseUrl + indexname+"-1", data=finalIndexCreationJson)
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'PUT'
    url = opener.open(request)

    #reindex
    reindexRequestData = "{ \"source\": { \"index\": \""+indexname+"\"},\"dest\": { \"index\": \""+indexname+"-1"+"\" }}"
    r = requests.post(baseUrl+"_reindex", reindexRequestData)
    x = 4
    
    
    
