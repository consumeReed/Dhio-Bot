import json
import pymongo
from datetime import datetime

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['timer']

col = db['users']
col.drop()
col = db['users']
col.insert_one({"discord_id": 148113452534202368, "discord_name": "Reed", "bosses_down": 0, "subscriptions": []})

col = db['bosses']
col.drop()
col = db['bosses']
col.insert_one({"boss_name": ["mordris", "mord", "mordy", "mordi"], "respawn_time": 1440, "window": 1440, "dead": 0})
col.insert_one({"boss_name": ["hippo", "hrung", "hrungnir", "hrungrir"], "respawn_time": 1440, "window": 1440, "dead": 1712548875})
col.insert_one({"boss_name": ["proteus", "prot"], "respawn_time": 1080, "window": 10, "dead": 1712635365})
col.insert_one({"boss_name": ["necro", "necromancer", "efnisien"], "respawn_time": 1440, "window": 1440, "dead": 1712465096})
col.insert_one({"boss_name": ["bloodthorn", "bt"], "respawn_time": 2160, "window": 2160, "dead": 0})
col.insert_one({"boss_name": ["gelebron", "gele"], "respawn_time": 2160, "window": 2160, "dead": 0})
col.insert_one({"boss_name": ["dhiothu", "dino", "dhio", "dhino"], "respawn_time": 90, "window": 10, "dead": 0})
col.insert_one({"boss_name": ["215", "unox"], "respawn_time": 133, "window": 10, "dead": 0})
col.insert_one({"boss_name": ["snorri", "180"], "respawn_time": 90, "window": 10, "dead": 0})