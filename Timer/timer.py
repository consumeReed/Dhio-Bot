import os
from discord.ext import commands
from dotenv import load_dotenv
import discord
import pymongo
import time
import logging
import json

#logging.basicConfig(level=logging.INFO,
#                    format="%(asctime)s %(levelname)s %(message)s",
#                    datefmt="%Y-%m-%d %H:%M:%S",
#                    filename="TimerLogs.log")

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['timer']
col = db['bosses']

#def set_respawn_and_window(boss, respawn, window):
#    col.update_one({'boss_name': {'$in':[str(boss).lower()]}}, {'$set': {'respawn': int(respawn)}, '$set': {'window': int(window)}})

def set_dead(boss, time, version):
    if version == 1:
        print()
    else:
        print()


intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)

def display_time(seconds, granularity=4):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


#col.insert_one({"boss_name": ["mordris", "mord", "mordy", "mordi"], "respawn_time": 1440, "window": 1440, "dead": 0})

def react():
    return "The react message"

def print_boss_1():
    now = int(time.time())
    output = "Elemental Bosses:\n\n"
    res = col.find()

    #with open('Timer/bosses.json') as file:
    #    res = json.load(file)

    for boss in res:
        output+=boss['boss_name'][0]+": "

        dead = boss['dead']
        respawn = boss['respawn_time']*60
        window = boss['window']*60

        if now > dead and now < dead + respawn:
            output+="Open in XXX\n"
        elif now > dead + respawn and now < dead + respawn + window:
            output+="Open for YYY\n"
        else:
            output+="Missing, last killed at ZZZ\n"
        
    return output

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_TIMER')
bot = commands.Bot(intents=discord.Intents.all(), command_prefix='!')


@bot.command(name='setup', help='Create the initial boss messages')
async def find_prot(ctx, *, channels):

    ids = str(channels).split()

    timerMsg1 = print_boss_1()
    timerMsg2 = print_boss_1() #Change me to 2
    reactMsg = react()

    reactMsgChannel = bot.get_channel(int(ids[0]))
    timerMsg1Channel = bot.get_channel(int(ids[1]))
    timerMsg2Channel = bot.get_channel(int(ids[2]))
    
    await reactMsgChannel.send(reactMsg)
    await timerMsg1Channel.send(timerMsg1) 
    await timerMsg2Channel.send(timerMsg2)

    async for message in reactMsgChannel.history(limit=1):
        reactMsgId = message.id

    async for message in timerMsg1Channel.history(limit=1):
        timerMsg1Id = message.id

    async for message in timerMsg2Channel.history(limit=1):
        timerMsg2Id = message.id

    #m = await reactMsgChannel.fetch_message(reactMsgId)
    #await m.edit(content = "hello world")


    
bot.run(TOKEN)

