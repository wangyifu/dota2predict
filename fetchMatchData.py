import requests
import pymongo
from pymongo import MongoClient

#get data using steam API
#game mode: 2 - captain mode, skill: 3 - very high
content = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v001/?game_mode=2&skill=3&key=C13E4166CAAA9955FF78739B58CCF5D8").json()
client = MongoClient()
db = client.matchdataDB
collection = db.matchdata_collection
# structure of matchlist['players']:
# [{'player_slot': 0, 'hero_id': 11, 'account_id': 198183807}, {'player_slot': 1, 'hero_id': 69, 'account_id': 36979741}, {'player_slot': 2, 'hero_id': 5, 'account_id': 4294967295}, {'player_slot': 3, 'hero_id': 44, 'account_id': 111706033}, {'player_slot': 4, 'hero_id': 2, 'account_id': 4294967295}, {'player_slot': 128, 'hero_id': 21, 'account_id': 52567955}, {'player_slot': 129, 'hero_id': 27, 'account_id': 136246446}, {'player_slot': 130, 'hero_id': 66, 'account_id': 4294967295}, {'player_slot': 131, 'hero_id': 15, 'account_id': 4294967295}, {'player_slot': 132, 'hero_id': 1, 'account_id': 4294967295}]
for match_list in content['result']['matches']:
    if len(match_list['players']) == 10: #only count match with 10 players
        radiantHeroes = [];
        direHeroes = [];
        for hero in match_list['players']:
            if hero['player_slot'] < 128: #radient hero slots are from 0 to 4
                radiantHeroes.append(hero['hero_id']);
            else: #dire hero slots are from 128 to 132
                direHeroes.append(hero['hero_id']); 
        #get if radiant team wins
        match_id = str(match_list['match_id'])
        match_details = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v001/?match_id="+match_id+"&key=C13E4166CAAA9955FF78739B58CCF5D8").json()
        result = 0
        if match_details['result']['radiant_win']:
            result = 1
        match_data = { "radiantHeroes" : radiantHeroes,
                               "direHeroes" : direHeroes,
                               "radiant_win" : result}
        print(match_data)
        #store it to database
        collection.insert(match_data)
print("----------------")
