import re
import requests

items = []
dhio = []
with open('D:\Downloads\Masters_Grimoire_v4.00\Resources\Database\itemlist.txt') as file:
    items = file.readlines()

for i in items:
    if 'Dhiothu' in i:
        name = re.search('~.*?~', i).group(0).replace('~', '').replace(' ', '-')
        id = re.search('.*?~', i).group(0).replace('~', '')
        url = 'https://celticheroesdb.com/_images/item/' + str(id) + '_' + name + '.png'
        dhio.append(url)

i = 1
for j in dhio:
    img_data = requests.get(j).content
    iname = 'images/'+ str(i) + '.png'
    with open(iname, 'wb') as handler:
        handler.write(img_data)
    i+=1