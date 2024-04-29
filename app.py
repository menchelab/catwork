from flask import Flask, render_template_string, render_template, request, session, redirect, url_for
import json
import csv
import plotlyExamples
import random, string
import qrcodeStuff
# Create the Flask application
app = Flask(__name__)

# Details on the Secret Key: https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY
# NOTE: The secret key is used to cryptographically-sign the cookies used for storing
#       the session data.
app.secret_key = 'Hamlo!'

myusers = [] #{'uid': 4, 'links': [666]}, {'uid': 666, 'links': [133,4]}, {'uid': 133, 'links': [666]}, {'uid': 555, 'links': [666, 133, 4, 123, 124, 125]}, {'uid': 125, 'links': [555, 128]}, {'uid': 128, 'links': [555]}, {'uid': 130, 'links': [555]}

@app.before_first_request
# read userdata from file
def execute_before_first_request():
    f = open('dataNew.json')
    global myusers
    myusers = json.load(f)
    f.close()

@app.route('/')
def index():
    if session.get('id') is not None:
        #print(str(session["id"]))
        return redirect(url_for('main')+"?uid="+ str(session["id"]))
    else:
        return redirect(url_for('login'))
    #print(myusers['users'][0]["name"])

@app.route('/set_pw', methods=['GET', 'POST'])
def set_pw():
    global myusers
    if request.method == 'POST':
        # Save the form data to the session object
        session['pw'] = request.form['pw']
        # look up user, check pw
        valid = False
        pw = "abc" 
        c = 0
        for u in myusers["users"]:
            if u["id"] == session['id']:
                #print(u["id"])
                pw = u["pw"]
                session['name'] = u["name"]
                session['index'] = c
                valid = True
                break
            c+=1
        if valid == True:
            if pw == session['pw']:
                if session.get('id') is not None:
                    #print(str(session["id"]))
                    return redirect(url_for('main')+"?uid="+ str(session["id"]))
                else:
                    return "invalid password"
        else:
            return "invalid uid"

    return """
        <form method="post">
            <p>we will set a cookie to keep you logged in on this browser<br>
            <input type="checkbox" name="consent" value = false required /> I agree<br>
            <label for="email">Enter your code:</label>
            <input type="text" name="pw" required />
            <button type="submit">Submit</button
        </form>
        """


@app.route('/main')
def main():

    #global myusers
    if session.get('pw') is not None:
    #if session['email']:
        print("cookie found " + str( session['id'] ))
        uid = -1
        if request.args.get('uid'):
            uid = request.args.get('uid')
            valid = False
            name = ""
            c = 0
            for u in myusers["users"]:
                
                if u["id"] == uid:
                    name = u["name"]
                    index = c
                    valid = True
                    break
                c += 1
            if valid == True:
                thislink = [session["index"],c]
                if thislink not in myusers["links"]:
                    myusers["links"].append(thislink)
                    myusers["users"][thislink[0]]["score"] += 1
                    with open('dataNew.json', 'w') as f:
                            json.dump(myusers, f)
                    f.close()

                graphJSON = plotlyExamples.networkGraphRT(myusers)
                barJson = plotlyExamples.barGraph(myusers)
                return render_template("catwork.html", name=session["name"], user = name, uindex = session["index"] , uid = session["id"], otheruindex = c, graphJSON=graphJSON, barJson=barJson)
            else:
                return "Invalid uid"
        else:
            return "Invalid url"

    else:
        print("no cookie found..redirecting to login")
        if request.args.get('uid'):
            session["id"] = request.args.get('uid')
            
            valid = False
            for u in myusers["users"]:
                if u["id"] == session["id"]:
                    #print(u["id"])
                    valid = True
                    #break
            if valid == True:
                return redirect(url_for('set_pw'))


            else:
                return "invalid uid"
        else:
            return "no uid"












@app.route('/login',  methods=['GET', 'POST'])
def login():
    global myusers
    if request.method == 'POST':
        # user exists?
        result = list(filter(lambda x:x["name"]==request.form['name'],myusers["users"]))
        #print(result)
        if result == [] :
        
            if result == []:
                # Name does Not exist in users, add it
                user = {}
                user["name"] = request.form['name']
                user["id"] = qrcodeStuff.randomword(4)
                user["pw"] = request.form['pw']
                user["score"] = 0
                #set coockies
                session["id"] = user["id"]
                session['name'] = user["name"]
                session['index'] = len(myusers["users"])
                session['pw'] = user["pw"]
                qrcodeStuff.makeqrcode(user["id"])
                #Add to user data
                myusers["users"].append(user)
                with open('dataNew.json', 'w') as f:
                    json.dump(myusers, f)
                f.close()
                return redirect(url_for('main')+"?uid="+ str(session["id"]))

        elif result[0]["pw"] == request.form['pw']: 
            
            return redirect(url_for('main')+"?uid="+ str(result[0]["id"]))
        

        else:
            return "invalid password"


    return """
        <form method="post">
            <p>we will set a cookie to keep you logged in on this browser<br>
            <input type="checkbox" name="consent" value = false required /> I agree<br>
            <label for="name">Enter your name:</label>
            <input type="text" name="name" required />
            <label for="pw">password:</label>
            <input type="text" name="pw" required />
            <button type="submit">Submit</button
        </form>
        """


@app.route('/logout')
def logout():
    # Clear the email stored in the session object
    session.pop('pw', default=None)
    session.pop('id', default=None)
    session.pop('name', default=None)
    session.pop('index', default=None)
    return '<h1>Session deleted!</h1>'


if __name__ == '__main__':
    app.run()