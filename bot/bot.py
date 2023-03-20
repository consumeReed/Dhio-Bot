import os
from discord.ext import commands
from dotenv import load_dotenv
import discord
import pymongo
from datetime import datetime

classes = ['mage', 'druid', 'warrior', 'rogue', 'ranger']

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dhio']

def getItems(substr):

    if substr.lower() in classes: 
        col = db['bank']
        rec = col.find({'class': substr.lower()}, {'_id': 0})
        l = []
        for it in rec:
            if(it['amount']> 0):
                l.append([it['id'], it['item_name'], it['amount']])
        return l

    else:
        col = db['bank']
        rec = col.find({'item_name': { '$regex': '.*'+substr.lower()+'.*'}}, {'_id': 0})
        l = []
        for it in rec:
            if(it['amount']> 0):
                l.append([it['id'], it['item_name'], it['amount']])
        return l

def getDate():
    col = db['date']
    r = col.find({'id': 1})
    return 'Bot Last Updated at ' + str(r[0]['date'].strftime('%I:%M%p on %B %d %Y'))

def getIds(ch):
    col = db['bank']
    rec = col.find({'class': ch}, {'_id': 0})
    l = []
    for it in rec:
        l.append([it['id'], it['item_name']])
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

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='!')

@bot.command(name='find', help='Search the available dhio items banked. Input either item name or class')
async def bank(ctx, *, search):
    db = client['dhio']
    r = getItems(search)
    resp = getDate() + "\n\n"
    if(len(r) == 0):
        resp += 'No Results'
    for i in r:
        resp += "#"+ str(i[0]) +" " + i[1] + "   "  + str(i[2])  +  "\n"
    await ctx.send(resp)

@bot.command(name='image', help='Input item id to see stats as an image')
async def im(ctx, search):
    if str(search).isnumeric():
        if int(search) < 299:
            await ctx.send(file=discord.File('images/'+str(search)+'.PNG'))

@bot.command(name='show', help='Input item id to see stats as an image')
async def im(ctx, search):
    if str(search).isnumeric():
        if int(search) < 299:
            await ctx.send(file=discord.File('images/'+str(search)+'.PNG'))

@bot.command(name='update')
async def up(message, *, search):
    if message.author == bot.user:
        return
    if message.author.id == 148113452534202368:
        inp = str(search).split()
        #out = 'id: '+ str(inp[0]) + '   quantity: '+ str(inp[1])
        addToBank(int(inp[0]), int(inp[1]))
        changeDate()

@bot.command(name='ids', help='Shows ids of items')
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
                resp+= str(i[0]) + '  ' + i[1]+"\n"
            else:
                resp2+= str(i[0]) + '  ' + i[1]+"\n"
        
        await ctx.send(resp)
        await ctx.send(resp2)
    else:
        items = getIdsName(search)
        resp = ''
        for i in items:
            resp+=str(i[0]) + '  ' + i[1]+'\n'
        await ctx.send(resp)

bot.run(TOKEN)