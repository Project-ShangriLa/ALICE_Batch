import requests
import json

url='http://api.moemoe.tokyo/anime/v1/master/2016/1'
result = requests.get(url)

#print(result.text)

master_list = json.loads(result.text)

for master in master_list:

    titles = master['title']
    if len(master['title_short1']) > 0:
        titles += ' or ' + master['title_short1']
    if len(master['title_short2']) > 0:
        titles += ' or ' + master['title_short2']
    if len(master['title_short3']) > 0:
        titles += ' or ' + master['title_short3']

    print(titles)