import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from Levenshtein import distance
import os
import re
import sys

class DBConnection:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.client = MongoClient(os.getenv("MONGODB_KEY"))

        self.namePattern = "([a-zA-Z]{0,3}kekw[a-zA-Z]{0,3})"

    def get_players(self):
        result = self.client['natum-perdere']['PlayersyRiotID'].find({})
        result = list(result)
        
        return result

    def find_player(self, puuid):
        result = self.client['natum-perdere']['PlayersyRiotID'].find({ "puuid" : puuid})
        
        return result  

    def get_matches(self):
        result = self.client['natum-perdere']['LorMatches'].find({})
        result = list(result)

        return result 

    def searchCard(self, name, cost, attack, health):

        result = self.client['natum-perdere']['cardsCollection'].find({ "name" : re.compile(name, re.IGNORECASE)})

        result = list(result)

        # if we didn't find perfect match and enough information is given attempt to guess (possibly needs optimization)
        if len(result) == 0 and len(name) >= 3:
            result = self.client['natum-perdere']['cardsCollection'].find({})
            result = list(result)

            min_distance = sys.maxsize
            for each in result:
                dif = distance(each["name"], name)
                if dif == 1:
                    result = each
                    break
                elif dif < min_distance:
                    min_distance = dif
                    result = each
        else:
            result = result[0]

        return result

    def getCardByCode(self, code):
        result = self.client['natum-perdere']['cardsCollection'].find({ "cardCode" : code})

        result = list(result)
        result = result[0]

        return result

    def getAllCards(self):
        result = self.client['natum-perdere']['cardsCollection'].find({})
        result = list(result)

        return result

    def getCardsByRegion(self, region, set):
        result = self.client['natum-perdere']['cardsCollection'].find({ "region" : region, "set" : set})
        result = list(result)

        return result

    def getUserLeaderboard(self):
        result = self.client['natum-perdere']['userLeaderboard'].find({}).sort( "score" , pymongo.DESCENDING )
        result = list(result)

        return result

    def decreaseUserRating(self, user_id, decrease):
        result = self.client['natum-perdere']['userLeaderboard'].find({ "user" : user_id})
        if len(list(result)) == 0:
            self.client['natum-perdere']['userLeaderboard'].insert({ "user" : user_id, "score" : 0})
        else:
            self.client['natum-perdere']['userLeaderboard'].update( { "user" : user_id }, { '$inc': { "score" : -decrease}})

    def increaseUserRating(self, user_id, increase):
        result = self.client['natum-perdere']['userLeaderboard'].find({ "user" : user_id})
        if len(list(result)) == 0:
            self.client['natum-perdere']['userLeaderboard'].insert({ "user" : user_id, "score" : increase})
        else:
            self.client['natum-perdere']['userLeaderboard'].update( { "user" : user_id }, { '$inc': { "score" : increase}})

    def getUserRating(self, user_id):
        result = self.client['natum-perdere']['userLeaderboard'].find({ "user" : user_id})

        result = list(result)
        result = result[0]

        table = self.getUserLeaderboard()

        rating = -1

        for i in range(len(table)):
            if table[i]["user"] == user_id:
                rating = i+1
                break

        return [result, rating]

    def getCodeByName(self, name):
        result = self.client['natum-perdere']['cardsCollection'].find({ "name" : re.compile(name, re.IGNORECASE)})

        result = list(result)

        if len(result) == 0 and len(name) >= 3:
            result = self.client['natum-perdere']['cardsCollection'].find({})
            result = list(result)

            min_distance = sys.maxsize
            for each in result:
                dif = distance(each["name"], name)
                if dif == 1:
                    result = each
                    break
                elif dif < min_distance:
                    min_distance = dif
                    result = each
        else:
            result = result[0]

        result = result["cardCode"]

        return result
# connection = DBConnection()
# connection.searchCard("Кровожадный василиск")
