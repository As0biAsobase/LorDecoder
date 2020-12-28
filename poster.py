# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv, find_dotenv
import requests
import json
import traceback
from main import generate_image
from database import DBConnection
from lor_deckcodes import LoRDeck, CardCodeAndCount
from deckchanges import get_highest_growth

load_dotenv(find_dotenv())
token = os.getenv("VKAPI_USER_TOKEN")
gid = '196727308'
connection = DBConnection()

def generate_deck_desc(my_deck):
    deck = LoRDeck.from_deckcode(my_deck["cardsCode"])
    deck_name = ""
    champions = []
    regions_str = ""

    for each in deck:
        q, code = each.split(':')
        q = int(q)

        dict = connection.getCardByCode(code)

        if dict["type"] == "Боец":
            if dict["supertype"] == "Чемпион":
                champions.append({"name" : dict["name"], "quantity" :  q})

    for i, each in enumerate(champions):
        deck_name += each["name"].split()[0]
        if i < len(champions)-1:
            deck_name += "-"


    if len(my_deck["regions"]) > 1:
        regions_str = " (%s/%s)" % (my_deck["regions"][0], my_deck["regions"][1])
    else:
        regions_str = " (%s)" % (my_deck["regions"][0])

    deck_name += regions_str
    print(deck_name)

    winrate = round(my_deck["matchesWin"] / my_deck["matchesCollected"], 4) * 100
    winrate = str(winrate)[0:5:]

    response_str = "Колода: %s \nКод: %s \nМатчей сыграно: %s \nПобед: %s\nВинрейт: %s%%" % (deck_name, my_deck["cardsCode"], my_deck["matchesCollected"], my_deck["matchesWin"], winrate)

    return response_str

def generate_deck_changes():
    result = get_highest_growth()

    max_deck = result[0]
    max_previous = result[1]

    new_winrate = round(max_deck["matchesWin"] / max_deck["matchesCollected"], 4) * 100
    old_winrate = round(max_previous["matchesWin"] / max_previous["matchesCollected"], 4) * 100

    wr_diff = new_winrate - old_winrate
    wr_diff = str(wr_diff)
    wr_diff = wr_diff[0:5]

    generate_image(["moba", max_deck["cardsCode"]], 0, connection, "/home/khun/LorDecoder/output/posting/rising_deck.png")
    response_str = generate_deck_desc(max_deck)

    return [response_str, wr_diff]

def generate_mobalytics_data(type):
    try:
        if type == "best_deck":
            location = "/home/khun/LorDecoder/output/posting/best_deck.png"
            filter = "winRateDesc"
            threshold = ""
        elif type == "popular_deck":
            location = "/home/khun/LorDecoder/output/posting/popular_deck.png"
            filter = "matchesDesc"
            threshold = "all"
        else:
            location = "/home/khun/LorDecoder/output/posting/deck.png"
            filter = ""

        r = requests.get('https://lor.mobalytics.gg/api/v2/meta/statistics/decks?sortBy=%s&from=0&count=500&threshold=%s' % (filter, threshold))

        with open("/home/khun/LorDecoder/output/posting/yesterday_decks_" + filter +".json", "w", encoding='utf-8') as fp:
            json.dump(r.json(), fp, ensure_ascii=False, indent=2, sort_keys=True)

        for deck in r.json()["decksStats"]:
            if deck["matchesCollected"] > 2000:
                my_deck = deck
                break

        generate_image(["moba", my_deck["cardsCode"]], 0, connection, location)

        response_str = generate_deck_desc(my_deck)

        return response_str
    except:
        traceback.print_exc()
        return ""

def upload_image(type):
    if type == "best_deck":
        location = "/home/khun/LorDecoder/output/posting/best_deck.png"
    elif type == "popular_deck":
        location = "/home/khun/LorDecoder/output/posting/popular_deck.png"
    elif type == "rising_deck":
        location = "/home/khun/LorDecoder/output/posting/rising_deck.png"
    else:
        location = "/home/khun/LorDecoder/output/posting/posting/deck.png"

    img = {'photo': ('img.jpg', open(location, 'rb'))}

    # Получаем ссылку для загрузки изображений
    method_url = 'https://api.vk.com/method/photos.getWallUploadServer?'
    data = dict(access_token=token, gid=gid, v='5.126')
    response = requests.post(method_url, data)
    result = json.loads(response.text)
    # print(result)
    upload_url = result['response']['upload_url']

    # Загружаем изображение на url
    response = requests.post(upload_url, files=img)
    result = json.loads(response.text)
    # print(result)

    # Сохраняем фото на сервере и получаем id
    method_url = 'https://api.vk.com/method/photos.saveWallPhoto?'
    data = dict(access_token=token, gid=gid, photo=result['photo'], hash=result['hash'], server=result['server'], v='5.126')
    response = requests.post(method_url, data)
    # print(response.text)
    result = json.loads(response.text)['response'][0]
    result = "photo{}_{}".format(result["owner_id"], result["id"])

    return result

def generate_player_data(message):
    headers = {
        "X-Riot-Token": os.getenv("RIOT_API_KEY")
    }

    r = requests.get('https://europe.api.riotgames.com/lor/ranked/v1/leaderboards', headers=headers)

    r = r.json()
    with open("/home/khun/LorDecoder/output/posting/yesterday_palyers.json", "w", encoding='utf-8') as fp:
        json.dump(r, fp, ensure_ascii=False, indent=2, sort_keys=True)

    r = r["players"]

    message += "Топ5 игроков из России:\n"
    russian_top = []

    for each in r:
        is_russian = requests.get("https://www.perdere.ru:4444/api/v1/check_ru?name=" + each["name"])
        is_russian = is_russian.json()
        is_russian = is_russian["isRu"]

        if is_russian:
            russian_top.append(each)

        if len(russian_top) > 4:
            break

    i = 0
    for i, player in enumerate(russian_top):
        player_string = "%s(%s). %s %s LP\n" % ((i+1), player["rank"], player["name"], player["lp"])
        message += player_string

    return message

def generate_normal_post():
    photo_ids = []
    message = ""

    r = generate_deck_changes()
    message += "Колода с самым большим приростом винрейта за день (+%s%%):\n" % (r[1])
    moba_message = r[0]
    print(moba_message)
    message += moba_message
    message += "\n"
    message += ("&#127385;" * 10)
    message += "\n"
    photo_ids.append(upload_image("rising_deck"))

    message += "\n"

    message += "Лучшая колода на данный момент:\n"
    moba_message = generate_mobalytics_data("best_deck")
    print(moba_message)
    message += moba_message
    message += "\n"
    message += ("&#127385;" * 10)
    message += "\n"
    photo_ids.append(upload_image("best_deck"))
    # photo_ids.insert(0, upload_image("best_deck"))

    message += "\n"

    message += "Самая популярная колода на данный момент:\n"
    moba_message = generate_mobalytics_data("popular_deck")
    print(moba_message)
    message += moba_message
    message += "\n"
    message += ("&#127385;" * 10)
    message += "\n"
    photo_ids.append(upload_image("popular_deck"))
    # photo_ids.insert(0, upload_image("popular_deck"))

    message += "\n\n"

    attachment_str = ""
    print(photo_ids)
    for i, each in enumerate(photo_ids):
        attachment_str += each
        if i < len(photo_ids)-1:
            attachment_str += ","

    print(attachment_str)

    player_message = generate_player_data("")
    message += player_message

    message += "\n&#9940; Это сообщение было сгенерировано и отправлено автоматически. Данные Mobalytics и Riot Games &#9940;"
    params = (
        ('owner_id', '-196727308'),
        ('from_group', '1'),
        ('message', message),
        ('attachments', attachment_str),
        ('access_token', token),
        ('v', '5.126')
    )

    response = requests.get('https://api.vk.com/method/wall.post', params=params)

generate_normal_post()
