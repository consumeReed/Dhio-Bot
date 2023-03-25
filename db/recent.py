import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dhio']
col = db['recent']

'''
col.insert_one({ "id": 43, "changed": 1})
col.insert_one({ "id": 34, "changed": 6})
col.insert_one({ "id": 7, "changed": -1})
col.insert_one({ "id": 3, "changed": 1})
col.insert_one({ "id": 43, "changed": -1})
'''

res = col.find().limit(3).sort("_id", -1)
for r in res:
    print(r)