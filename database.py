from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
import re

class DBConnection:
    def __init__(self):
        load_dotenv(find_dotenv())
        client = MongoClient(os.getenv("MONGODB_KEY"))

    def searchCard(self, name):
        result = client['natum-perdere']['cardsCollection'].find({ "name" : re.compile(username, re.IGNORECASE)})
        print(list(result))

connection = DBConnection()
connection.searchCard("Кровожадный василиск")
