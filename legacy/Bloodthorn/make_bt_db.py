import json
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dhio']
col = db['bt']
col.drop()
col = db['bt']

items = []
with open('Bloodthorn/bt_items.json') as f:
    items = json.load(f)

c = 299
for i in items:
    entry = { "item_name": i, "amount": 0, 'id': c}
    col.insert_one(entry)
    c+=1
