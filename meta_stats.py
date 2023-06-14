from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os

# MongoDB query for retreiving a winrate for decks with specific combinations of cards
def query_archetype_wr(input_cards):
    load_dotenv(find_dotenv())
    client = MongoClient(os.getenv("MONGODB_KEY"))
    result = client['natum-perdere']['meta-stats'].aggregate([
        {
            '$match': {
                'decklist': {
                    '$all': input_cards
                }
            }
        }, {
            '$sort': {
                'matchesCollected': -1
            }
        }, {
            '$addFields': {
                'winrate': {
                    '$divide': [
                        '$matchesWin', '$matchesCollected'
                    ]
                }
            }
        }, {
            '$group': {
                '_id': None,
                'count': {
                    '$sum': 1
                    },
                'total_collected': {
                    '$sum': '$matchesCollected'
                },
                'total_won': {
                    '$sum': '$matchesWin'
                }
                }
        }, {
            '$project': {
                '_id' : 0,
                'total_won': '$total_won',
                'total_collected': "$total_collected",
                'average_winrate': {
                    '$divide': [
                        '$total_won', '$total_collected'
                    ]
                }
            }
        }
    ])

    result = list(result)
    print(result)
    return result
