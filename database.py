from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
import re

class DBConnection:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.client = MongoClient(os.getenv("MONGODB_KEY"))

    def searchCard(self, name):
        result = self.client['natum-perdere']['cardsCollection'].find({ "name" : re.compile(name, re.IGNORECASE)})
        print(list(result))

        result = list(result)
        print(result)

        result = result[0]
        print(result)

        return result

# connection = DBConnection()
# connection.searchCard("Кровожадный василиск")
