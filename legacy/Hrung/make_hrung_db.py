import json
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dhio']
col = db['hrung']
col.drop()
col = db['hrung']

items = []
with open('Hrung/hrung_items.json') as f:
    items = json.load(f)

c = 518
for i in items:
    if 'energy shield' in i or 'fire bolt' in i or  'firestorm' in i or 'freeze' in i or 'ice shards' in i or 'sacrifice' in i:
        spec = 'mage'
    elif 'energy harvest' in i or 'grasping' in i or 'lightning strike' in i or 'natures' in i or 'spring' in i:
        spec = 'druid'
    elif 'bracer' in i or 'swing' in i or 'rupture' in i or 'warcry' in i:
        spec = 'warrior'
    elif 'cuff' in i or 'quick' in i or 'shadowstrike' in i or 'sneaky' in i:
        spec = 'rogue'
    elif 'armlet' in i or 'explosive' in i or 'longshot' in i or 'sharp shot' in i:
        spec = 'ranger'
    elif 'fireruby' in i or 'frostopal' in i or 'stormpearl' in i or 'venomjade' in i:
        spec = 'hotswap'
    else:
        spec = 'trash'

    entry = { "item_name": i, "amount": 0, 'id': c, "class": spec}
    col.insert_one(entry)
    c+=1
