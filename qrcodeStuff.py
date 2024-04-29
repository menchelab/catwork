import csv
import json
import random, string
import qrcode
import qrcode.image.svg
'''
fd = open('participants.csv', encoding="utf8")
reader = csv.DictReader(fd)

participants = {}
participants["users"] = list(reader)
print(participants["users"][0]["Full Name"])
'''

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def makeqrcode(uid):
        data = 'https://catwork.azurewebsites.net/main?uid=' + uid
        img = qrcode.make( data, box_size=40, image_factory=qrcode.image.svg.SvgImage, version=2)
        img.save('static/qrcodes/uid_'+ str(uid) +'.svg')

        
def makeqrcodes():

    f = open('dataNew.json')
    myusers = json.load(f)
    f.close()

    for i in myusers["users"]:
    # Data to be encoded
        data = 'https://catwork.azurewebsites.net/main?uid=' + str(i["id"])
        #data = 'https://catwork.azurewebsites.net/main?uid=' + str(i["id"])
        # Encoding data using make() function
        #img = qrcode.make(data)
        img = qrcode.make( data, box_size=40, image_factory=qrcode.image.svg.SvgImage, version=2)
        
        # Saving as an image file
        img.save('static/qrcodes/uid_'+ str(i["id"]) +'.svg')

#makeqrcodes()

def make_dummy_data():
    myusers = {}
    myusers["users"]= []
    myusers["links"]= [(0,1)]
    '''
    fd = open('participants.csv', encoding="utf8")
    reader = csv.DictReader(fd)

    participants["users"] = list(reader)
    '''

    for u in range (50):
        user ={}
        #user["name"] = participants["users"][u]["Full Name"]
        user["name"] = "cat #" + str(u)
        user["id"] = randomword(4)
        user["pw"] = randomword(3)
        user["score"] = 0
        myusers["users"].append(user)

    for i in range(100):
        #start = random.randint(0,len(myusers["users"])-1)
        #end = random.randint(0,len(myusers["users"])-1)
        start = random.randint(0,49)
        end = random.randint(0,49)
        myusers["links"].append([start, end])
        myusers["users"][start]["score"] += 1

    with open('dataNew.json', 'w') as f:
        json.dump(myusers, f) 
#print(myusers)