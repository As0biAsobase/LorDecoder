from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os

class DBConnection:
    def __init__(self):
        load_dotenv(find_dotenv())
        client = MongoClient(os.getenv("MONGODB_KEY"))

    def searchCard(self, name):
        result = client['natum-perdere']['cardsCollection'].find({ "name" : {$regex : new RegExp(name, "i")}})
        print(list(result))

connection = DBConnection()
connection.searchCard("Кровожадный василиск")
