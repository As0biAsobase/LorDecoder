from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os

def query_archetype_wr(input_cards):
    # input_cards = ['01DE039', '01DE026', '02DE010', '02BW008']
    client = MongoClient(os.getenv("MONGODB_KEY"))
    result = client['Natum_Perdere']['Meta'].aggregate([
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
    return result
