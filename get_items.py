import re
import json

items = []
dhio_items = []
with open('D:\Downloads\Masters_Grimoire_v4.00\Resources\Database\itemlist.txt') as file:
    items = file.readlines()

for i in items:
    if 'Dhiothu' in i:
        dhio_items.append(re.search('~.*?~', i).group(0).replace('~', ''))
        
with open('items.json', 'w') as f:
    json.dump(dhio_items, f)