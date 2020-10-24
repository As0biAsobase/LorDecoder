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

        return list(result)
