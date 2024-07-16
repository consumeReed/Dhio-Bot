import os
from discord.ext import commands
from dotenv import load_dotenv
import discord
import pymongo
from datetime import datetime
import logging
import json

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename="Logs.log")

classes = {'mage': 3, 'druid': 2, 'warrior': 1, 'rogue': 5, 'ranger': 4}

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dhio']

def get_date():
    col = db['date']
    r = col.find({'id': 1})
    return str(r[0]['date'].strftime('%I:%M%p on %B %d %Y'))

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

def get_items_ids_formatted(item_substring, bank_type):
    col = db['bank']
    query = col.find({'item_name': {'$regex': '.*'+item_substring.lower()+'.*'}, 'bank': str(bank_type)}, {'_id': 0})
    response = 'Matching items for: ' + str(item_substring)+'\n\n'
    list_ = list(query)
    if len(list_) == 0:
        response+='No matches'
        return response
    for item in list_:
         response+='#' + str(item['id']) + ' ' + format_item(item['item_name']) + '\n'
    return response


def get_items_name(item_substring, bank_type):
    col = db['bank']
    query = col.find({'item_name': {'$regex': '.*'+item_substring.lower()+'.*'}, 'bank': bank_type, 'amount': {'$gt': 0}}, {'_id': 0})
    return query

def increment_search(discord_id, discord_name, query_type):
    col = db['users']
    query = col.find_one({'discord_id': discord_id})
    if query is None and query_type == 1:
        col.insert_one({"discord_id": int(discord_id), "discord_name": str(discord_name), "privilege": 0, "queries": 1, "image_queries": 0})
    elif query is None and query_type == 2:
        col.insert_one({"discord_id": int(discord_id), "discord_name": str(discord_name), "privilege": 0, "queries": 0, "image_queries": 1})
    elif query_type == 1:
        col.update_one({'discord_id': int(discord_id)}, {'$inc': {'queries': 1}})
    elif query_type == 2:
        col.update_one({'discord_id': int(discord_id)}, {'$inc': {'image_queries': 1}})

def get_items_formatted(search, bank_type, discord_id, discord_name):
    increment_search(discord_id, discord_name, 1)
    col = db['bank']
    items = []
    if search.lower() in classes:
        items = list(get_items_class(classes[search.lower()], bank_type))
    else:
        items = list(get_items_name(search, bank_type))
    response = 'Bot Last Updated at ' + get_date() + '\n\n'
    if len(items) == 0:
        response+='No Results'
    else:
        for item in items:
            response+='#' + str(item['id']) + ' ' + format_item(id_to_name(int(item['id']))) + "  " + str(item['amount'])+'\n'
    return response

def id_to_name(item_id):
    col = db['bank']
    query = col.find_one({'id': item_id}, {'_id': 0})
    return query['item_name']

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
    query = col.find_one({'bank_id': bank_name})
    return query['on']

def set_active(bank_name, on):
    col = db['active']
    col.update_one({'bank_id': bank_name}, {'$set': {'on': on}})

def get_active():
    col = db['active']
    query = col.find()
    print(query)
    return query

def get_privilege_users(privilege_level):
    col = db['users']
    query = col.find({'privilege': {'$gte': privilege_level}})
    return query

async def update_privilege(discord_id, privilege_level, discord_name):
    col = db['users']
    if str(discord_id) != 'name':
        query = col.find_one({'discord_id': int(discord_id)})
        if query == None:
            col.insert_one({'discord_id': int(discord_id), 'discord_name': discord_name, 'privilege': privilege_level, 'queries': 0, 'image_queries': 0})
        else:
            col.update_one({'discord_id': int(discord_id)}, {'$set': {'privilege': privilege_level}})
    else:
        query = col.find_one({'discord_name': str(discord_name)})
        if query != None:
            col.update_one({'discord_name': str(discord_name)}, {'$set': {'privilege': privilege_level}})

def update_query(discord_id):
    col = db['users']
    col.update_one({'discord_id': discord_id}, {'$inc': {'queries': 1}})

def update_image_queries(discord_id):
    col = db['users']
    col.update_one({'discord_id': discord_id}, {'$inc': {'image_queries': 1}})

def get_statistics(discord_id):
    queries = [0,0,0]
    col = db['users']
    if discord_id == -1:
        query = col.find()
        for user in query:
            queries[0]=queries[0]+user['queries']
            queries[1]=queries[1]+user['image_queries']
            queries[2]=queries[2]+1
    elif str(discord_id).isnumeric():
        query = col.find_one({'discord_id': discord_id})
        queries[0]=query['queries']
        queries[1]=query['image_queries']
    else:
        query = col.find_one({'discord_name': str(discord_id)})
        queries[0]=query['queries']
        queries[1]=query['image_queries']
    return queries

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='!')

@bot.command(name='kill', help='Kill a Dhiothu and see what loot you got!')
async def kill(message):
    await message.send('This command has been discontinued.')

@bot.command(name='find', help='Search the available Dhiothu items banked. Input either item name or class')
async def find(message):
    await message.send('This command has been discontinued.'
                 +'\nUse bank specific commands:'
                 +'\n!dhio, !hippo, !prot,'
                 +'\n!mord, !bt, !gele')

@bot.command(name='show', help='Input item id to see stats as an image')
async def show(ctx, search):
    try:
        if str(search).isnumeric():
            increment_search(ctx.author.id, ctx.author.name, 2)
            await ctx.send(file=discord.File('images/'+str(search)+'.PNG'))
            logging.info('Successfully displayed image, user='+str(ctx.author)+', image #'+str(search))
    except:
        await ctx.send('Invalid input, try command again.')
        logging.error('Error displaying item image, user='+str(ctx.author)+', image #'+str(search))      

@bot.command(name='update', help='Update quantities of items in bank')
async def update(message, *, search):
    try:
        message_author = message.author.id
        if message_author == bot.user:
            return
        for user in get_privilege_users(1):
            print(message_author)
            print(user)
            if int(user['discord_id']) == message_author:
                print('good')
                inputs = str(search).split()
                modifer = '+'
                if int(inputs[1]) < 0:
                    modifer = ''
                update_item_amount(int(inputs[0]), int(inputs[1]))
                logging.info("Updated bank item, user="+str(message.author)+", query=["+search+"]")
                await message.send(format_item(id_to_name(int(inputs[0])))+' '+modifer+str(inputs[1]))
                return
        await message.send('You are not eligible to use the update command')
        logging.warning("Unauthorized user tried to update items, user="+str(message.author))
    except Exception as e:
        logging.error("Error updating item quantities, user="+str(message.author)+", query=["+search+"]")
        await message.send('Error updating item quantities')

@bot.command(name='privilege', help='Update the privilege level of a user')
async def privilege(message, *, search):
    try:
        message_author = message.author.id
        if message_author == bot.user:
            return
        for user in get_privilege_users(2):
            if int(user['discord_id']) == message_author:
                inputs = str(search).split()
                if str(inputs[0]).isnumeric():
                    name = await bot.fetch_user(int(inputs[0]))
                    await update_privilege(int(inputs[0]), int(inputs[1]), str(name))
                    await message.send('Successfully updated privilege for ' + str(name) + ' to level ' + str(inputs[1]))
                else:
                    await update_privilege('name', int(inputs[1]), str(inputs[0]))
                    await message.send('Successfully updated privilege for ' + str(inputs[0]) + ' to level ' + str(inputs[1]))
                logging.info('Updated user '+ str(inputs[0]) + ' to level ' + str(inputs[1]) + ' by ' + str(message.author))

    except:
            logging.info('Error updating privilege level')

@bot.command(name='privilege_list', help='Get list of privileged users')
async def privilege_list(message):
    try:
        message_author = message.author.id
        if message_author == bot.user:
            return
        response = ""
        for user in get_privilege_users(2):
            if int(user['discord_id']) == message_author:
                privilege_list = get_privilege_users(1)
                for user in privilege_list:
                    response+=str(user['discord_name']) + ' is level ' + str(user['privilege']) + '\n'
            break
        if response != "":
            await message.send(response)
    except:
        logging.error('Error displaying privilege list')

@bot.command(name='bt', help='Search the available Bloodthorn items banked. Input either item name or class')
async def find_bt(ctx, *, search):
    try:
        if get_is_active('bloodthorn'):
            await ctx.send(get_items_formatted(search, 'bloodthorn', ctx.author.id, ctx.author))
        else:
            await ctx.send('Bloodthorn bank is disabled currently')
        logging.info("Successfully fulfilled bt search, user="+str(ctx.author)+", query="+search)
    except Exception as e:
        logging.error("Error doing find query for Bloodthorn. Search is: "+ str(search)+ ' by user: '+str(ctx.author))

@bot.command(name='mord', help='Search the available Mordris items banked. Input either item name or class')
async def find_mord(ctx, *, search):
    try:
        if get_is_active('mordris'):
            await ctx.send(get_items_formatted(search, 'mordris', ctx.author.id, ctx.author))
        else:
            await ctx.send('Mordris bank is disabled currently')
        logging.info("Successfully fulfilled mord search, user="+str(ctx.author)+", query="+search)
    except:
        logging.error("Error doing find query for Mordris. Search is: "+ str(search)+ ' by user: '+str(ctx.author))

@bot.command(name='prot', help='Search the available Proteus items banked. Input either item name or class')
async def find_prot(ctx, *, search):
    try:
        if get_is_active('proteus'):
            await ctx.send(get_items_formatted(search, 'proteus', ctx.author.id, ctx.author))
        else:
            await ctx.send('Proteus bank is disabled currently')
        logging.info("Successfully fulfilled prot search, user="+str(ctx.author)+", query="+search)
    except:
        logging.error("Error doing find query for Proteus. Search is: "+ str(search)+ ' by user: '+str(ctx.author))

@bot.command(name='hippo', help='Search the available Hrungnir items banked. Input either item name or class')
async def find_hippo(ctx, *, search):
    try:
        if get_is_active('hrungnir'):
            await ctx.send(get_items_formatted(search, 'hrungnir', ctx.author.id, ctx.author))
        else:
            await ctx.send('Hippo bank is disabled currently')
        logging.info("Successfully fulfilled hippo search, user="+str(ctx.author)+", query="+search)
    except:
        logging.error("Error doing find query for Hrungnir. Search is: "+ str(search)+ ' by user: '+str(ctx.author))

@bot.command(name='gele', help='Search the available Gelebron items banked. Input either item name or class')
async def find_gele(ctx, *, search):
    try:
        if get_is_active('gelebron'):
            await ctx.send(get_items_formatted(search, 'gelebron', ctx.author.id, ctx.author))
        else:
            await ctx.send('Gelebron bank is disabled currently')
        logging.info("Successfully fulfilled gele search, user="+str(ctx.author)+", query="+search)
    except:
        logging.error("Error doing find query for Gelebron. Search is: "+ str(search)+ ' by user: '+str(ctx.author))

@bot.command(name='dhio', help='Search the available Dhiothu items banked. Input either item name or class')
async def find_dhio(ctx, *, search):
    try:
        if get_is_active('dhiothu'):
            await ctx.send(get_items_formatted(search, 'dhiothu', ctx.author.id, ctx.author))
        else:
            await ctx.send('Dhiothu bank is disabled currently')
        logging.info("Successfully fulfilled dhio search, user="+str(ctx.author)+", query="+search)
    except:
        logging.error("Error doing find query for Dhiothu. Search is: "+ str(search)+ ' by user: '+str(ctx.author))

@bot.command(name='statistics', help='Statistics about Dhio Bot')
async def stats(ctx, *, search):
    try:
        if search == 'all':
            user_stats = get_statistics(-1)
            response='Statistics about Dhio Bot:\n'+str(user_stats[0])+' Queries made for items\n'+str(user_stats[1])+' Images displayed\n'+str(user_stats[2])+' Unique users'
            await ctx.send(response)
        elif str(search).isnumeric():
            user_stats = get_statistics(int(search))
            name = await bot.fetch_user(int(search))
            response='Statistics about '+str(name)+'\n'+str(user_stats[0])+' Queries made for items\n'+str(user_stats[1])+' Images displayed'
            await ctx.send(response)
        else:
            user_stats = get_statistics(str(search))
            response='Statistics about '+str(search)+'\n'+str(user_stats[0])+' Queries made for items\n'+str(user_stats[1])+' Images displayed'
            await ctx.send(response)
    except:
        logging.error('Error displaying statistics, query is: '+ str(search))

@bot.command(name='dhioid', help='Discover id numbers for Dhiothu items')
async def dhio_id(ctx, *, search):
    try:
        response = get_items_ids_formatted(search, 'dhiothu')
        await ctx.send(response)
    except:
        logging.error('Error displaying dhio ids for: '+ str(search)+ ' by user: '+str(ctx.author))

@bot.command(name='mordid', help='Discover id numbers for Mordris items')
async def mord_id(ctx, *, search):
    try:
        response = get_items_ids_formatted(search, 'mordris')
        await ctx.send(response)
    except:
        logging.error('Error displaying mordris ids for: '+ str(search)+ ' by user: '+str(ctx.author))

@bot.command(name='protid', help='Discover id numbers for Proteus items')
async def prot_id(ctx, *, search):
    try:
        response = get_items_ids_formatted(search, 'proteus')
        await ctx.send(response)
    except:
        logging.error('Error displaying proteus ids for: '+ str(search)+ ' by user: '+str(ctx.author))

@bot.command(name='hippoid', help='Discover id numbers for Hippo items')
async def hippo_id(ctx, *, search):
    try:
        response = get_items_ids_formatted(search, 'hrungnir')
        await ctx.send(response)
    except:
        logging.error('Error displaying hrungnir ids for: '+ str(search)+ ' by user: '+str(ctx.author))

@bot.command(name='btid', help='Discover id numbers for Bloodthorn items')
async def bt_id(ctx, *, search):
    try:
        response = get_items_ids_formatted(search, 'bloodthorn')
        await ctx.send(response)
    except:
        logging.error('Error displaying bloodthorn ids for: '+ str(search)+ ' by user: '+str(ctx.author))

@bot.command(name='geleid', help='Discover id numbers for Gelebron items')
async def gele_id(ctx, *, search):
    try:
        response = get_items_ids_formatted(search, 'gelebron')
        await ctx.send(response)
    except:
        logging.error('Error displaying gelebron ids for: '+ str(search)+ ' by user: '+str(ctx.author))

@bot.command(name='get_previous')
async def get_previous(ctx, *, search):
    to_log=[]
    if ctx.author.name == 'consume_':
        channel = bot.get_channel(int(search))
        async for message in channel.history(limit=10000):
            if message.author.id != 900834045863280670:
                to_log.append(str(message.content)+' '+str(message.author.name)+' '+str(message.author.id))

    with open('previous_history.json', 'w') as f:
        json.dump(to_log, f)

bot.run(TOKEN)