import csv
import json
import random, string
import qrcode

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



def qrcodes():

    for i in range(217,230):
    # Data to be encoded
        data = 'https://catwork.azurewebsites.net/?uid=' + str(i)
        
        # Encoding data using make() function
        img = qrcode.make(data)
        
        # Saving as an image file
        img.save('uid_'+str(i)+'.png')



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