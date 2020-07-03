from lor_deckcodes import LoRDeck, CardCodeAndCount
from PIL import Image
import json
import requests
from io import BytesIO
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

champions = []
followers = []
spells = []

champions_total = 0
followers_total = 0
spells_total = 0

cost_font = ImageFont.truetype("fonts/Roboto-Black.ttf", 50)
name_font = ImageFont.truetype("fonts/Roboto-Regular.ttf", 37)
title_font = ImageFont.truetype("fonts/AmaticSC-Bold.ttf", 70)

jdata = json.loads(open("cards.json",  encoding='utf-8').read())

# Decoding
deck = LoRDeck.from_deckcode('CEBAIAIFAEHSQNQIAEAQGDAUDAQSOKJUAIAQCBI5AEAQCFYA')

# list all cards with card format 3:01SI001
# list(deck)

# natum = Image.open("Natum_Perdere_HD.png")
# natum.putalpha(200)
# background.paste(natum)
# background.show()
# bg_w, bg_h = background.size
for each in deck:
    for dict in jdata:
        q, code = each.split(':')
        q = int(q)
        if dict["cardCode"] == code:
            # print(dict["name"])
            if dict["type"] == "Боец":
                if dict["supertype"] == "Чемпион":
                    # background.paste(img, (50, 100 + len(champions)*110))
                    champions.append({"name" : dict["name"], "cost" : dict["cost"], "cardCode" :  dict["cardCode"], "regionRef" :  dict["regionRef"], "quantity" :  q})
                    champions_total += q
                else:
                    # background.paste(img, (550, 100 + len(followers)*110))
                    followers.append({"name" : dict["name"], "cost" : dict["cost"], "cardCode" :  dict["cardCode"], "regionRef" :  dict["regionRef"], "quantity" :  q})
                    followers_total += q
            else:
                # background.paste(img, (1050, 100 + len(followers)*110))
                spells.append({"name" : dict["name"], "cost" : dict["cost"], "cardCode" :  dict["cardCode"], "regionRef" :  dict["regionRef"], "quantity" :  q})
                spells_total += q

height = max([len(champions), len(followers), len(spells)]) * 72 + 200
background = Image.new('RGBA', (1920, height), (30, 30, 30, 255))

logo = Image.open("logos/Natum_Perdere_Logo.png")
logo = logo.resize((640, 360))
background.paste(logo, (0, 360), mask = logo)
print(height)

champions = sorted(champions, key = lambda i: i['cost'])
followers = sorted(followers, key = lambda i: i['cost'])
spells = sorted(spells, key = lambda i: i['cost'])

i = 0
for each in champions:
    img = Image.open("processed/" + each["cardCode"] + ".png")
    img = img.resize((600, 70))
    draw = ImageDraw.Draw(img)

    text = str(each["quantity"])
    x, y = 570, 10

    draw.text((x-2, y-2), text, (0,0,0), font=name_font)
    draw.text((x+2, y-2), text,(0,0,0),font=name_font)
    draw.text((x+2, y+2), text, (0,0,0), font=name_font)
    draw.text((x-2, y+2), text, (0,0,0),font=name_font)
    draw.text((570, 10), text, font=name_font, fill='rgb(255, 255, 255)')

    background.paste(img, (30, 100 + i*72))
    i += 1

i = 0
for each in followers:
    img = Image.open("processed/" + each["cardCode"] + ".png")
    img = img.resize((600, 70))
    draw = ImageDraw.Draw(img)

    text = str(each["quantity"])
    x, y = 570, 10

    draw.text((x-2, y-2), text, (0,0,0), font=name_font)
    draw.text((x+2, y-2), text,(0,0,0),font=name_font)
    draw.text((x+2, y+2), text, (0,0,0), font=name_font)
    draw.text((x-2, y+2), text, (0,0,0),font=name_font)

    draw.text((x, y), text, font=name_font, fill='rgb(255, 255, 255)')

    background.paste(img, (660, 100 + i*72))
    i += 1

i = 0
for each in spells:
    img = Image.open("processed/" + each["cardCode"] + ".png")
    img = img.resize((600, 70))
    draw = ImageDraw.Draw(img)

    text = str(each["quantity"])
    x, y = 570, 10

    draw.text((x-2, y-2), text, (0,0,0), font=name_font)
    draw.text((x+2, y-2), text,(0,0,0),font=name_font)
    draw.text((x+2, y+2), text, (0,0,0), font=name_font)
    draw.text((x-2, y+2), text, (0,0,0),font=name_font)

    draw.text((x, y), text, font=name_font, fill='rgb(255, 255, 255)')

    background.paste(img, (1290, 100 + i*72))
    i += 1


draw = ImageDraw.Draw(background)
draw.text((30, 10), "Главари: " + str(champions_total), font=title_font, fill='rgb(255, 255, 255)')
draw.text((660, 10), "Воены: " + str(followers_total), font=title_font, fill='rgb(255, 255, 255)')
draw.text((1290, 10), "Колдунства: " + str(spells_total), font=title_font, fill='rgb(255, 255, 255)')

background.show()
print("Чемпион: " + str(len(champions)) + " Боец: " + str(len(followers)) + " Заклинание: " + str(len(spells)))
