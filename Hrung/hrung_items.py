import re
import requests
import json

items = []
h = []
with open('D:\Downloads\Masters_Grimoire_v4.00\Resources\Database\itemlist.txt') as file:
    items = file.readlines()

for i in items:
    if 'Hrungnir' in i and 'Iceband' not in i and 'Fireband' not in i and 'Bangle' not in i:
        name = re.search('~.*?~', i).group(0).replace('~', '').lower()
        id = re.search('.*?~', i).group(0).replace('~', '')
        #url = 'https://celticheroesdb.com/_images/item/' + str(id) + '_' + name + '.png'
        #h.append(url)
        h.append(name)

with open('Hrung/hrung_items.json', 'w') as f:
    json.dump(h, f)