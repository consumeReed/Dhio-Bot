import json
import pymongo
from datetime import datetime

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dhio']

#Users setup, add 2 admins
col = db['users']
col.drop()
col = db['users']
#col.insert_one({"discord_id": 148113452534202368, "discord_name": "Reed", "privilege": 2, "queries": 0, "image_queries": 0})
#col.insert_one({"discord_id": 654157138763186206, "discord_name": "Colleen", "privilege": 2, "queries": 0, "image_queries": 0})

#Last modification date
col = db['date']
col.drop()
col = db['date']
col.insert_one({"id": 1, "date": datetime.today()})

#Recently updated items
col = db['recent']
col.drop()
col = db['recent']
col.insert_one({'id': 247, "changed": 1})

#Active banks
col = db['active']
col.drop()
col = db['active']
col.insert_one({'bank_id': 'dhiothu', 'on': True})
col.insert_one({'bank_id': 'proteus', 'on': True})
col.insert_one({'bank_id': 'mordris', 'on': True})
col.insert_one({'bank_id': 'gelebron', 'on': True})
col.insert_one({'bank_id': 'bloodthorn', 'on': True})
col.insert_one({'bank_id': 'hrungnir', 'on': True})


#For prot and hrung since items don't have innate requirements
def determine_class(the_item, bank):
    if bank == 1:
        if 'energy shield' in the_item or 'fire bolt' in the_item or  'firestorm' in the_item or 'freeze' in the_item or 'ice shards' in the_item or 'sacrifice' in the_item:
            return [3]
        elif 'energy harvest' in the_item or 'grasping' in the_item or 'lightning strike' in the_item or 'natures' in the_item or 'spring' in the_item:
            return [2]
        elif 'bracer' in the_item or 'swing' in the_item or 'rupture' in the_item or 'warcry' in the_item:
            return [1]
        elif 'cuff' in the_item or 'quick' in the_item or 'shadowstrike' in the_item or 'sneaky' in the_item:
            return [5]
        elif 'armlet' in the_item or 'explosive' in the_item or 'longshot' in the_item or 'sharp shot' in the_item:
            return [4]
        else:
            return [6]
        
    elif bank == 2:
        if 'frenzy' in the_item or 'shield wall' in the_item or 'protective' in the_item:
            return [1]
        elif 'quick strike' in the_item or 'expose' in the_item or 'poison' in the_item:
            return [5]
        elif 'double' in the_item or 'sharpen' in the_item or 'steady' in the_item:
            return [4]
        elif 'natures' in the_item or 'howling' in the_item or 'bark' in the_item:
            return [2]
        elif 'fire' in the_item or 'ice' in the_item:
            return [3]
        else:
            return [6]


#initialize bank items
id = 1
col = db['bank']
col.drop()
col = db['bank']
dhio_items = []
with open('db/dhio_items.json') as f:
    dhio_items = json.load(f)
for i in dhio_items:
    entry = { "item_name": i[0].lower().replace('-', ' '), "db_id": i[1], "amount": 0, "id": id, "class": [int(k) for k in i[2].split(',')], "bank": "dhiothu"}
    col.insert_one(entry)
    id+=1

hrung_items = []
with open('db/hrung_items.json') as f:
    hrung_items = json.load(f)
for i in hrung_items:
    entry = { "item_name": i[0].lower().replace('-', ' '), "db_id": int(i[1]), "amount": 0, "id": id, "class": determine_class(i[0].lower(), 1), "bank": "hrungnir"}
    col.insert_one(entry)
    id+=1

bt_items = []
with open('db/bloodthorn_items.json') as f:
    bt_items = json.load(f)
for i in bt_items:
    entry = { "item_name": i[0].lower().replace('-', ' '), "db_id": int(i[1]), "amount": 0, "id": id, "class": [int(k) for k in i[2].split(',')], "bank": "bloodthorn"}
    col.insert_one(entry)
    id+=1

gele_items = []
with open('db/gelebron_items.json') as f:
    gele_items = json.load(f)
for i in gele_items:
    entry = { "item_name": i[0].lower().replace('-', ' '), "db_id": int(i[1]), "amount": 0, "id": id, "class": [int(k) for k in i[2].split(',')], "bank": "gelebron"}
    col.insert_one(entry)
    id+=1

mordris_items = []
with open('db/mordris_items.json') as f:
    mordris_items = json.load(f)
for i in mordris_items:
    if i[2] != '':
        entry = { "item_name": i[0].lower().replace('-', ' '), "db_id": int(i[1]), "amount": 0, "id": id, "class": [int(k) for k in i[2].split(',')], "bank": "mordris"}
    else:
        entry = { "item_name": i[0].lower().replace('-', ' '), "db_id": int(i[1]), "amount": 0, "id": id, "class": [6], "bank": "mordris"}
    col.insert_one(entry)
    id+=1

prot_items = []
with open('db/proteus_items.json') as f:
    prot_items = json.load(f)
for i in prot_items:
    entry = { "item_name": i[0].lower().replace('-', ' '), "db_id": int(i[1]), "amount": 0, "id": id, "class": determine_class(i[0].lower(), 2), "bank": "proteus"}
    col.insert_one(entry)
    id+=1