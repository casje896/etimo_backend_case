"""
RestAPI for a database where the user information consists of an email, first name and last name. 
The email is the key for the database since it is supposed to be unique while the first and last names does not have to be unique. 

"""

from flask import Flask, request, jsonify, abort

#Some initial data in the "database". 
dataDict = {"casper@casper.se": ("Casper", "casp"),
            "somedude@hello.com": ("Some", "dude")}

app = Flask(__name__)

@app.route('/', methods=['GET'])
def getUsers():
    try:
        #Simply return the whole dictionary since JSON structure is very similar to the dictionary structure. 
        return jsonify(dataDict)
    except:
        abort(500) #Something went wrong
    
@app.route('/', methods=['PUT'])
def addUser():
    data = request.json

    #Make sure that the request have a proper format. 
    try: 
        email = data["email"]    
    except:
        abort(400, description='Key error, unvalid key in request.')     

    #Check if email is not in the database, if it is then send an error message
    if dataDict.get(email) != None:
            
        #Error 409 for conflict with input from client. 
        abort(409, description='Email already in database')  #Note: might be security risk to let the client know the email is already in use 
    else:
        fname = data["fname"]
        lname = data["lname"]
        nameTup = (fname, lname)

        dataDict[email] = nameTup

        return jsonify({email: dataDict[email]})

@app.route('/', methods=['DELETE'])
def removeUser():
    data = request.json

    #Make sure that the request have a proper format. 
    try: 
        email = data["email"]    
    except:
        abort(400, description='Key error, unvalid key in request.')     
    
    try: 
        #Check if email already exist
        dataDict[email]     
        #Delete item and return email and name
        return jsonify({email:dataDict.pop(email)})     
    except: 
        #Send relevant error code if user dont exist. error 404
        abort(404, description='Email is not in database.') 

if __name__ == '__main__':
    app.run()  # run Flask app