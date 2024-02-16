import json
import pymongo
from datetime import datetime

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dhio']

#Users setup, add 2 admins
col = db['users']
col.drop()
col = db['users']
col.insert_one({"discord_id": 148113452534202368}, {"discord_name": "Reed"}, {"privilege": 2}, {"queries": 0}, {"image_queries": 0})
col.insert_one({"discord_id": 654157138763186206}, {"discord_name": "Colleen"}, {"privilege": 2}, {"queries": 0}, {"image_queries": 0})

#Last modification date
col = db['date']
col.drop()
col = db['date']
col.insert_one({"id": 1},{'$set':{"date": datetime.today()}})

#Recently updated items
col = db['recent']
col.drop()
col = db['recent']
col.insert_one({'id': 247}, {"changed": 1})

#For prot and hrung since items don't have innate requirements
def determine_class(the_item, bank):
    if bank == 1:
        if 'energy shield' in the_item or 'fire bolt' in the_item or  'firestorm' in the_item or 'freeze' in the_item or 'ice shards' in the_item or 'sacrifice' in the_item:
            return 'mage'
        elif 'energy harvest' in the_item or 'grasping' in the_item or 'lightning strike' in the_item or 'natures' in the_item or 'spring' in the_item:
            return 'druid'
        elif 'bracer' in the_item or 'swing' in the_item or 'rupture' in the_item or 'warcry' in the_item:
            return 'warrior'
        elif 'cuff' in the_item or 'quick' in the_item or 'shadowstrike' in the_item or 'sneaky' in the_item:
            return 'rogue'
        elif 'armlet' in the_item or 'explosive' in the_item or 'longshot' in the_item or 'sharp shot' in the_item:
            return 'ranger'
        elif 'fireruby' in the_item or 'frostopal' in the_item or 'stormpearl' in the_item or 'venomjade' in the_item:
            return 'hotswap'
        else:
            return 'trash'
    #elif bank == 2:


#initialize bank items
id = 1
col = db['bank']
col.drop()
col = db['bank']
dhio_items = []
with open('db/dhio_items.json') as f:
    dhio_items = json.load(f)
for i in dhio_items:
    entry = { "item_name": i[0].lower(), "db_id": i[1], "amount": 0, "id": id, "class": i[2], "bank": "dhiothu"}
    col.insert_one(entry)
    id+=1

hrung_items = []
with open('db/hrung_items.json') as f:
    hrung_items = json.load(f)
for i in hrung_items:
    entry = { "item_name": i[0].lower(), "db_id": i[1], "amount": 0, "id": id, "class": determine_class(i, 1), "bank": "hrungnir"}
    col.insert_one(entry)
    id+=1

bt_items = []
with open('db/bt_items.json') as f:
    bt_items = json.load(f)
for i in bt_items:
    entry = { "item_name": i[0].lower(), "db_id": i[1], "amount": 0, "id": id, "class": i[2], "bank": "bloodthron"}
    col.insert_one(entry)
    id+=1

gele_items = []
with open('db/gele_items.json') as f:
    gele_items = json.load(f)
for i in gele_items:
    entry = { "item_name": i[0].lower(), "db_id": i[1], "amount": 0, "id": id, "class": i[2], "bank": "gelebron"}
    col.insert_one(entry)
    id+=1

mordris_items = []
with open('db/mordris_items.json') as f:
    mordris_items = json.load(f)
for i in mordris_items:
    entry = { "item_name": i[0].lower(), "db_id": i[1], "amount": 0, "id": id, "class": i[2], "bank": "mordris"}
    col.insert_one(entry)
    id+=1

prot_items = []
with open('db/proteus_items.json') as f:
    prot_items = json.load(f)
for i in bt_items:
    entry = { "item_name": i[0].lower(), "db_id": i[1], "amount": 0, "id": id, "class": determine_class(i, 2), "bank": "proteus"}
    col.insert_one(entry)
    id+=1