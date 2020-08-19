import json

jdata = json.loads(open("../cards_data/card_data.json",  encoding='utf-8').read())
en_jdata = json.loads(open("../cards_data/en_card_data.json", encoding='utf-8').read())

result = []
en_result = []

for dict in jdata:

    if dict["collectible"] == True:

        result.append({"supertype" : dict["supertype"], "type" : dict["type"], "name" : dict["name"], "cost" : dict["cost"], "cardCode" :  dict["cardCode"], "regionRef" :  dict["regionRef"],
         "assets" : dict["assets"], "attack" : dict["attack"], "health" : dict["health"], "level" : "1"})

    elif dict["collectible"] == False and dict["supertype"] == "Чемпион" and dict["type"] != "Заклинание":

        result.append({"supertype" : dict["supertype"], "type" : dict["type"], "name" : dict["name"], "cost" : dict["cost"], "cardCode" :  dict["cardCode"], "regionRef" :  dict["regionRef"],
         "assets" : dict["assets"], "attack" : dict["attack"], "health" : dict["health"], "level" : "2"})

    elif dict["collectible"] == False and dict["supertype"] == "Чемпион" and dict["type"] == "Заклинание":

        result.append({"supertype" : dict["supertype"], "type" : dict["type"], "name" : dict["name"], "cost" : dict["cost"], "cardCode" :  dict["cardCode"], "regionRef" :  dict["regionRef"],
         "assets" : dict["assets"], "attack" : dict["attack"], "health" : dict["health"], "level" : "3"})


for dict in en_jdata:
    if dict["collectible"] == True:

        en_result.append({"supertype" : dict["supertype"], "type" : dict["type"], "name" : dict["name"], "cost" : dict["cost"], "cardCode" :  dict["cardCode"], "regionRef" :  dict["regionRef"],
         "assets" : dict["assets"], "attack" : dict["attack"], "health" : dict["health"], "level" : "1"})

    elif dict["collectible"] == False and dict["supertype"] == "Champion" and dict["type"] != "Spell":

        en_result.append({"supertype" : dict["supertype"], "type" : dict["type"], "name" : dict["name"], "cost" : dict["cost"], "cardCode" :  dict["cardCode"], "regionRef" :  dict["regionRef"],
         "assets" : dict["assets"], "attack" : dict["attack"], "health" : dict["health"], "level" : "2"})

    elif dict["collectible"] == False and dict["supertype"] == "Champion" and dict["type"] == "Spell":

        en_result.append({"supertype" : dict["supertype"], "type" : dict["type"], "name" : dict["name"], "cost" : dict["cost"], "cardCode" :  dict["cardCode"], "regionRef" :  dict["regionRef"],
         "assets" : dict["assets"], "attack" : dict["attack"], "health" : dict["health"], "level" : "3"})


with open("../cards_data/cards.json", "w", encoding='utf-8') as fp:
    json.dump(result, fp, ensure_ascii=False, indent=2, sort_keys=True)

with open("../cards_data/en_cards.json", "w", encoding='utf-8') as fp:
    json.dump(en_result, fp, ensure_ascii=False, indent=2, sort_keys=True)
