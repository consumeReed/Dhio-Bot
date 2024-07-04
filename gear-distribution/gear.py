import discord
from discord.ext import commands
import pymongo
from datetime import datetime
from time import time
import sys

'''
won Pyroblast Godly bloodleaf charm of invocation


won july 3 2024 Pyroblast Godly bloodleaf charm of invocation 3


won
Pyroblast Godly bloodleaf charm of invocation
ReedHammer Voidsworn sword of earth 2


won july 3 2024
Pyroblast Godly bloodleaf charm of invocation
ReedHammer Voidsworn sword of earth 4


gear Pyroblast october 2023 sep 2024


gear Pyroblast
'''
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dhio']

#col.insert_one({'player': 'Admin', 'item': 'Shoreline Sword', 'time': 0, 'quantity': 1})

async def on_message(message):
    if message.channel == 'Gear Distribution':
        col = db['gear']
        text = message.content
        if text.startswith('won'):
            print('hi')
        elif text.startswith('gear'):
            try:
                split = text.split()
                result = col.find({'player': split[1]})

                period_start = 0
                period_end = sys.maxsize
                if len(split) > 2:
                    period_start = datetime.datetime(int(split[3]), month_string_to_number(split[2]), 1, 0, 0)
                    period_end = datetime.datetime(int(split[5]), month_string_to_number(split[4]), 1, 0, 0)
                    output = "Gear won for " + split[1] + " between " + split[2] + " " + split[3] + " and " + split[4] + " " + split[5] + ":\n\n"
                else:
                    output = "All gear won for " + split[1] + ":\n\n"

                for item in result:
                    if item['time'] >= period_start and item['time'] <= period_end:
                        if item['quantity'] > 1:
                            output += time.strftime("%b %d %Y") + " " + item['quantity'] + " " + item['item'] + "\n"
                        else:
                            output += time.strftime("%b %d %Y") + " " + item['item'] + "\n"
            except:
                await message.channel.send('Invalid gear input')
        else:
            await message.channel.send('Invalid input')


def month_string_to_number(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')