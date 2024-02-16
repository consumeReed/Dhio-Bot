import json
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dhio']
col = db['bank']
col.drop()
col = db['bank']

items = []
with open('items.json') as f:
    items = json.load(f)

for i in items:
    entry = { "item_name": i, "amount": 0}
    col.insert_one(entry)

col = db['recent']
for i in range(3):
    col.insert_one({ "item_name": str(i)})