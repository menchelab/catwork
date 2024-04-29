import os
import flask
from flask import (Flask, redirect, render_template,make_response, request, send_from_directory, url_for)
import chatGPTTest
import plotlyExamples
import json
import csv
import requests
import random
app = Flask(__name__)


myusers = [] #{'uid': 4, 'links': [666]}, {'uid': 666, 'links': [133,4]}, {'uid': 133, 'links': [666]}, {'uid': 555, 'links': [666, 133, 4, 123, 124, 125]}, {'uid': 125, 'links': [555, 128]}, {'uid': 128, 'links': [555]}, {'uid': 130, 'links': [555]}
participants = {}
matches = {}

def getImageUrls():
    images = {}
    imsuccess = True
    descriptions = {}
    descSuccess = True
    try:
        request = requests.get('https://eulife-conference-server.azurewebsites.net/get_speaker_image')
        request.raise_for_status()
        images = request.json()
    except requests.exceptions.HTTPError as err:
        imsuccess = False
        print("failed")

    try:
        request = requests.get('https://eulife-conference-server.azurewebsites.net/get_speaker_summary')
        request.raise_for_status()
        descriptions = request.json()
    except requests.exceptions.HTTPError as err:
        descSuccess = False         

    if imsuccess and descSuccess:
        for i in range(len(images)):
            images[i]["description"] = descriptions[i]["summary"]
        return images
    else:
        return 0
            



@app.before_first_request
def execute_before_first_request():
    f = open('data.json')
    global myusers
    myusers = json.load(f)
    myusers = myusers['users']
    #print(myusers)

    fd = open('participants.csv', encoding="utf8")
    reader = csv.DictReader(fd)

    global participants
    participants["users"] = list(reader)
    #print(participants["users"][0]["Full Name"])

    for p in participants["users"]:
        p["match"] = random.randint(0, len(participants["users"])-1)
        p["conversation"] = '### Conversation suggestion: ""Integrating AI to Enhance Research Efficiency and Diversity in Scientific Institutions"" #### Ice Breaker:'
    

    fd = open('matches.csv', encoding="utf8")
    reader = csv.DictReader(fd)

    matches["matches"] = list(reader)
    #print(matches["matches"][0]["B_Name"])
    for m in matches["matches"]:
        participants["users"][int(m["A_Index"])]["match"] = int(m["B_Index"])
        participants["users"][int(m["A_Index"])]["conversation"] = m["Conversation"]
    
    #print(participants["users"][154]["conversation"])







@app.route('/catGraph')
def catgraph():
    global myusers
    global participants
    graphJSON = plotlyExamples.networkGraphRT(myusers, participants)
    barJson = plotlyExamples.barGraph(myusers, participants)
                    #return '<h1>welcome ' + name + '</h1><br>You just met Agent ' + uid
    return render_template("catGraph.html", graphJSON=graphJSON, barJson=barJson)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/deleteData')
def delete():
    with open('data.json', 'w') as f:
        outjson = {}
        outjson["users"] = []
        json.dump(outjson, f)
    f = open('data.json')
    global myusers
    myusers = json.load(f)
    myusers = myusers['users']
    return "user data deleted"

@app.route('/')
def evilAI():
    AImages = getImageUrls()
    if AImages == 0:
        AImages = [{"image_url":"/static/images/randomcat.png","description":"can i haz AI?"}]
    #print(AImages[0]["image_url"])
    
    # has cookie, add to links

    if  request.cookies.get('userID'):
        if request.args.get('uid'):
            uid = request.args.get('uid')
            name = request.cookies.get('userID')
            for i in myusers:
                if i['uid'] == int(uid):

                    for i in myusers:
                        if i['uid'] == int(name):
                            if int(uid) not in i['links']:
                                i['links'].append(int(uid))
                            break

                    for i in myusers:
                        if i['uid'] == int(uid):
                            if int(name) not in i['links']:
                                i['links'].append(int(name))
                            break

                    with open('data.json', 'w') as f:
                        outjson = {}
                        outjson["users"] = myusers
                        json.dump(outjson, f)                        
                                    
                        #print(links)
                        #print(nodes)
                        #print(annot)
                        #print(myusers)


                    graphJSON = plotlyExamples.networkGraphRT(myusers, participants)
                    barJson = plotlyExamples.barGraph(myusers, participants)
                    #return '<h1>welcome ' + name + '</h1><br>You just met Agent ' + uid
                    return render_template("evilAi.html", user=participants["users"][int(name)]["Full Name"], uid=int(name), graphJSON=graphJSON, barJson=barJson, AImages=AImages)
                    break
            return '<h1>user not in system</h1>'
    #login set cookie
    else:
        if request.args.get('uid'):
            uid = request.args.get('uid')
            return render_template('login.html', uid = int(uid))
            '''
            if int(uid) < len(participants["users"]):
                exists = False

                for i in myusers:
                    if i['uid'] == int(uid):
                        exists = True
                        print("user already exists")

                if not exists:
                    thisUser = {}
                    thisUser["uid"] = int(uid)
                    thisUser["links"] = []
                    myusers.append(thisUser)
                   
                    graphJSON = plotlyExamples.networkGraphRT(myusers, participants)
                    barJson = plotlyExamples.barGraph(myusers, participants)

                    resp = make_response(render_template("evilAi.html", user=participants["users"][int(uid)]["Full Name"], uid=int(uid), graphJSON=graphJSON, barJson=barJson, AImages=AImages))
                    resp.set_cookie('userID', uid)
                    return resp
                else:
                    return '<h1>QR code already claimed</h1>'
 
        '''
        
@app.route('/login', methods = ['GET'])
def login():
    if request.args.get('uid'):
        uid = request.args.get('uid')
        return render_template("login.html", uid = int(uid))


@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
    graphJSON = plotlyExamples.networkGraphRT(myusers, participants)
    barJson = plotlyExamples.barGraph(myusers, participants)
    AImages = getImageUrls()
    if request.method == 'POST':
        code = request.form['pw']
        uid =  request.form['uid']
       
        if code == "123":
            graphJSON = plotlyExamples.networkGraphRT(myusers, participants)
            barJson = plotlyExamples.barGraph(myusers, participants)

            resp = make_response(render_template("evilAi.html", user=participants["users"][int(uid)]["Full Name"], uid=int(uid), graphJSON=graphJSON, barJson=barJson, AImages=AImages))
            resp.set_cookie('userID', uid)
            return resp
        
        else:
            return "WRONG"
    else:
        if request.args.get('uid'):
            uid = request.args.get('uid')
            graphJSON = plotlyExamples.networkGraphRT(myusers, participants)
            barJson = plotlyExamples.barGraph(myusers, participants)
            AImages = getImageUrls()
            return render_template(render_template("evilAi.html", user=participants["users"][int(uid)]["Full Name"], uid=int(uid), graphJSON=graphJSON, barJson=barJson, AImages=AImages))
        else:
            return "get request without argument"
@app.route('/getcookie')
def getcookie():
    if  request.cookies.get('userID'):
        name = request.cookies.get('userID')
        return '<h1>welcome ' + name + '</h1>'
    else:
        return '<h1>no cookie</h1>'



@app.route("/GPT", methods=["POST"])
def GPT():
    result = {}


    if request.method == "POST":

        global participants
       # print(participants["users"][int(data.get("userId"))])

        data = flask.request.get_json()
        answer = chatGPTTest.NewGPTrequest(data.get("text"), participants["users"][int(data.get("userId"))], participants["users"][int( participants["users"][int(data.get("userId"))]["match"])] )
        #fname = TextToSpeech.makeogg(answer, 0)
        

        return {"text": answer}

if __name__ == '__main__':
   app.run()
