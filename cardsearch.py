from Levenshtein import distance
import json
import sys

def find_card(name):
    jdata = json.loads(open("cards.json",  encoding='utf-8').read())

    name = name.lower()
    min_distance = sys.maxsize
    result = ""

    for dict in jdata:
        if name == dict["name"].lower():
            result = dict["cardCode"]
            break
        elif name in dict["name"].lower():
            result = dict["cardCode"]
            break
        else:
            yo = distance(dict["name"], name)
            if  yo < min_distance:
                min_distance = yo
                result = dict["cardCode"]

    return result

# find_card("Бодряч")
