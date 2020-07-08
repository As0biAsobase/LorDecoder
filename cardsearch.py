from Levenshtein import distance
import json
import sys

def find_card(args):
    jdata = json.loads(open("cards.json",  encoding='utf-8').read())

    costs = ["0", "1", "2", "3", "4", "5",
                "7", "8", "9", "10", "11", "12"]

    name = ""
    cost = None
    attack = None
    health = None

    for each in args:

        if each not in costs and not ("/" in each):
            name += each + " "
            # print(name)
        elif each in costs and not ("/" in each):
            cost = int(each)
            # print(cost)
        elif "/" in each:
            stats = each.split("/")

            if each.endswith("/"):
                attack = int(stats[0])
            elif each.endswith("/"):
                health = int(stats[0])
            else:
                attack = int(stats[0])
                health = int(stats[1])

    print(name)
    print(cost)
    print(attack)
    print(health)


    name.strip()
    min_distance = sys.maxsize
    result = ""

    for dict in jdata:
        if (name == dict["name"].lower() or name == "") and (dict["cost"] == cost or cost is None) and (dict["attack"] == attack or attack is None) and (dict["health"] == health or health is None):
            result = dict["cardCode"]
            break
        elif (name in dict["name"].lower() or name == "") and (dict["cost"] == cost or cost is None) and (dict["attack"] == attack or attack is None) and (dict["health"] == health or health is None):
            result = dict["cardCode"]
            break
        elif (dict["cost"] == cost or cost is None) and (dict["attack"] == attack or attack is None) and (dict["health"] == health or health is None):
            yo = distance(dict["name"], name)
            if  yo < min_distance:
                min_distance = yo
                result = dict["cardCode"]

    return result

# find_card("Бодряч")
