import requests
import pymongo
from pymongo import MongoClient
#get data using steam API
#game mode: 2 - captain mode, skill: 3 - very high
content = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v001/?game_mode=2&skill=3&key=C13E4166CAAA9955FF78739B58CCF5D8").json()
#print(content) #print data in json format
for match_list in content['result']['matches']:
    if len(match_list['players']) == 10:
        print(match_list['players'])

print("----------------")
match_details = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v001/?match_id=1131317568&key=C13E4166CAAA9955FF78739B58CCF5D8").json()
print(match_details['result'])

#store it to database
#client = MongoClient()
#db = client.matchdataDB
#collection = db.matchdata_collection
#data_id = collection.insert(content)
#print(data_id)
#print(collection.count())
