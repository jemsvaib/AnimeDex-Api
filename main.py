from flask import Flask, redirect, request
import pymongo

mUrl = 'mongodb+srv://TechZ:Bots@websitedata.wdycbvp.mongodb.net/?retryWrites=true&w=majority'

db = pymongo.MongoClient(mUrl).AnimeDex
viewsdb = db.views
app = Flask(__name__)


@app.route('/')
def home():
    return redirect('https://anime-dex1.vercel.app')


@app.route('/db/save')
def saveToDB():
    anime = request.args.get('anime')
    if anime:
        anime = anime.strip()
        if anime != '':
            viewsdb.update_one({'anime': anime}, {'$inc': {'views': 1}},upsert = True)
            return 'Success'
    return 'Something Went Wrong...'