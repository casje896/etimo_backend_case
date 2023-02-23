import json
from flask import Flask, request, jsonify, abort

dataDict = {"casper@casper.se": ("Casper", "casp"),
            "somedude@hello.com": ("Some", "dude")}

app = Flask(__name__)

@app.route('/', methods=['GET'])
def getUsers():
    try:
        return jsonify(dataDict)
    except:
        abort(500) #something went wrong
    
@app.route('/', methods=['PUT'])
def addUser():
    data = request.json
    email = data["email"]    

      
        #Check if email is not in the database, if it is then send error message
    try:
        if not dataDict[email]:
            fname = data["fname"]
            lname = data["lname"]
            nameTup = (fname, lname)

            dataDict[email] = nameTup

            return jsonify({email: dataDict[email]})
        else:
            abort(400, description='Email already in database')     #kika på detta, inte så snyggt nu
            
    except: 
        abort(400, description='Email already in database')

@app.route('/', methods=['DELETE'])
def removeUser():
    data = request.json
    email = data["email"]

    try: 
        #Check if email already exist
        dataDict[email]     
        #Delete item and return email and name
        return jsonify({email:dataDict.pop(email)})     
    except: 
        #Send error with relevant code if user dont exist. error 404
        abort(404, description='Email is not in database.') 

if __name__ == '__main__':
    app.run()  # run Flask app