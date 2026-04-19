import os
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_pymongo import PyMongo

load_dotenv()

mongo = PyMongo()

_client = None
_db = None

def init_db(app):
    global _client, _db
    mongo_uri = os.getenv("MONGO_URI")
    
    _client = MongoClient(mongo_uri)
    _db = _client["prod"]
    
    app.config["MONGO_URI"] = mongo_uri
    mongo.init_app(app)

def get_collection(name):
    return _db[name]