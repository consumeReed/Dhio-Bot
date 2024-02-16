import pymongo
import json


client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dhio']
col = db['bank']

#Add ids and classes to items

mage = ['flames', 'ice shards', 'ice blast', 'blizzards', 'wand', 'firestorm', 'laceration', 'contusion', 'fire bolt', 'grimoire of ash', 'grimoire of winter']
druid = ['opposition', 'lightning', 'seer', 'breath', 'touch', 'resistance', 'storm', 'totem', 'sage', 'grimoire of earth']
warrior = ['shield', 'rupture', 'viking', 'valor', 'sword', 'hammer', 'axe', 'knights', 'barbarian', 'pummel', 'taunt']
ranger = ['shot', 'archer', 'hunter', 'bow']
rogue = ['of shadows', 'ass', 'sneaky', 'dagger', 'quick', 'brawlers', 'knuckle']

d = {"mage": mage, "druid": druid, "warrior": warrior, "ranger": ranger, "rogue": rogue}

items = []
i = 1
with open('db\items.json') as f:
    items = json.load(f)


def getItems(substr):
    it = d.get(substr)
    if it is None:
        col = db['bank']
        rec = col.find({'item_name': { '$regex': '.*'+substr.lower()+'.*'}}, {'_id': 0})
        l = []
        for it in rec:
            l.append([it['item_name'], it['amount']])
        return l
    else:
        l = []
        for i in it:
            l.extend(getItems(i))
        return l
    

def func(str):
    for j in d.get(str):
        f = getItems(str)
        for i in f:
            col.update_one(
                {'item_name': i[0]},
                {'$set': {'class': str}}
                )

for item in items:
    col.update_one(
        {'item_name': item.lower()},
        {'$set': {'id': i}}
        )
    i+=1

func('mage')
func('druid')
func('warrior')
func('ranger')
func('rogue')