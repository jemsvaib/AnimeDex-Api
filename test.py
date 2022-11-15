import pymongo

mUrl = 'mongodb+srv://TechZ:Bots@websitedata.wdycbvp.mongodb.net/?retryWrites=true&w=majority'

db = pymongo.MongoClient(mUrl).AnimeDex
viewsdb = db.views

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


print(views,watch)  
print(t1,t2)  
print(a1,a2)