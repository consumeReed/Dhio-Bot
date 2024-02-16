import re
import requests

items = []
bt = []
with open('D:\Downloads\Masters_Grimoire_v4.00\Resources\Database\itemlist.txt') as file:
    items = file.readlines()

for i in items:
    if 'Bloodthorn the Ravenous' in i and 'Jagged' not in i and 'DNU' not in i and 'Potion' not in i and 'Seed' not in i and 'Mighty' not in i and 'Majestic' not in i or 'gem blessed by' in i and 'Jagged' not in i and 'DNU' not in i and 'Potion' not in i and 'Seed' not in i and 'Mighty' not in i and 'Majestic' not in i:
        name = re.search('~.*?~', i).group(0).replace('~', '').replace(' ', '-')
        id = re.search('.*?~', i).group(0).replace('~', '')
        url = 'https://celticheroesdb.com/_images/item/' + str(id) + '_' + name + '.png'
        bt.append(url)

i = 299
for j in bt:
    img_data = requests.get(j).content
    iname = 'bt_images/'+ str(i) + '.png'
    with open(iname, 'wb') as handler:
        handler.write(img_data)
    i+=1