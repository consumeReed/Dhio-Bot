import re
import requests
import json

all_items = []

dhiothu = []
bloodthorn = []
hrungnir = []
mordris = []
proteus = []
gelebron = []

def extract_class(input):
    pattern = r'(5\^[0-9]{3}~[0-9,]*~)'
    matches = re.search(pattern, input)
    classes = re.search('~(.*)~', matches.group(0))
    return classes.group(1)

with open('D:\Downloads\Masters_Grimoire_v4.01\Resources\Database\itemlist.txt') as file:
    all_items = file.readlines()

for i in all_items:
    name = re.search('~.*?~', i).group(0).replace('~', '').replace(' ', '-')
    id = re.search('.*?~', i).group(0).replace('~', '')
    
    if 'Dhiothu' in i:
        dhiothu.append([name, id, extract_class(i)])
    elif 'Bloodthorn the Ravenous' in i and 'Jagged' not in i and 'DNU' not in i and 'Potion' not in i and 'Seed' not in i and 'Mighty' not in i and 'Majestic' not in i or 'gem blessed by' in i and 'Jagged' not in i and 'DNU' not in i and 'Potion' not in i and 'Seed' not in i and 'Mighty' not in i and 'Majestic' not in i:
        bloodthorn.append([name, id, extract_class(i)])
    elif 'Hrungnir' in i and 'Iceband' not in i and 'Fireband' not in i and 'Bangle' not in i:
        hrungnir.append([name, id, extract_class(i)])
    elif 'Abyssal' and 'Mordris' in i and 'TEST' not in i and 'OVERWRITE' not in i and 'Chocolate' not in i or 'scale' and 'Mordris' in i and 'TEST' not in i and 'OVERWRITE' not in i and 'Chocolate' not in i:
        mordris.append([name, id, extract_class(i)])
    elif 'Aetheric' in i and 'crafted' not in i and 'Cuhcullain' not in i and 'Fingal' not in i and 'Myrine' not in i and 'Myrrdin' not in i and 'Dian' not in i:
        gelebron.append([name, id, extract_class(i)])
    elif 'Proteus' in i:
        proteus.append([name, id, extract_class(i)])

with open('db/dhio_items.json', 'w') as f:
    json.dump(dhiothu, f)

with open('db/hrung_items.json', 'w') as f:
    json.dump(hrungnir, f)

with open('db/bloodthorn_items.json', 'w') as f:
    json.dump(bloodthorn, f)

with open('db/mordris_items.json', 'w') as f:
    json.dump(mordris, f)

with open('db/gelebron_items.json', 'w') as f:
    json.dump(gelebron, f)

with open('db/proteus_items.json', 'w') as f:
    json.dump(proteus, f)