import json
import mysql.connector

regions_dict = {
    "Ionia" : "IO",
    "PiltoverZaun" : "PZ",
    "Bilgewater" : "BW",
    "Demacia" : "DE",
    "Freljord" : "FR",
    "Targon" : "MT",
    "Noxus" : "NX",
    "ShadowIsles" : "SI"
}

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="test",
  password="password"
)

print(mydb)

mycursor = mydb.cursor()

mycursor.execute("USE test")

jdata = json.loads(open("../cards_data/card_data.json",  encoding='utf-8').read())

for each in jdata:
    # asset = json.loads(each["assets"][0])
    asset = each["assets"][0]
    print(each['name'])
    sql = """INSERT INTO cards (associated_cards, game_image_path, full_image_path, region, attack, health, cost, `description`, levelup_description,
    flavor_text, artist_name, `name`, card_code, keywords, spell_speed, rarity, subtypes, `type`, supertype, collectible, `set`) VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    val = (str(each["associatedCardRefs"]), asset['gameAbsolutePath'], asset['fullAbsolutePath'], regions_dict.get(each['regionRef']),
    each['attack'], each['health'], each['cost'], each['description'], each['levelupDescription'], each['flavorText'], each['artistName'], each['name'],
    each['cardCode'], str(each['keywordRefs']), each['spellSpeedRef'], each['rarityRef'], str(each['subtypes']), each['type'], each['supertype'], each['collectible'], 0)

    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
