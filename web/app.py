from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcyrpt

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

    if bcyrpt.checkpw(password.encode('utf8'), user_hashed_pw):
        return True
    else:
        return False


def getUserMessage(username):
    return users.find({
        "Username": username
    })[0]["Messages"]