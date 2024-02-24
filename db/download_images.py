import re
import requests
import pymongo


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
    return formatted_output.strip().replace(' ', '-')

items = db['bank'].find()

for item in items:
    url = 'https://celticheroesdb.com/_images/item/' + str(item['db_id']) + '_' + str(format_item(str(item['item_name']))) + '.png'
    img_data = requests.get(url).content
    iname = 'images/'+str(item['id'])+'.png'
    with open(iname, 'wb') as handler:
        handler.write(img_data)
