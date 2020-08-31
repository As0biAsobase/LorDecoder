# coding=utf-8
from lor_deckcodes import LoRDeck, CardCodeAndCount
from PIL import Image
import json
import requests
from io import BytesIO
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont



# Decoding
def generate_image(code, user_id):
    champions = []
    followers = []
    spells = []

    champions_total = 0
    followers_total = 0
    spells_total = 0

    cost_font = ImageFont.truetype("fonts/Roboto-Black.ttf", 50)
    name_font = ImageFont.truetype("fonts/Roboto-Regular.ttf", 37)
    title_font = ImageFont.truetype("fonts/AmaticSC-Bold.ttf", 70)

    champion_string = "Главари: "
    follower_string = "Воены: "
    spell_string = "Колдунства: "

    jdata = json.loads(open("cards_data/cards.json",  encoding='utf-8').read())

    deck = LoRDeck.from_deckcode(code)


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

    ratio = height / 960
    background = Image.open("background/1gs.png")
    new_width = 1920 * ratio
    background = background.resize(new_width, height)

    margin = (new_width - 1920) // 2
    background = background.crop(margin, 0, new_width-margin, height) 

    # background = Image.new('RGBA', (1920, height), (61, 61, 61, 255))

    print(user_id)
    if user_id == 103657653:
        logo = Image.open("logos/Biolog.png")
        logo = logo.resize((640, 360))
        background.paste(logo, (0, height-360), mask = logo)
    elif user_id == 283942422 or user_id == 488352580:
        logo = Image.open("logos/okolo.png")
        logo = logo.resize((640, 360))
        background.paste(logo, (0, height-360), mask = logo)
    elif user_id ==3015002:
        logo = Image.open("logos/numi.png")
        logo = logo.resize((640, 360))
        background.paste(logo, (0, height-360), mask = logo)

        champion_string = "Военачальники: "
        follower_string = "Подданные: "
        spell_string = "Йордловская магия: "
    else:
        logo = Image.open("logos/Natum_Perdere_Logo.png")
        logo = logo.resize((640, 360))
        background.paste(logo, (0, height-360), mask = logo)



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
    draw.text((30, 10), champion_string + str(champions_total), font=title_font, fill='rgb(255, 255, 255)')
    draw.text((660, 10), follower_string + str(followers_total), font=title_font, fill='rgb(255, 255, 255)')
    draw.text((1290, 10), spell_string + str(spells_total), font=title_font, fill='rgb(255, 255, 255)')

    background.save("output/output.png")

# generate_image("CEBAIAIDDYVC4LYEAEBAECAJHECAGAIDBMNSYAICAMEQEAICBQSQCAQCAUBACAIDCMAQCARR")
# print("Чемпион: " + str(len(champions)) + " Боец: " + str(len(followers)) + " Заклинание: " + str(len(spells)))
