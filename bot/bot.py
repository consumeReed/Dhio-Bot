import os
from discord.ext import commands
from dotenv import load_dotenv
import discord
import pymongo
from datetime import datetime

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


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='!')

@bot.command(name='find', help='Search the available dhio items banked. Input either item name or class')
async def bank(ctx, *, search):
    db = client['dhio']
    r = getItems(search)
    resp = 'Bot Last Updated at '+ getDate() + "\n\n"
    if(len(r) == 0):
        resp += 'No Results'
    for i in r:
        resp += "#"+ str(i[0]) +" " + i[1] + "   "  + str(i[2])  +  "\n"
    await ctx.send(resp)

@bot.command(name='bt', help='Shows the good BT gear in bank :3')
async def bt(ctx):
    r = getBt()
    resp = 'All the good BT items :3\n\n'
    if(len(r)== 0):
        resp+= 'No Results'
    for i in r:
        resp += "#"+ str(i[0]) +" " + i[1] + "   "  + str(i[2])  +  "\n"
    await ctx.send(resp)


@bot.command(name='show', help='Input item id to see stats as an image')
async def im(ctx, search):
    if str(search).isnumeric():
        if int(search) < 518:
            await ctx.send(file=discord.File('images/'+str(search)+'.PNG'))

@bot.command(name='update')
async def up(message, *, search):
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
        else:
            addToBt(int(inp[0]), int(inp[1]))
        await message.send(out)

@bot.command(name='btids', help='Shows ids of BT items')
async def u(ctx, search):
    items = getBtIdsName(search)
    resp = ''
    for i in items:
        resp+='#'+str(i[0]) + '  ' + i[1]+'\n'
    await ctx.send(resp)

@bot.command(name='ids', help='Shows ids of Dhio items')
async def i(ctx, search):
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
    else:
        items = getIdsName(search)
        resp = ''
        for i in items:
            resp+='#'+str(i[0]) + '  ' + i[1]+'\n'
        await ctx.send(resp)

@bot.command(name='recent', help='Shows the 10 most recently updated items')
async def r(ctx):
    resp = 'Recently Updated Items as of ' + getDate() + '\n\n'
    rec = getRecent()
    for r in rec:
        resp+='#'+str(r[0])+' '+idToName(r[0])+ ' '
        if r[1] >= 1:
            resp+='+'+str(r[1])+'\n'
        else:
            resp+=str(r[1])+'\n'
    await ctx.send(resp)
    
bot.run(TOKEN)