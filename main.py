# coding=utf-8
from lor_deckcodes import LoRDeck, CardCodeAndCount
from PIL import Image
import json
import requests
from io import BytesIO
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import operator

# Decoding
def generate_image(args, user_id, connection, location):
    empty_bg = False
    serious = False

    # code should always be the last parameter

    code = args[len(args)-1]


    if "пнг" in args:
        empty_bg = True
    if "духота" in args:
        serious = True

    champions = []
    followers = []
    spells = []
    landmarks = []

    deck_regions = {}

    champions_total = 0
    followers_total = 0
    spells_total = 0
    landmarks_total = 0

    cost_font = ImageFont.truetype("/home/khun/LorDecoder/fonts/Roboto-Black.ttf", 50)
    name_font = ImageFont.truetype("/home/khun/LorDecoder/fonts/Roboto-Regular.ttf", 37)
    title_font = ImageFont.truetype("/home/khun/LorDecoder/fonts/AmaticSC-Bold.ttf", 70)

    champion_string = "Главари: "
    follower_string = "Воены: "
    spell_string = "Колдунства: "
    landmark_string = "Главарства: "

    jdata = json.loads(open("/home/khun/LorDecoder/cards_data/cards.json",  encoding='utf-8').read())

    deck = LoRDeck.from_deckcode(code)

    for each in deck:
        q, code = each.split(':')
        q = int(q)

        dict = connection.getCardByCode(code)
        # this is a workaround for finding deck regions
        # technically can be derived from code itself but is not supported by library
        if dict["regionRef"] not in deck_regions:
            deck_regions[dict["regionRef"]] = 1
        else:
            deck_regions[dict["regionRef"]] +=1

        # populating arrays of three card types
        # will need to improve using MongoDB instead of simply looping through json
        if dict["type"] == "Боец":
            if dict["supertype"] == "Чемпион":
                champions.append({"name" : dict["name"], "cost" : dict["cost"], "cardCode" :  dict["cardCode"], "regionRef" :  dict["regionRef"], "quantity" :  q})
                champions_total += q
            else:
                followers.append({"name" : dict["name"], "cost" : dict["cost"], "cardCode" :  dict["cardCode"], "regionRef" :  dict["regionRef"], "quantity" :  q})
                followers_total += q
        elif dict["type"] == "Место силы":
            landmarks.append({"name" : dict["name"], "cost" : dict["cost"], "cardCode" :  dict["cardCode"], "regionRef" :  dict["regionRef"], "quantity" :  q})
            landmarks_total += q
        else:
            spells.append({"name" : dict["name"], "cost" : dict["cost"], "cardCode" :  dict["cardCode"], "regionRef" :  dict["regionRef"], "quantity" :  q})
            spells_total += q

    height = max([len(champions)+len(landmarks)+6, len(followers), len(spells)]) * 85 + 200

    ratio = height / 960

    # we find region with most cartds (not counting individual copies)
    top_region = max(deck_regions.items(), key=operator.itemgetter(1))[0]

    if not empty_bg:
        if user_id == 103657653:
            background = Image.open("/home/khun/LorDecoder/background/biolog.jpg")
        else:
            background = Image.open("/home/khun/LorDecoder/background/poros/%s.png" % (top_region))
    else:
        background = Image.open("/home/khun/LorDecoder/background/empty.png")

    # background processing
    if ratio > 1:
        new_width = 1920 * ratio
        background = background.resize((int(new_width), int(height)))
        margin = (new_width - 1920) // 2
        background = background.crop((margin, 0, new_width-margin, height))
    else:
        background = background.crop((0, 0, 1920, height))

    # background = Image.new('RGBA', (1920, height), (61, 61, 61, 255))

    # print(user_id)

    if user_id == 103657653:
        logo = Image.open("/home/khun/LorDecoder/logos/Biolog.png")
        logo = logo.resize((640, 360))
        background.paste(logo, (0, height-360), mask = logo)
    elif user_id == 488352580:
        logo = Image.open("/home/khun/LorDecoder/logos/okolo.png")
        logo = logo.resize((640, 360))
        background.paste(logo, (0, height-360), mask = logo)

        follower_string = "Подписчики: "
        landmark_string = "Достопримечательности: "
    elif user_id ==3015002:
        logo = Image.open("/home/khun/LorDecoder/logos/numi.png")
        logo = logo.resize((640, 360))
        background.paste(logo, (0, height-360), mask = logo)

        champion_string = "Военачальники: "
        follower_string = "Подданные: "
        spell_string = "Йордловская магия: "
    else:
        logo = Image.open("/home/khun/LorDecoder/logos/Natum_Perdere_Logo.png")
        logo = logo.resize((640, 360))
        background.paste(logo, (0, height-360), mask = logo)

    if serious == True:
        champion_string = "Чемпионы: "
        follower_string = "Союзники: "
        spell_string = "Заклинания: "
        landmark_string = "Места силы: "

    champions = sorted(champions, key = lambda i: i['cost'])
    followers = sorted(followers, key = lambda i: i['cost'])
    spells = sorted(spells, key = lambda i: i['cost'])
    landmarks = sorted(landmarks, key = lambda i: i['cost'])

    i = 0
    for each in champions:
        img = Image.open("/home/khun/LorDecoder/processed/" + each["cardCode"] + ".png")
        # img = img.resize((605, 72))
        draw = ImageDraw.Draw(img)

        text = str(each["quantity"])
        x, y = 545, 12

        draw.text((x-2, y-2), text, (0,0,0), font=name_font)
        draw.text((x+2, y-2), text,(0,0,0),font=name_font)
        draw.text((x+2, y+2), text, (0,0,0), font=name_font)
        draw.text((x-2, y+2), text, (0,0,0),font=name_font)

        draw.text((x, y), text, font=name_font, fill='rgb(255, 255, 255)')

        background.paste(img, (30, 100 + i*80), img)
        i += 1

    if landmarks_total > 0:
        draw = ImageDraw.Draw(background)
        offset = 100+(i)*72
        draw.text((30, offset), landmark_string + str(landmarks_total), font=title_font, fill='rgb(255, 255, 255)')

        i = 0
        for each in landmarks:
            img = Image.open("/home/khun/LorDecoder/processed/" + each["cardCode"] + ".png")
            # img = img.resize((625, 75))
            draw = ImageDraw.Draw(img)

            text = str(each["quantity"])
            x, y = 570, 10

            draw.text((x-2, y-2), text, (0,0,0), font=name_font)
            draw.text((x+2, y-2), text,(0,0,0),font=name_font)
            draw.text((x+2, y+2), text, (0,0,0), font=name_font)
            draw.text((x-2, y+2), text, (0,0,0),font=name_font)
            draw.text((570, 10), text, font=name_font, fill='rgb(255, 255, 255)')

            background.paste(img, (30, 100 + offset + i*85), img)
            i += 1

    i = 0
    for each in followers:
        img = Image.open("/home/khun/LorDecoder/processed/" + each["cardCode"] + ".png")
        # img = img.resize((605, 72))
        draw = ImageDraw.Draw(img)

        text = str(each["quantity"])
        x, y = 545, 12

        draw.text((x-2, y-2), text, (0,0,0), font=name_font)
        draw.text((x+2, y-2), text,(0,0,0),font=name_font)
        draw.text((x+2, y+2), text, (0,0,0), font=name_font)
        draw.text((x-2, y+2), text, (0,0,0),font=name_font)

        draw.text((x, y), text, font=name_font, fill='rgb(255, 255, 255)')

        background.paste(img, (621, 100 + i*80), img)
        i += 1

    i = 0
    for each in spells:
        img = Image.open("/home/khun/LorDecoder/processed/" + each["cardCode"] + ".png")
        # img = img.resize((625, 75))
        draw = ImageDraw.Draw(img)

        text = str(each["quantity"])
        x, y = 565, 22

        draw.text((x-2, y-2), text, (0,0,0), font=name_font)
        draw.text((x+2, y-2), text,(0,0,0),font=name_font)
        draw.text((x+2, y+2), text, (0,0,0), font=name_font)
        draw.text((x-2, y+2), text, (0,0,0),font=name_font)

        draw.text((x, y), text, font=name_font, fill='rgb(255, 255, 255)')

        background.paste(img, (1212, 100 + i*85), img)
        i += 1


    draw = ImageDraw.Draw(background)
    draw.text((30, 10), champion_string + str(champions_total), font=title_font, fill='rgb(255, 255, 255)')
    draw.text((621, 10), follower_string + str(followers_total), font=title_font, fill='rgb(255, 255, 255)')
    draw.text((1212, 10), spell_string + str(spells_total), font=title_font, fill='rgb(255, 255, 255)')

    background.save(location)

# generate_image("CEBAIAIDDYVC4LYEAEBAECAJHECAGAIDBMNSYAICAMEQEAICBQSQCAQCAUBACAIDCMAQCARR")
# print("Чемпион: " + str(len(champions)) + " Боец: " + str(len(followers)) + " Заклинание: " + str(len(spells)))
