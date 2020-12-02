# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv, find_dotenv
import requests
import json
import traceback
from main import generate_image
from database import DBConnection

load_dotenv(find_dotenv())
token = os.getenv("VKAPI_USER_TOKEN")
gid = '196727308'
message = ""
connection = DBConnection()


def generate_mobalytics_data(message):
    try:
        r = requests.get('https://lor.mobalytics.gg/api/v2/meta/statistics/decks?sortBy=winRateDesc&from=0&count=100')

        for deck in r.json()["decksStats"]:
            if deck["matchesCollected"] > 2000:
                my_deck = deck
                break

        generate_image(["moba", my_deck["cardsCode"]], 0, connection, "output/posting/output.png")


        winrate = round(my_deck["matchesWin"] / my_deck["matchesCollected"], 4) * 100
        winrate = str(winrate)[0:5:]

        response_str = "Колода: %s \nМатчей сыграно: %s \nПобед: %s\nВинрейт: %s%%" % (my_deck["cardsCode"], my_deck["matchesCollected"], my_deck["matchesWin"], winrate)

        return response_str
    except:
        traceback.print_exc()
        return ""

def upload_image(filename):
    img = {'photo': ('img.jpg', open(r'output/posting/output.png', 'rb'))}

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
    message += "Топ10 ранкеда ЕУ:\n"

    headers = {
        "X-Riot-Token": os.getenv("RIOT_API_KEY")
    }

    r = requests.get('https://europe.api.riotgames.com/lor/ranked/v1/leaderboards', headers=headers)

    r = r.json()
    r = r["players"]

    for i in range(10):
        player = r[i]

        player_string = "%s. %s %s LP\n" % ((i+1), player["name"], player["lp"])
        message += player_string

    message += "\nТоп5 игроков из России:\n"
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
        player_string = "%s. %s %s LP\n" % ((i+1), player["name"], player["lp"])
        message += player_string

    return message

moba_message = generate_mobalytics_data("")
print(moba_message)
message += moba_message
message += "\n"
message += ("&#127385;" * 10)
message += "\n\n"

photo_id = upload_image('')

player_message = generate_player_data("")
message += player_message

message += "\n&#9940; Это сообщение было сгенерировано и отправлено автоматически &#9940;"
params = (
    ('owner_id', '-196727308'),
    ('from_group', '1'),
    ('message', message),
    ('attachments', photo_id),
    ('access_token', token),
    ('v', '5.126')
)

response = requests.get('https://api.vk.com/method/wall.post', params=params)
