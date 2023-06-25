import re
import requests

items = []
h = []
with open('D:\Downloads\Masters_Grimoire_v4.00\Resources\Database\itemlist.txt') as file:
    items = file.readlines()

for i in items:
    if 'Hrungnir' in i and 'Iceband' not in i and 'Fireband' not in i and 'Bangle' not in i:
        name = re.search('~.*?~', i).group(0).replace('~', '').replace(' ', '-')
        id = re.search('.*?~', i).group(0).replace('~', '')
        url = 'https://celticheroesdb.com/_images/item/' + str(id) + '_' + name + '.png'
        h.append(url)

i = 518
for j in h:
    img_data = requests.get(j).content
    iname = 'hrung_images/'+ str(i) + '.png'
    with open(iname, 'wb') as handler:
        handler.write(img_data)
    i+=1