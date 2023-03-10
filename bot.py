import os
from discord.ext import commands
from dotenv import load_dotenv
import discord
import pymongo

mage = ['flames', 'ice shards', 'ice blast', 'blizzards', 'wand', 'firestorm', 'laceration', 'contusion', 'fire bolt']
druid = ['opposition', 'lightning', 'seer', 'breath', 'touch', 'resistance', 'storm', 'totem', 'sage']
warrior = ['shield', 'rupture', 'viking', 'valor', 'sword', 'hammer', 'axe', 'knights', 'barbarian', 'pummel', 'taunt']
ranger = ['shot', 'archer', 'hunter', 'bow']
rogue = ['of shadows', 'ass', 'sneaky', 'dagger', 'quick', 'brawlers']

d = {"mage": mage, "druid": druid, "warrior": warrior, "ranger": ranger, "rogue": rogue}

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dhio']
def getItems(substr):
    it = d.get(substr)
    if it is None:
        col = db['bank']
        rec = col.find({'item_name': { '$regex': '.*'+substr.lower()+'.*'}}, {'_id': 0})
        l = []
        for it in rec:
            if(it['item']> 0):
                l.append([it['item_name'], it['amount']])
        return l
    else:
        l = []
        for i in it:
            l.extend(getItems(i))
        return l

def getDate():
    col = db['date']
    r = col.find({'id': 1})
    return 'Bot Last Updated at ' + str(r[0]['date'].strftime('%I:%M%p on %B %d %Y'))


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='!')

@bot.command(name='find', help='Search the available dhio items banked.')
async def bank(ctx, *, search):
    db = client['dhio']
    r = getItems(search)
    resp = getDate() + "\n\n"
    if(len(r) == 0):
        resp += 'No Results'
    for i in r:
        resp += i[0] + "   "  + str(i[1])  +  "\n"
    await ctx.send(resp)

bot.run(TOKEN)