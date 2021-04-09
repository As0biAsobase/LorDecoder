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

    def getCardsByRegion(self, region):
        result = self.client['natum-perdere']['cardsCollection'].find({ "region" : region})
        result = list(result)

        return result
        
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
