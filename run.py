import requests
from datetime import date
from flask import Flask, redirect, request, send_file
import pymongo

from gogo import get_GPage, get_html

mUrl = "mongodb+srv://TechZ:Bots@websitedata.wdycbvp.mongodb.net/?retryWrites=true&w=majority"

db = pymongo.MongoClient(mUrl).AnimeDex
viewsdb = db.views
daydb = db.day
app = Flask(__name__)

techzdb = pymongo.MongoClient(
    "mongodb+srv://techz:bots@cluster0.uzrha.mongodb.net/?retryWrites=true&w=majority"
).techzapi.userdb


@app.route("/")
def home():
    text = {}
    views = 0
    watch = 0
    t1, t2 = [0], [0]
    a1 = a2 = 0

    for i in viewsdb.find({}):
        x = i.get("views")
        y = i.get("watch")
        if x:
            a1 += 1
            views += x
            if (
                x > t1[0]
                and i.get("anime") != "home-animedex"
                and i.get("anime") != "search-animedex"
            ):
                t1 = [x, i.get("anime")]

            if i.get("anime") == "home-animedex":
                text["home page views"] = x
            elif i.get("anime") == "search-animedex":
                text["searches"] = x
        if y:
            a2 += 1
            watch += y
            if (
                y > t2[0]
                and i.get("anime") != "home-animedex"
                and i.get("anime") != "search-animedex"
            ):
                t2 = [y, i.get("anime")]
    text["total views"] = views + watch

    text["views"] = {}
    text["views"]["anime"] = views
    text["views"]["episode"] = watch

    text["top"] = {}
    text["top"]["anime"] = t1
    text["top"]["episode"] = t2

    text["pages opened"] = {}
    text["pages opened"]["anime"] = a1
    text["pages opened"]["episode"] = a2

    text["per day"] = []

    for i in daydb.find({}):
        text["per day"].append(
            {"day": i.get("day"), "views": i.get("views"), "watch": i.get("watch")}
        )
    return text


topdb = db.top
from stats import day, over


@app.route("/top")
def top():
    return {"top": topdb.find_one({"anime": "top"}).get("top")}


@app.route("/stats/day")
def day_():
    img = day()
    return send_file(img, mimetype="image/jpg")


@app.route("/stats/over")
def over_():
    img = over()
    return send_file(img, mimetype="image/jpg")


def increment_techz(key, data):
    animedex = data.get("animedex")
    if not animedex:
        animedex = []

    try:
        animedex = int(animedex)
        animedex = []
    except:
        pass

    today = str(date.today())

    if today not in animedex:
        animedex[today] = 1
    else:
        animedex[today] += 1

    techzdb.update_one({"api_key": key}, {"$inc": {"animedex": animedex}}, upsert=True)


@app.route("/db/view")
def saveView():
    anime = request.args.get("anime")
    key = request.args.get("key")

    data = techzdb.find_one({"api_key": key})
    if not data:
        return "Invalid Key"

    if anime:
        anime = anime.strip()
        if anime != "":
            viewsdb.update_one({"anime": anime}, {"$inc": {"views": 1}}, upsert=True)
            today = str(date.today())
            daydb.update_one({"day": today}, {"$inc": {"views": 1}}, upsert=True)

            increment_techz(key, data)

            return "Success"
    return "Something Went Wrong..."


@app.route("/db/watch")
def saveWatch():
    anime = request.args.get("anime")
    key = request.args.get("key")

    data = techzdb.find_one({"api_key": key})
    if not data:
        return "Invalid Key"

    if anime:
        anime = anime.strip()
        if anime != "":
            viewsdb.update_one({"anime": anime}, {"$inc": {"watch": 1}}, upsert=True)
            today = str(date.today())
            daydb.update_one({"day": today}, {"$inc": {"watch": 1}}, upsert=True)

            increment_techz(key, data)

            return "Success"
    return "Something Went Wrong..."


@app.route("/latest/<page>")
def latest(page):
    try:
        data = get_GPage(page)
        html = get_html(data)
        return {"html": html}
    except:
        return {"html": ""}


if __name__ == "__main__":
    app.run()
