import os
from discord.ext import commands
from dotenv import load_dotenv
import discord
import pymongo

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

bot.run(TOKEN)