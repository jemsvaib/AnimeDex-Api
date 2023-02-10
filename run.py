import requests
from datetime import date
from flask import Flask, redirect, request
import pymongo

from gogo import get_GPage, get_html

mUrl = 'mongodb+srv://TechZ:Bots@websitedata.wdycbvp.mongodb.net/?retryWrites=true&w=majority'

db = pymongo.MongoClient(mUrl).AnimeDex
viewsdb = db.views
daydb = db.day
app = Flask(__name__)


@app.route('/')
def home():
    text = {}
    views = 0
    watch = 0
    t1, t2 = [0], [0]
    a1 = a2 = 0

    for i in viewsdb.find({}):
        x = i.get('views')
        y = i.get('watch')
        if x:
            a1 += 1
            views += x
            if x > t1[0] and i.get('anime') != 'home-animedex' and i.get('anime') != 'search-animedex':
                t1 = [x, i.get('anime')]

            if i.get('anime') == 'home-animedex':
                text['home page views'] = x
            elif i.get('anime') == 'search-animedex':
                text['searches'] = x
        if y:
            a2 += 1
            watch += y
            if y > t2[0] and i.get('anime') != 'home-animedex' and i.get('anime') != 'search-animedex':
                t2 = [y, i.get('anime')]
    text['total views'] = views + watch

    text['views'] = {}
    text['views']['anime'] = views
    text['views']['episode'] = watch

    text['top'] = {}
    text['top']['anime'] = t1
    text['top']['episode'] = t2

    text['pages opened'] = {}
    text['pages opened']['anime'] = a1
    text['pages opened']['episode'] = a2

    text['per day'] = []

    for i in daydb.find({}):
        text['per day'].append(str(i))
    return text


count = 0
top_cache = []


@app.route('/top')
def top():
    global count
    global top_cache
    count += 1

    if count < 100:
        return {'data': top_cache}
    count = 0

    data = []
    ignore = ['home-animedex', 'search-animedex', 'home-blackanime']
    for i in viewsdb.find({}).sort([('views', -1), ('watch', -1)]):
        if i.get('anime') in ignore:
            continue
        try:
            if '<a class="ep-btn" href="/episode/' in requests.get('https://animedex.live/anime/' + i.get('anime')).text:
                data.append(i)
        except:
            pass
        if len(data) == 10:
            break
    top_cache = data
    return {'data': data}


@app.route('/db/view')
def saveView():
    anime = request.args.get('anime')
    if anime:
        anime = anime.strip()
        if anime != '':
            viewsdb.update_one({'anime': anime}, {
                               '$inc': {'views': 1}}, upsert=True)
            today = str(date.today())
            daydb.update_one({'day': today}, {
                '$inc': {'views': 1}}, upsert=True)
            return 'Success'
    return 'Something Went Wrong...'


@app.route('/db/watch')
def saveWatch():
    anime = request.args.get('anime')
    if anime:
        anime = anime.strip()
        if anime != '':
            viewsdb.update_one({'anime': anime}, {
                               '$inc': {'watch': 1}}, upsert=True)
            today = str(date.today())
            daydb.update_one({'day': today}, {
                '$inc': {'watch': 1}}, upsert=True)
            return 'Success'
    return 'Something Went Wrong...'


@app.route('/latest/<page>')
def latest(page):
    try:
        data = get_GPage(page)
        html = get_html(data)
        return {'html': html}
    except:
        return {'html': ''}


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
