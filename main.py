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
    return redirect('https://anime-dex1.vercel.app')


@app.route('/db/view')
def saveView():
    anime = request.args.get('anime')
    if anime:
        anime = anime.strip()
        if anime != '':
            viewsdb.update_one({'anime': anime}, {
                               '$inc': {'views': 1}}, upsert=True)
            today = date.today()
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
            today = date.today()
            daydb.update_one({'day': today}, {
                '$inc': {'watch': 1}}, upsert=True)
            return 'Success'
    return 'Something Went Wrong...'
