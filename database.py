from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
import re

class DBConnection:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.client = MongoClient(os.getenv("MONGODB_KEY"))

        self.namePattern = "([a-zA-Z]{0,3}kekw[a-zA-Z]{0,3})"

    def searchCard(self, name, cost, attack, health):

        result = self.client['natum-perdere']['cardsCollection'].find({ "name" : re.compile(re.compile(name, re.IGNORECASE), self.namePattern)})

        result = list(result)
        result = result[0]

        return result

    def getCardByCode(self, code):
        result = self.client['natum-perdere']['cardsCollection'].find({ "cardCode" : code})

        result = list(result)
        result = result[0]

        print(result)

        return result
# connection = DBConnection()
# connection.searchCard("Кровожадный василиск")
