from datetime import date
from flask import Flask, redirect, request
import pymongo

mUrl = 'mongodb+srv://TechZ:Bots@websitedata.wdycbvp.mongodb.net/?retryWrites=true&w=majority'

db = pymongo.MongoClient(mUrl).AnimeDex
viewsdb = db.views
daydb = db.day
app = Flask(__name__)


@app.route('/')
def home():
    views = 0
    watch = 0
    t1,t2 = [0],[0]
    a1=a2=0

    for i in viewsdb.find({}):
        x = i.get('views')
        y = i.get('watch')
        if x:
            a1+=1
            views+=x
            if x > t1[0] and i.get('anime') != 'home-animedex':
                t1 = [x,i.get('anime')]
        if y:
            a2+=1
            watch+=y
            if y > t2[0] and i.get('anime') != 'home-animedex':
                t2 = [y,i.get('anime')]
    text = {}
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
        text['per day'].append(i)
    return text


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
