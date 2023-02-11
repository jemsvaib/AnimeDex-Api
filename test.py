import time
from bs4 import BeautifulSoup as bs
import pymongo
import requests
mUrl = 'mongodb+srv://TechZ:Bots@websitedata.wdycbvp.mongodb.net/?retryWrites=true&w=majority'

db = pymongo.MongoClient(mUrl).AnimeDex
viewsdb = db.views
topdb = db.top


working = {}
not_working = []


def top():
    global working, not_working
    data = {}
    ignore = ['home-animedex', 'search-animedex', 'home-blackanime']
    x = viewsdb.find({}).sort([('views', -1), ('watch', -1)])
    for i in x:
        if i.get('anime') == 'one piece':
            i['anime'] = 'one-piece'
        print(i, data, len(data))
        if i.get('anime') in ignore:
            continue
        try:
            if i.get('anime') in working:
                data[i.get('anime')] = working[i.get('anime')]
            elif i.get('anime') in not_working:
                continue
            else:
                res = requests.get(
                    'https://animedex.live/anime/' + i.get('anime'))
                print('<a class="ep-btn" href="/episode/' in res.text,
                      res.status_code)
                if '<a class="ep-btn" href="/episode/' in res.text:
                    soup = bs(res.text, 'html.parser')
                    h1 = soup.find('div', 'details').find('h1')
                    genre = soup.find('div', 'genre').find('a')
                    ep = soup.find_all('span', 'item-des')[2]
                    type = soup.find_all('span', 'item-des')[4]
                    status = soup.find_all('span', 'item-des')[5]
                    img = soup.find('div', 'poster').find('img')

                    data[i.get('anime')] = [h1.text if h1 else 'None', genre.text if genre else 'None', ep.text if ep else 'None',
                                            type.text if type else 'None', status.text if status else 'None', str(img.get('src'))]
                    working[i.get('anime')] = data.get('anime')
        except:
            not_working.append(i.get('anime'))
            continue

        if len(data) == 10:
            break
    print('Top Cache Updated...')

    topdb.update_one({'anime': 'top'}, {'$set': {'top': data}}, upsert=True)


while True:
    try:
        top()
    except:
        pass
    time.sleep(10 * 60)
