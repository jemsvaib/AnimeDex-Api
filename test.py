import time
from bs4 import BeautifulSoup as bs
import pymongo
import requests

mUrl = "mongodb+srv://TechZ:Bots@websitedata.wdycbvp.mongodb.net/?retryWrites=true&w=majority"

db = pymongo.MongoClient(mUrl).AnimeDex
viewsdb = db.views
topdb = db.top


working = {}
not_working = []


def top():
    global working, not_working
    data = []
    ignore = ["home-animedex", "search-animedex", "home-blackanime"]
    x = viewsdb.find({})
    d = []
    for i in x:
        d.append(
            {"anime": i.get("anime"), "views": i.get("views"), "watch": i.get("watch")}
        )
    d = sorted(
        d, key=lambda i: ((i.get("views") or 0) + (i.get("watch") or 0)), reverse=True
    )

    for i in d:
        if i.get("anime") == "one piece":
            i["anime"] = "one-piece"
        print(i, data, len(data))
        if i.get("anime") in ignore:
            continue
        try:
            res = requests.get("https://animedex.live/anime/" + i.get("anime"))
            print('<a class="ep-btn" href="/episode/' in res.text, res.status_code)
            if '<a class="ep-btn" href="/episode/' in res.text:
                soup = bs(res.text, "html.parser")
                h1 = soup.find("div", "details").find("h1")
                genre = soup.find("div", "genre").find("a")
                ep = soup.find_all("span", "item-des")[2]
                type = soup.find_all("span", "item-des")[4]
                status = soup.find_all("span", "item-des")[5]
                img = soup.find("div", "poster").find("img")
                data.append(
                    (
                        i.get("anime"),
                        [
                            h1.text if h1 else "None",
                            genre.text if genre else "None",
                            ep.text if ep else "None",
                            type.text if type else "None",
                            status.text if status else "None",
                            str(img.get("src")),
                        ],
                    )
                )
        except:
            continue

        if len(data) == 10:
            break
    print("Top Cache Updated...")

    topdb.update_one({"anime": "top"}, {"$set": {"top": data}}, upsert=True)


while True:
    try:
        top()
    except Exception as e:
        print(e)
    time.sleep(5 * 60)
