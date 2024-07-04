import json
import pymongo
from datetime import datetime

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dhio']

col = db['gear']
col.drop()
col = db['gear']
#col.insert_one({"discord_id": 148113452534202368, "discord_name": "Reed", "privilege": 2, "queries": 0, "image_queries": 0})
#col.insert_one({"discord_id": 654157138763186206, "discord_name": "Colleen", "privilege": 2, "queries": 0, "image_queries": 0})