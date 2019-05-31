from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

# Initializing Flask app and creating rest API service
app = Flask(__name__)
api = Api(app)

# Connecting database to our app
# 27015 is the standard port for Mongo
client = MongoClient("mongodb://my_db:27017")
db = client.projectDB
users = db["Users"]

"""
HELPER FUNCTIONS
"""


def userExists(username):
    if users.find({"Username": username}).count() == 0:
        return False
    else:
        return True


def verifyUser(username, password):
    if not userExists(username):
        return False

    user_hashed_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.checkpw(password.encode('utf8'), user_hashed_pw):
        return True
    else:
        return False


def getUserMessage(username):
    return users.find({
        "Username": username
    })[0]["Messages"]


"""
RESOURCES
"""


class Hello(Resource):
    def get(self):
        return "Hello World"


class Register(Resource):
    def post(self):
        # Get the posted data from request
        data = request.get_json()

        # get data
        username = data["username"]
        password = data["password"]

        # check if user exists
        if userExists(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username",
            }
            return jsonify(retJson)

        # Encrypting the password
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # Insert record
        users.insert({
            "Username": username,
            "Password": password,
            "Messages": []
        })

        # Return successful result
        retJson = {
            "status": 200,
            "msg": "Registration Successful",
        }
        return jsonify(retJson)


class Retrieve(Resource):
    def post(self):
        # Get the posted data from request
        data = request.get_json()

        # get data
        username = data["username"]
        password = data["password"]

        # check if user exists
        if not userExists(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username",
            }
            return jsonify(retJson)

        # Check if password is correct
        correct_pw = verifyUser(username, password)
        if not correct_pw:
            retJson = {
                "status": 302,
                "msg": "Invalid Password",
            }
            return jsonify(retJson)

        # get the messages
        messages = getUserMessage(username)

        # Build successful response
        retJson = {
            "status": 200,
            "obj": messages,
        }
        return jsonify(retJson)


class Save(Resource):
    def post(self):
        # Get the posted data from request
        data = request.get_json()

        # get the data
        username = data["username"]
        password = data["password"]
        message = data["message"]

        # check if user exists
        if not userExists(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username",
            }
            return jsonify(retJson)

        # Check if password is correct
        correct_pw = verifyUser(username, password)
        if not correct_pw:
            retJson = {
                "status": 302,
                "msg": "Invalid Password",
            }
            return jsonify(retJson)

        # Check if the message is valid
        if not message:
            retJson = {
                "status": 303,
                "msg": "Please Supply a valid message",
            }
            return jsonify(retJson)

        # get the messages
        messages = getUserMessage(username)

        # Add current message
        messages.append(message)

        # Save the User's new message
        users.update({
            "Username": username
        }, {
            "$set": {
                "Messages": messages
            }
        })

        retJson = {
            "status": 200,
            "msg": "Message has been saved successfully",
        }

        return jsonify(retJson)


api.add_resource(Hello, '/hello')
api.add_resource(Register, '/register')
api.add_resource(Retrieve, '/retrieve')
api.add_resource(Save, '/save')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
