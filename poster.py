# -*- coding: utf-8 -*-
import os
import sys
from dotenv import load_dotenv, find_dotenv
import requests
import json
import traceback
from main import generate_image
from database import DBConnection
from lor_deckcodes import LoRDeck, CardCodeAndCount
from deckchanges import get_highest_growth
from datetime import datetime

load_dotenv(find_dotenv())
token = os.getenv("VKAPI_USER_TOKEN")
gid = os.getenv("VK_GID")
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

def generate_player_stats():
    player_stats_string = ''
    players = connection.get_playrs() 
    matches = connection.get_matches() 

    matches_last_day = []

    for each in matches:
        try:
            match_time = each["info"]["game_start_time_utc"]
            match_time = match_time.split('.')[0]
            date_time_obj = datetime.strptime(match_time, "%Y-%m-%dT%H:%M:%S")

            difference = datetime.utcnow() - date_time_obj
            if difference.days == 0:
                matches_last_day.append(each)
        except Exception as e:
            print(f"We were unable to get match")

    player_stats_string += f"Мы собрали {len(matches)} матчей {len(players)} игроков, из них {len(matches_last_day)} за последний день\n"
    return player_stats_string

def upload_image(type):
    if type == "best_deck":
        location = "/home/khun/LorDecoder/output/posting/best_deck.png"

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

    r = requests.get('https://www.perdere.ru:4444/api/v1/get_leaderboard')

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

    try:
        message += generate_player_stats()
    except Exception as e:
        message += "Не удалось получить статистику игроков. Блип-блоп."

    try:
        player_message = generate_player_data("")
        message += player_message
    except:
        traceback.print_exc()
        message += "Не удалось получить данные игроков. Блип-блоп."

    attachment_str = ""
    print(photo_ids)
    for i, each in enumerate(photo_ids):
        attachment_str += each
        if i < len(photo_ids)-1:
            attachment_str += ","
    print(attachment_str)

    message += "\n&#8265; Это сообщение было сгенерировано и отправлено автоматически. Данные Riot Games &#8265;"
    params = (
        ('owner_id', f'-{gid}'),
        ('from_group', '1'),
        ('message', message),
        ('attachments', attachment_str),
        ('access_token', token),
        ('v', '5.126')
    )

    response = requests.get('https://api.vk.com/method/wall.post', params=params)

if __name__ == "__main__":
    a = sys.argv[1]
    print(a)
    if a == "normal":
        generate_normal_post()
    elif a == "donut":
        generate_donut_post()
    else:
        print("Hi, hello!")
