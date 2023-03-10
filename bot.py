import os
from discord.ext import commands
from dotenv import load_dotenv
import discord
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dhio']
def getItems(substr):
    col = db['bank']
    rec = col.find({'item_name': { '$regex': '.*'+substr.lower()+'.'}}, {'_id': 0})
    l = []
    for it in rec:
        if(it['amount'] > 0):
            l.append([it['item_name'], it['amount']])
    return l

def getDate():
    col = db['date']
    r = col.find({'id': 1})
    return 'Bot Last Updated ' + str(r[0]['date'])


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='!')

@bot.command(name='find', help='Search the available dhio items banked.')
async def bank(ctx, search):
    r = getItems(search)
    resp = getDate() + "\n\n"
    if(len(r) == 0):
        resp += 'No Results'
    for i in r:
        resp += i[0] + "   "  + str(i[1])  +  "\n"
    await ctx.send(resp)

bot.run(TOKEN)