from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os#

load_dotenv(find_dotenv())
client = MongoClient(os.getenv("MONGODB_KEY"))

result = client['natum-perdere']['cardsCollection'].find({})

print(list(result))
