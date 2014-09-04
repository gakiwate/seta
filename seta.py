import json
import requests
import requests_cache
import itertools

requests_cache.install_cache('seta-backend', backend='sqlite', expire_after=604800)

_r = requests.get('http://54.215.155.53/unique_fields')
setaUFjson = json.loads(_r.text)

buildTypes = list(itertools.chain(*setaUFjson['buildtypes']))
testTypes = list(itertools.chain(*setaUFjson['testtypes']))
platforms = list(itertools.chain(*setaUFjson['platforms']))

masterList = [platforms, buildTypes, testTypes]

setaList = list(itertools.product(*masterList))

f = open('seta-failure-analysis.csv', 'w')

for item in setaList:
    url = 'http://54.215.155.53/revisions_with_failures?platform=%s&buildtype=%s&testtype=%s' %(
        item[0], item[1], item[2])
    r = requests.get(url)
    resultJSON = json.loads(r.text)
    if 'revlist' in resultJSON:
        data = (item[0], item[1], item[2], len(resultJSON['revlist']))
    else:
        data = (item[0], item[1], item[2], 0)

    print data
    f.write(str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "," + str(data[3]) + "\n")

print "--------"
print "Done!"
print "--------"
