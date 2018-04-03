#get list of indicies\
#create new index based on old index
#reindex
import json
import urllib2
import requests

baseUrl = "test"

listOfIndices = urllib2.urlopen(baseUrl+"something").read()

for indexname in listOfIndices:
    uniqueIndexUrl = baseUrl+"something"+indexname
    indexStructureString = urllib2.urlopen(uniqueIndexUrl).read()
    indexStructureJson = json.loads(indexStructureString)
    # set up indexcreation
    creationdate = indexStructureJson["settings"]["index"]["creation_date"]
    del indexStructureJson["settings"]["index"]["creation_date"]
    del indexStructureJson["settings"]["index"]["version"]
    indexStructureJson["mappings"]["_default_"]["_meta"]["creation_date"] = creationdate
    
    #create new index
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(baseUrl + indexname+"-1", data=indexStructureJson)
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'PUT'
    url = opener.open(request)

    #reindex
    https://stackoverflow.com/questions/4476373/simple-url-get-post-function-in-python
    
    
    
    
