import requests as r
import matplotlib.pyplot as plt
import random
from string import hexdigits

cache = []


def hash():
    while True:
        hash = "".join(random.choices(hexdigits, k=10))
        if hash not in cache:
            cache.append(hash)
            break
    return hash


def day():
    a = r.get("https://api.animedex.live").json()["per day"]

    total = []
    anime = []
    ep = []

    for i in a:
        s1 = i["watch"]
        s2 = i["views"]

        total.append(s1 + s2)
        anime.append(s2)
        ep.append(s1)

    plt.plot(total, label="Total")
    plt.plot(anime, label="Anime")
    plt.plot(ep, label="Episode")

    plt.title("AnimeDex Stats Graph | Per Day Views")
    plt.xlabel("Days")
    plt.ylabel("Views")
    plt.legend()
    n = hash() + ".jpg"
    plt.savefig(n)
    plt.close()
    return n


def over():
    a = r.get("https://api.animedex.live").json()["per day"]

    total = []
    anime = []
    ep = []

    x1, x2, x3 = 0, 0, 0

    for i in a:
        s1 = i["watch"]
        s2 = i["views"]

        x1 += s1 + s2
        x2 += s1
        x3 += s2
        total.append(x1)
        anime.append(x3)
        ep.append(x2)

    plt.plot(total, label="Total")
    plt.plot(anime, label="Anime")
    plt.plot(ep, label="Episode")

    plt.title("AnimeDex Stats Graph | Overall Views")
    plt.xlabel("Days")
    plt.ylabel("Views (In Millions)")
    plt.legend()
    n = hash() + ".jpg"
    plt.savefig(n)
    plt.close()
    return n