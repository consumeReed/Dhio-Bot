import re
import json

all_items = []

mordris = []


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
    
    if 'Abyssal Armlet' in i or 'ancient tome lie forgotten words' in i:
        mordris.append([name, id, extract_class(i)])

with open('db/mordris_items_appends.json', 'w') as f:
    json.dump(mordris, f)