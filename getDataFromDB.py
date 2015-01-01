import pymongo
from pymongo import MongoClient

#connect to database
client = MongoClient()
db = client.matchdataDB
collection = db.matchdata_collection
print(collection.find_one( { }, { result: 1} ))
