import json
import requests

def get_highest_grow():
    jdata = json.loads(open("output/posting/yesterday_decks_matchesDesc.json",  encoding='utf-8').read())
    jdata = jdata["decksStats"]

    r = requests.get('https://lor.mobalytics.gg/api/v2/meta/statistics/decks?sortBy=%s&from=0&count=100&threshold=all' % (filter))
    r = r.json()["decksStats"]


    max_wr = 0
    max_deck = None
    max_previous = None
    for dict in jdata:
        print(dict)
        for deck in r:
            if deck["cardsCode"] == dict["cardsCode"]:
                print("It's a match!")
                deck_winrate = round(deck["matchesWin"] / deck["matchesCollected"], 4) * 100
                dict_winrate = round(dict["matchesWin"] / dict["matchesCollected"], 4) * 100

                if deck_winrate > dict_winrate:
                    print("Growth!")
                    if deck_winrate - dict_winrate > max_wr:
                        max_deck = deck
                        max_previous = dict
                        max_wr = deck_winrate - dict_winrate

    print(max_deck)
    print(max_previous)
    print(max_wr)
get_highest_grow()
