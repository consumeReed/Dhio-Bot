import os
from discord.ext import commands
from dotenv import load_dotenv
import discord
import pymongo
from datetime import datetime
from random import *
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename="Logs.log")

classes = ['mage', 'druid', 'warrior', 'rogue', 'ranger']

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


def getItems(substr):

    if substr.lower() in classes: 
        col = db['bank']
        rec = col.find({'class': substr.lower()}, {'_id': 0})
        l = []
        for it in rec:
            if(it['amount']> 0):
                l.append([it['id'], formatItem(it['item_name']), it['amount']])
        return l

    else:
        col = db['bank']
        rec = col.find({'item_name': { '$regex': '.*'+substr.lower()+'.*'}}, {'_id': 0})
        l = []
        for it in rec:
            if(it['amount']> 0):
                l.append([it['id'], formatItem(it['item_name']), it['amount']])
        return l

def getBt():
    col = db['bt']
    rec = col.find({},{'_id': 0})
    l = []
    for it in rec:
        if(it['amount']>0):
            l.append([it['id'], formatItem(it['item_name']), it['amount']])
    return l

def addToBt(item, v):
    col = db['bt']
    col.update_one(
        {'id': item},
        {'$inc': {'amount': int(v)}}
    )

def getBtIdsName(it):
    col = db['bt']
    rec = col.find({'item_name': { '$regex': '.*'+it.lower()+'.*'}}, {'_id': 0})
    l = []
    for it in rec:
        l.append([it['id'], it['item_name']])
    return l


def addToHrung(item, v):
    col = db['hrung']
    col.update_one(
        {'id': item},
        {'$inc': {'amount': int(v)}}
    )


def getHrungIdsName(it):
    col = db['hrung']
    rec = col.find({'item_name': { '$regex': '.*'+it.lower()+'.*'}}, {'_id': 0})
    l = []
    for it in rec:
        l.append([it['id'], it['item_name']])
    return l
    
def getHrungItems(substr):

    if substr.lower() in classes or substr.lower() == 'hotswap': 
        col = db['hrung']
        rec = col.find({'class': substr.lower()}, {'_id': 0})
        l = []
        for it in rec:
            if(it['amount']> 0):
                l.append([it['id'], formatItem(it['item_name']), it['amount']])
        return l

    else:
        col = db['hrung']
        rec = col.find({'item_name': { '$regex': '.*'+substr.lower()+'.*'}}, {'_id': 0})
        l = []
        for it in rec:
            if(it['amount']> 0):
                l.append([it['id'], formatItem(it['item_name']), it['amount']])
        return l


def getDate():
    col = db['date']
    r = col.find({'id': 1})
    return str(r[0]['date'].strftime('%I:%M%p on %B %d %Y'))

def getIds(ch):
    col = db['bank']
    rec = col.find({'class': ch}, {'_id': 0})
    l = []
    for it in rec:
        l.append([it['id'], formatItem(it['item_name'])])
    return l

def getIdsName(it):
    col = db['bank']
    rec = col.find({'item_name': { '$regex': '.*'+it.lower()+'.*'}}, {'_id': 0})
    l = []
    for it in rec:
        l.append([it['id'], it['item_name']])
    return l

def addToBank(item, v):
    col = db['bank']
    col.update_one(
        {'id': item},
        {'$inc': {'amount': int(v)}}
    )

def changeDate():
    col = db['date']
    col.update_one({"id": 1},{'$set':{"date": datetime.today()}})

def getRecent():
    res_list=[]
    col = db['recent']
    res = col.find().limit(10).sort("_id", -1)
    for r in res:
        res_list.append([r['id'], r['changed']])
    return res_list

def idToName(id):
    if id < 299:
        col = db['bank']
        rec = col.find({'id': int(id)}, {'_id': 0})
        return formatItem(rec[0]['item_name'])
    else:
        col = db['bt']
        rec = col.find({'id': int(id)}, {'_id': 0})
        return formatItem(rec[0]['item_name'])


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

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='!')

@bot.command(name='kill', help='Kill a Dhiothu and see what loot you got!')
async def kill(message):
    try:
        loot = getLoot()
        #print(loot)
        resp = str(message.author) + " killed a Dhiothu. Loot is: \n"
        for i in loot:
            resp+= '#' + str(i[0]) + ' ' + i[1] + "\n"
        await message.send(resp)
        logging.info("Successfully killed a dhiothu, user="+str(message.author)+", loot="+str(loot))
    except:
        logging.error("Error killing a dhiothu, user="+str(message.author))

@bot.command(name='find', help='Search the available dhio items banked. Input either item name or class')
async def bank(ctx, *, search):
    try:
        db = client['dhio']
        r = getItems(search)
        resp = 'Bot Last Updated at '+ getDate() + "\n\n"
        if(len(r) == 0):
            resp += 'No Results'
        for i in r:
            resp += "#"+ str(i[0]) +" " + i[1] + "   "  + str(i[2])  +  "\n"
        await ctx.send(resp)
        logging.info("Successfully fulfilled search, user="+str(ctx.author)+", query="+search)
    except:
        logging.error("Error while searching items, user="+str(ctx.author)+", query="+search)

@bot.command(name='bt', help='Shows the good BT gear in bank :3')
async def bt(ctx):
    try:
        r = getBt()
        resp = 'All the good BT items :3\n\n'
        if(len(r)== 0):
            resp+= 'No Results'
        for i in r:
            resp += "#"+ str(i[0]) +" " + i[1] + "   "  + str(i[2])  +  "\n"
        await ctx.send(resp)
        logging.info("Successfully displayed bt items, user="+str(ctx.author))
    except:
        logging.error("Error displaying bt items, user="+str(ctx.author))

@bot.command(name='hippo', help='Search the available Hrung items banked. Input either item name or class or "hotswap" to see dmg rings')
async def bank(ctx, *, search):
    try:
        db = client['hrung']
        r = getHrungItems(search)
        resp = 'Bot Last Updated at '+ getDate() + "\n\n"
        if(len(r) == 0):
            resp += 'No Results'
        for i in r:
            resp += "#"+ str(i[0]) +" " + i[1] + "   "  + str(i[2])  +  "\n"
        await ctx.send(resp)
        logging.info("Successfully fulfilled hrung search, user="+str(ctx.author)+", query="+search)
    except:
        logging.error("Error while searching hrung items, user="+str(ctx.author)+", query="+search)

@bot.command(name='show', help='Input item id to see stats as an image')
async def im(ctx, search):
    try:
        if str(search).isnumeric():
            if int(search) < 914:
                await ctx.send(file=discord.File('images/'+str(search)+'.PNG'))
        logging.info("Successfully displayed image, user="+str(ctx.author)+", image #"+str(search))
    except:
        logging.error("Error displaying item image, user="+str(ctx.author)+", image #"+str(search))

@bot.command(name='update')
async def up(message, *, search):
    try:
        if message.author == bot.user:
            return
        if message.author.id == 148113452534202368 or message.author.id == 336429699469279232 or message.author.id == 365440390200950786:
            inp = str(search).split()
            if int(inp[1]) < 0:
                out = idToName(int(inp[0]))+ str(inp[1])
            else:
                out = idToName(int(inp[0]))+ '+'+ str(inp[1])
            if int(inp[0]) < 299:
                addToBank(int(inp[0]), int(inp[1]))
                changeDate()
                col = db['recent']
                col.insert_one({ "id": int(inp[0]), "changed": int(inp[1])})
                logging.info("Updated Dhiothu item, user="+str(message.author)+", query=["+search+"]")
            elif int(inp[0]) >= 299 and int(inp[0] < 518):
                addToBt(int(inp[0]), int(inp[1]))
                logging.info("Updated BT item, user="+str(message.author)+", query=["+search+"]")
            else:
                addToHrung(int(inp[0]), int(inp[1]))
                changeDate()
                logging.info("Updated Hrung item, user="+str(message.author)+", query=["+search+"]")
            await message.send(out)
        else:
            await message.send('You are not eligible to update item quantities')
            logging.warning("Unauthorized user tried to update items, user="+str(message.author))
    except:
        logging.error("Error updating item quantities, user="+str(message.author)+", query=["+search+"]")

@bot.command(name='btids', help='Shows ids of BT items')
async def u(ctx, search):
    try:
        items = getBtIdsName(search)
        resp = ''
        for i in items:
            resp+='#'+str(i[0]) + '  ' + i[1]+'\n'
        await ctx.send(resp)
        logging.info("Succesffully displayed bt ids list, user="+str(ctx.author)+", search="+search)
    except:
        logging.error("Error displaying bt ids list, user="+str(ctx.author)+", search="+search)

@bot.command(name='hrungids', help='Shows ids of Hrung items')
async def u(ctx, search):
    try:
        items = getHrungIdsName(search)
        resp = ''
        for i in items:
            resp+='#'+str(i[0]) + '  ' + i[1]+'\n'
        await ctx.send(resp)
        logging.info("Succesffully displayed hrung ids list, user="+str(ctx.author)+", search="+search)
    except:
        logging.error("Error displaying hrung ids list, user="+str(ctx.author)+", search="+search)

@bot.command(name='ids', help='Shows ids of Dhio items')
async def i(ctx, search):
    try:
        if search in classes:
            items = getIds(search)
            l = len(items)
            k = 0
            resp = ''
            resp2 = ''
            for i in items:
                k+=1
                if(k<l/2):
                    resp+= '#'+str(i[0]) + '  ' + i[1]+"\n"
                else:
                    resp2+= '#'+str(i[0]) + '  ' + i[1]+"\n"
            
            await ctx.send(resp)
            await ctx.send(resp2)
            logging.info("Succesfully displayed dhiothu ids list by class, user"+str(ctx.author)+", class="+search)
        else:
            items = getIdsName(search)
            resp = ''
            for i in items:
                resp+='#'+str(i[0]) + '  ' + i[1]+'\n'
            await ctx.send(resp)
            logging.info("Successfully displayed dhiothu ids list, user="+str(ctx.author)+", search="+search)
    except:
        logging.error("Error displaying dhiothu ids list, user="+str(ctx.author)+", search="+search)

@bot.command(name='recent', help='Shows the 10 most recently updated items')
async def r(ctx):
    try:
        resp = 'Recently Updated Items as of ' + getDate() + '\n\n'
        rec = getRecent()
        for r in rec:
            resp+='#'+str(r[0])+' '+idToName(r[0])+ ' '
            if r[1] >= 1:
                resp+='+'+str(r[1])+'\n'
            else:
                resp+=str(r[1])+'\n'
        await ctx.send(resp)
        logging.info('Succesfully displayed recent items, user='+str(ctx.author))
    except:
        logging.error('Error displaying recent items, user='+str(ctx.author))

bot.run(TOKEN)