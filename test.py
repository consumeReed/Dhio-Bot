import os
from discord.ext import commands
from dotenv import load_dotenv
import discord
import pymongo
from datetime import datetime
from random import *

classes = ['mage', 'druid', 'warrior', 'rogue', 'ranger']
named = ['goibnu', 'luchtaine', 'creidhne']

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dhio']

def formatItem(item):
    formatted_output = ''
    l = item.split(' ')
    for word in l:
        if word != 'of' and word != 'the':
            formatted_output+= word.capitalize() + ' '
        else:
            formatted_output+=word +' '
    return formatted_output


def getSlots(type):
    if type == 1:
        items_neck = []
        items_brace = []
        for j in range(65):
            items_neck.append('majestic')
        for j in range(26):
            items_neck.append('royal')
        for j in range(6):
            items_neck.append('imperial')
        for j in range(3):
            items_neck.append('godly')

        for j in range(60):
            items_brace.append('majestic')
        for j in range(24):
            items_brace.append('royal')
        for j in range(6):
            items_brace.append('imperial')
        for j in range(3):
            items_brace.append('godly')

        random = randint(1, 4)

        if random == 1:
            v = randint(0,99)
            return {items_neck[v]: "necklace"}
        else:
            v = randint(0, 92)
            return {items_brace[v]: "bracelet"}
        

    elif type == 2:
        items_neck = []
        items_weapon = []
        for j in range(208):
            items_neck.append('majestic')
        for j in range(83):
            items_neck.append('royal')
        for j in range(21):
            items_neck.append('imperial')
        for j in range(10):
            items_neck.append('godly')

        for j in range(49):
            items_weapon.append('darksworn')
        for j in range(29):
            items_weapon.append('shadowsworn')
        for j in range(20):
            items_weapon.append('voidsworn')
        for j in range(5):
            items_weapon.append('named')

        random = randint(1, 5)

        if random == 1:
            v = randint(0,102)
            return {items_weapon[v]: "weapon"}
        else:
            v = randint(0, 321)
            return {items_neck[v]: "necklace"}

def getItems0(substr):

    if substr.lower() in classes: 
        col = db['bank']
        rec = col.find({'class': substr.lower()}, {'_id': 0})
        l = []
        for it in rec:
            l.append([it['id'], formatItem(it['item_name']), it['amount']])
        return l

    elif substr == 'weapon':
        col = db['bank']
        rec = col.find({'item_name': { '$regex': '.*of ashes.*'}}, {'_id': 0})
        rec2 = col.find({'item_name': { '$regex': '.*of winter.*'}}, {'_id': 0})
        rec3 = col.find({'item_name': { '$regex': '.*of earth.*'}}, {'_id': 0})
        l = []
        for it in rec:
            l.append([it['id'], formatItem(it['item_name']), it['amount']])
        for it in rec2:
            l.append([it['id'], formatItem(it['item_name']), it['amount']])
        for it in rec3:
            l.append([it['id'], formatItem(it['item_name']), it['amount']])
        return l
    else:
        col = db['bank']
        rec = col.find({'item_name': { '$regex': '.*'+substr.lower()+'.*'}}, {'_id': 0})
        l = []
        for it in rec:
            l.append([it['id'], formatItem(it['item_name']), it['amount']])
        return l

def getLoot():
    bracelets = getItems0('bracelet')
    weapons = getItems0('weapon')
    necklaces = getItems0('necklace')

    bracelets_s = []
    weapons_s = []
    necklaces_s = []
    
    loot = []
    loot_names = []
    loot.append(getSlots(1))
    loot.append(getSlots(1))
    loot.append(getSlots(2))

    for l in loot:
        for key in l.keys():
            tier = key
            type = l[key]

            if type == 'necklace':
                for i in necklaces:
                    if tier in i[1].lower():
                        necklaces_s.append([i[0], i[1]])
                random = randint(0, (len(necklaces_s)-1))
                loot_names.append(necklaces_s[random])
            
            if type == 'weapon':
                for i in weapons:
                    if tier in i[1].lower() and tier != "named":
                        weapons_s.append([i[0], i[1]])
                    elif tier == 'named':
                        if 'dark' not in i[1].lower() and 'shadow' not in i[1].lower() and 'void' not in i[1].lower():
                            weapons_s.append([i[0], i[1]])
                random = randint(0, len(weapons_s)-1)
                loot_names.append(weapons_s[random])

            if type == 'bracelet':
                for i in bracelets:
                    if tier in i[1].lower():
                        bracelets_s.append([i[0], i[1]])
                random = randint(0, len(bracelets_s)-1)
                loot_names.append(bracelets_s[random])
    
    return loot_names

print(getLoot())