import pymongo
from datetime import datetime

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dhio']

def inputRecent(list):
    col = db['recent']
    i = col.count_documents({})
    col.insert_one({'id': i+1,'items': list})

def sendRecentToBank(id):
    col = db['recent']
    rec = col.find({'id': id}, {'items':1, '_id': 0})
    list = rec[0]['items']
    col.delete_one({'id': id})

    col = db['bank']
    for i in list:
        col.update_one(
            {'item_name': i},
            {'$inc': {'amount': 1}}
        )

def addToBank(item, v):
    col = db['bank']
    col.update_one(
        {'item_name': item},
        {'$inc': {'amount': int(v)}}
    )

def removeFromRecent(id, item):
    col = db['recent']
    col.update_one(
        {'id': id}, 
        { '$pull': {'items': item}}
        )


def getItems(substr):
    col = db['bank']
    rec = col.find({'item_name': { '$regex': '.*'+substr.lower()+'.*'}}, {'_id': 0})
    l = []
    for it in rec:
        l.append([it['item_name'], it['amount']])
    return l

def updateAmount(item, v):
    col = db['bank']
    col.update_one(
            {'item_name': item},
            {'$set': {'amount': int(v)}}
        )
    
def changeDate():
    col = db['date']
    col.update_one({"id": 1},{'$set':{"date": datetime.today()}})

def getDate():
    col = db['date']
    r = col.find({'id': 1})
    return 'Last updated ' + str(r[0]['date'])
    
#l = ["Godly Aberrant Bracelet of Shield Wall", "Royal Eidolic Necklace of Mercenaries", "Shadowsworn Bow of Winter"]
#l2 = ["Creidhne's Knuckleblade of Ashes", "Shadowsworn Sword of Winter", "Majestic Eidolic Necklace of Hunters"]
