import os
from discord.ext import commands
from dotenv import load_dotenv
import discord
import pymongo
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename="Logs.log")

classes = {'mage': 3, 'druid': 2, 'warrior': 1, 'rogue': 5, 'ranger': 4}

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dhio']

def format_item(item):
    formatted_output = ''
    l = item.split(' ')
    for word in l:
        if word != 'of' and word != 'the':
            formatted_output+= word.capitalize() + ' '
        else:
            formatted_output+=word +' '
    return formatted_output

def get_items_class(ch_class, bank_type):
    col = db['bank']
    query = col.find({'class':{'$in':[ch_class]}, 'bank': bank_type, 'amount': {'$gt': 0}}, {'_id': 0})
    return query

def get_items_name(item_substring, bank_type):
    col = db['bank']
    query = col.find({'item_name': {'$regex': '.*'+item_substring.lower()+'.*'}, 'bank': bank_type, 'amount': {'$gt': 0}}, {'_id': 0})
    return query

def get_items_formatted(search, bank_type):
    col = db['bank']
    items = []
    if search.lower() in classes:
        items = get_items_class(classes[search.lower()], bank_type)
    else:
        items = get_items_name(search, bank_type)
    response = 'Bot Last Updated at ' + '\n\n'
    if len(items) == 0:
        response+='No Results'
    else:
        for item in items:
            response+='#' + format_item(str(item['id'])) + " " + str(item['amount'])
    return response
        


def id_to_name(item_id):
    col = db['bank']
    query = col.find({'id': id}, {'_id': 0})
    return query[0]['item_name']

def update_item_amount(item_id, modifier):
    col = db['bank']
    col.update_one({'id': item_id}, {'$inc': {'amount': modifier}})
    col = db['recent']
    col.insert_one({'id': item_id, 'changed': modifier})
    update_date()

def update_date():
    col = db['date']
    col.update_one({'id': 1}, {'$set': {'date': datetime.today()}})

def get_recently_updated():
    col = db['recent']
    query = col.find().limit(10).sort("_id", -1)
    return query

def get_is_active(bank_name):
    col = db['active']
    query = col.find({'bank_id': bank_name})
    return query['on']

def set_active(bank_name, on):
    col = db['active']
    col.update_one({'bank_id': bank_name}, {'on': on})

def get_active():
    col = db['active']
    return col.find()

def get_privilege_users(privilege_level):
    col = db['users']
    query = col.find({'privilege': {'$gte': privilege_level}})
    return query

def update_privilege(discord_id, privilege_level):
    col = db['users']
    col.update_one({'discord_id': discord_id}, {'privilege': privilege_level})

def update_query(discord_id):
    col = db['users']
    col.update_one({'discord_id': discord_id}, {'$inc': {'queries': 1}})

def update_image_queries(discord_id):
    col = db['users']
    col.update_one({'discord_id': discord_id}, {'$inc': {'image_queries': 1}})

def get_statistics(discord_id):
    col = db['users']
    if discord_id == -1:
        query = col.find()
        #cont

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='!')

@bot.command(name='kill', help='Kill a Dhiothu and see what loot you got!')
async def kill(message):
    message.send('This command has been discontinued.')

@bot.command(name='find', help='Search the available Dhiothu items banked. Input either item name or class')
async def find(message):
    message.send('This command has been discontinued.'
                 +'\nUse bank specific commands:'
                 +'\n!dhio, !hippo, !prot,'
                 +'\n!mord, !bt, !gele')

@bot.command(name='show', help='Input item id to see stats as an image')
async def show(ctx, search):
    try:
        if str(search).isnumeric():
            await ctx.send(file=discord.File('images/'+str(search)+'.PNG'))
            logging.info('Successfully displayed image, user='+str(ctx.author)+', image #'+str(search))
    except:
        await ctx.send('Invalid input, try command again.')
        logging.error('Error displaying item image, user='+str(ctx.author)+', image #'+str(search))      

@bot.command(name='update', help='Update quantities of items in bank')
async def update(message, *, search):
    try:
        message_author = message.author
        if message_author == bot.user:
            return
        for user in get_privilege_users(1):
            if user['discord_id'] == message_author:
                inputs = str(search).split()
                modifer = '+'
                if int(inputs[1]) < 0:
                    modifer = ''
                update_item_amount(int(inputs[0], int(inputs[1])))
                logging.info("Updated bank item, user="+str(message.author)+", query=["+search+"]")
                await message.send(id_to_name(int(inputs[0]))+' '+modifer+str(inputs[1]))
                return
        await message.send('You are not eligible to use the update command')
        logging.warning("Unauthorized user tried to update items, user="+str(message.author))
    except:
        logging.error("Error updating item quantities, user="+str(message.author)+", query=["+search+"]")
        await message.send('Error updating item quantities')

@bot.command(name='privilege', help='Update the privilege level of a user')
async def privilege(message, *, search):
    try:
        message_author = message.author
        if message_author == bot.user:
            return
        for user in get_privilege_users(2):
            if user['discord_id'] == message_author:
                inputs = str(search).split()
                update_privilege(float(inputs[0]), int(inputs[1]))
                message.send('Successfully updated privilege for ' + await client.fetch(float(inputs[0])) + ' to level ' + str(inputs[1]))
                logging.info('Updated user '+ str(inputs[0]) + ' to level ' + str(inputs[1]) + ' by ' + message.author)
    except:
        logging.info('Error updating privilege level')

@bot.command(name='privilege_list', help='Get list of privileged users')
async def privilege_list(message):
    try:
        message_author = message.author
        if message_author == bot.user:
            return
        for user in get_privilege_users(2):
            if user['discord_id'] == message_author:
                response = "Users and their privilege level:\n"
                privilege_list = get_privilege_users(1)
                for user in privilege_list:
                    response+=await client.fetch(user['discord_id']) + ' is level ' + user['privilege']
            await message.send(response)
    except:
        logging.error('Error displaying privilege list')

@bot.command(name='bt', help='Search the available Bloodthorn items banked. Input either item name or class')
async def find(ctx, *, search):
    if get_is_active('bloodthorn'):
        await ctx.send(get_items_formatted(search, 'bloodthorn'))
    else:
        await ctx.send('Bloodthorn bank is disabled currently')
    logging.info("Successfully fulfilled bt search, user="+str(ctx.author)+", query="+search)

@bot.command(name='mord', help='Search the available Mordris items banked. Input either item name or class')
async def find(ctx, *, search):
    if get_is_active('mordris'):
        await ctx.send(get_items_formatted(search, 'mordris'))
    else:
        await ctx.send('Mordris bank is disabled currently')
    logging.info("Successfully fulfilled mord search, user="+str(ctx.author)+", query="+search)

@bot.command(name='prot', help='Search the available Proteus items banked. Input either item name or class')
async def find(ctx, *, search):
    if get_is_active('proteus'):
        await ctx.send(get_items_formatted(search, 'proteus'))
    else:
        await ctx.send('Proteus bank is disabled currently')
    logging.info("Successfully fulfilled prot search, user="+str(ctx.author)+", query="+search)

@bot.command(name='hippo', help='Search the available Hrungnir items banked. Input either item name or class')
async def find(ctx, *, search):
    if get_is_active('hrungnir'):
        await ctx.send(get_items_formatted(search, 'hrungnir'))
    else:
        await ctx.send('Hippo bank is disabled currently')
    logging.info("Successfully fulfilled hippo search, user="+str(ctx.author)+", query="+search)

@bot.command(name='gele', help='Search the available Gelebron items banked. Input either item name or class')
async def find(ctx, *, search):
    if get_is_active('gelebron'):
        await ctx.send(get_items_formatted(search, 'gelebron'))
    else:
        await ctx.send('Gelebron bank is disabled currently')
    logging.info("Successfully fulfilled gele search, user="+str(ctx.author)+", query="+search)

@bot.command(name='dhio', help='Search the available Dhiothu items banked. Input either item name or class')
async def find(ctx, *, search):
    if get_is_active('dhiothu'):
        await ctx.send(get_items_formatted(search, 'dhiothu'))
    else:
        await ctx.send('Dhiothu bank is disabled currently')
    logging.info("Successfully fulfilled dhio search, user="+str(ctx.author)+", query="+search)