import json

jdata = json.loads(open("card_data.json",  encoding='utf-8').read())
result = []

for dict in jdata:
    if dict["collectible"] == True:
        print(dict["assets"])
        result.append({"supertype" : dict["supertype"], "type" : dict["type"], "name" : dict["name"], "cost" : dict["cost"], "cardCode" :  dict["cardCode"], "regionRef" :  dict["regionRef"],
         "assets" : dict["assets"], "attack" : dict["attack"], "health" : dict["health"]})

with open("cards.json", "w", encoding='utf-8') as fp:
    json.dump(result, fp, ensure_ascii=False, indent=2, sort_keys=True)
