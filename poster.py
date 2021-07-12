# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import os
import sys
from dotenv import load_dotenv, find_dotenv
import requests
import json
import traceback
import random
from main import generate_image
from database import DBConnection
from lor_deckcodes import LoRDeck, CardCodeAndCount
from deckchanges import get_highest_growth
from datetime import datetime

load_dotenv(find_dotenv())
token = os.getenv("VKAPI_USER_TOKEN")
gid = os.getenv("VK_GID")
connection = DBConnection()

factions_mapping = {
    "faction_Freljord_Name" : "Фрейльйорд",
    "faction_Shurima_Name" : "Шурима",
    "faction_Noxus_Name" : "Ноксус", 
    "faction_Piltover_Name" : "ПнЗ",
    "faction_ShadowIsles_Name" : "Острова",
    "faction_Ionia_Name" : "Иония",
    "faction_Bilgewater_Name" : "Билджвотер",
    "faction_Demacia_Name" : "Демасия",
    "faction_MtTargon_Name" : "Таргон"
}

region_colors = {
    "Фрейльйорд" : "#34cceb",
    "Шурима" : "#ebe834",
    "Ноксус" : "#e81a1a", 
    "ПнЗ" : "#b5ed4c",
    "Острова" : "#07a880",
    "Иония" : "#fa3494",
    "Билджвотер" : "#fa5534",
    "Демасия" : "#ffff00",
    "Таргон"  : "#8000ff"
}

def generate_deck_desc(deck_code):
    deck = LoRDeck.from_deckcode(deck_code)
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

    print(deck_name)

    response_str = "Колода: %s \nКод: %s \n" % (deck_name, deck_code)

    return response_str

def generate_region_popularity(matches, player_ids):
    popularity = {}

    for key in factions_mapping:
        popularity[factions_mapping[key]] = 0 

    for match in matches:
        try:
            players = match['info']['players'] 
            for player in players:
                if player["puuid"] in player_ids:
                    factions = player["factions"] 
                    for faction in factions:
                        popularity[factions_mapping[faction]] += 1 
        except Exception as e:
            print(f"We were unable to get match", end='\r')

    print(popularity)

    popularity = dict(sorted(popularity.items(), key=lambda item: item[1], reverse=True))

    labels = []
    numbers = []
    colors = []

    for x, y in popularity.items():
        labels.append(f"{x} ({y})")
        numbers.append(y)
        colors.append(region_colors[x])


    plt.pie(numbers, labels=labels, startangle=90, colors)

    plt.axis('equal')
    plt.savefig('/home/khun/LorDecoder/output/posting/region_pie.png')

    return popularity 

def generate_player_stats():
    player_stats_string = ''
    players = connection.get_players() 
    matches = connection.get_matches()

    matches_last_day = []

    for each in matches:
        try:
            match_time = each["info"]["game_start_time_utc"]

            if each["info"]["game_mode"] == "Constructed" and each["info"]["game_type"] == "Ranked":
                if is_today(match_time):
                    matches_last_day.append(each)
        except Exception as e:
            print(f"We were unable to get match", end='\r')

    player_dict = {}

    players = connection.get_players() 
    for each in players:
        player_dict[each["puuid"]] = 0 

    derbys = []
    
    for match in matches_last_day:  
        participant1, participant2 = match['metadata']['participants'] 
        if participant1 in player_dict:
            player_dict[participant1] += 1
        if participant2 in player_dict:
            player_dict[participant2] += 1

        if participant1 in player_dict and participant2 in player_dict:
            derbys.append(match)

    derby_dict = {}

    for match in derbys:
        players = match['info']['players'] 
        if (players[0]['puuid'], players[1]['puuid']) in derby_dict:
            if players[0]["game_outcome"] == "win":
                derby_dict[(players[0]['puuid'], players[1]['puuid'])]["p0"] +=1
                derby_dict[(players[0]['puuid'], players[1]['puuid'])]["n"] +=1
            else:
                derby_dict[(players[0]['puuid'], players[1]['puuid'])]["p1"] +=1
                derby_dict[(players[0]['puuid'], players[1]['puuid'])]["n"] +=1
        elif  (players[1]['puuid'], players[0]['puuid']) in derby_dict:
            if players[1]["game_outcome"] == "win":
                derby_dict[(players[1]['puuid'], players[0]['puuid'])]["p0"] +=1
                derby_dict[(players[1]['puuid'], players[0]['puuid'])]["n"] +=1
            else:
                derby_dict[(players[1]['puuid'], players[0]['puuid'])]["p1"] +=1
                derby_dict[(players[1]['puuid'], players[0]['puuid'])]["n"] +=1
        else:
            if players[0]["game_outcome"] == "win":
                derby_dict[(players[0]['puuid'], players[1]['puuid'])] = { "p0" : 1, "p1" : 0, "n" : 1}
            else:
                derby_dict[(players[0]['puuid'], players[1]['puuid'])] = { "p0" : 0, "p1" : 1, "n" : 1}

    derby_dict_names = {}
    for key in derby_dict:
        name0 = connection.find_player(key[0])["gameName"]
        name1 = connection.find_player(key[1])["gameName"]
        derby_dict_names[(name0, name1)] = derby_dict[key]

    players = connection.get_players() 
    player_stats_string += f"Мы собрали {len(matches)} матчей {len(players)} игроков, из них мы смогли получить {len(matches_last_day)} ранкед игр за последний день. {len(derbys)} раз игроки встретились друг с другом.\n\n"

    max_puuid = max(player_dict, key=player_dict.get)

    tryharder = connection.find_player(max_puuid)
    tryharder = tryharder["gameName"] 

    player_matches = connection.find_player_matches(max_puuid) 
    random.shuffle(player_matches)

    tryharder_decks = []
    for match in player_matches:
        players = match['info']['players'] 
        match_time = match["info"]["game_start_time_utc"]

        if match["info"]["game_mode"] == "Constructed" and match["info"]["game_type"] == "Ranked":
            if is_today(match_time):
                for player in players:
                    if player['puuid'] == max_puuid:
                        if player['game_outcome'] == 'win':
                            tryharder_decks.append(player["deck_code"])

    player_results = {}

    players = connection.get_players() 
    for player in players:
        player_results[player["puuid"]] = { "win": 0, "loss": 0}

    player_decks = []
    for player in players:
        player_matches = connection.find_player_matches(player["puuid"]) 
        for match in player_matches:
            participants = match['info']['players'] 
            match_time = match["info"]["game_start_time_utc"]
            
            if match["info"]["game_mode"] == "Constructed" and match["info"]["game_type"] == "Ranked":
                if is_today(match_time):
                    for participant in participants:
                        if participant['puuid'] == player["puuid"] and participant["deck_code"] != "":
                            player_decks.append(participant) 
                            player_results[participant['puuid']][participant["game_outcome"]] += 1 
    
    player_results_names = {}
    for puuid in player_results:
        name = connection.find_player(puuid)["gameName"]
        player_results_names[name] = player_results[puuid]

    decks = {}
    for deck in player_decks:
        if deck["deck_code"] not in decks:
            decks[deck["deck_code"]] = 1
        else:
            decks[deck["deck_code"]] += 1

    most_popular_deck = max(decks, key=decks.get)

    deck_code = None
    for deck in tryharder_decks:
        if deck != most_popular_deck:
            deck_code = deck 

    player_stats_string += f"Больше всего игр ({player_dict[max_puuid]}) сыграл {tryharder} \n"
    if deck_code:
        location = "/home/khun/LorDecoder/output/posting/deck.png"
        generate_image(["moba", deck_code], 0, connection, location)

        player_stats_string += "Случайная колода на которой он одержал победу:\n"
        player_stats_string += generate_deck_desc(deck_code)
    else:
        player_stats_string += "Его колода совпадает с самой популярной за сегодня.\n"
        

    
    location = "/home/khun/LorDecoder/output/posting/most_popular_deck.png"
    generate_image(["moba", most_popular_deck], 0, connection, location)


    player_stats_string += f"\nСамая популярная колода среди наших игрков сегодня ({decks[most_popular_deck]} игр):\n"
    player_stats_string += generate_deck_desc(most_popular_deck)

    player_stats_string += "\nИгроки регона по количеству побед за сегодня: \n"
    for s in sorted(player_results_names.items(), key=lambda k_v: k_v[1]['win'], reverse=True):
        if s[1]["win"] > 0:
            player_stats_string += f"{s[0]} - побед: {s[1]['win']} поражений: {s[1]['loss']}\n"
    
    if len(derby_dict_names) > 0:
        player_stats_string += f"\nСамые жаркие баталии за последние сутки:\n"
        for s in sorted(derby_dict_names.items(), key=lambda k_v: k_v[1]['n'], reverse=True):
            player_stats_string += f"{s[0][0]} {s[1]['p0']} - {s[1]['p1']} {s[0][1]}\n"

    players = connection.get_players() 
    player_ids = []
    for player in players:
        player_ids.append(player["puuid"])

    region_popularity = generate_region_popularity(matches, player_ids)
    player_stats_string += "\nПопулярность регионов среди наших игроков:\n"

    for region in region_popularity:
        player_stats_string += f"{region} - {region_popularity[region]}\n"

    return player_stats_string

def is_today(match_time):
    match_time = match_time.split('.')[0]
    date_time_obj = datetime.strptime(match_time, "%Y-%m-%dT%H:%M:%S")

    difference = datetime.utcnow() - date_time_obj
    if difference.days == 0:
        return True 
    else:
        return False

def upload_image(type):
    if type == "random_deck":
        location = "/home/khun/LorDecoder/output/posting/deck.png"
    elif type == "most_popular_deck":
        location = "/home/khun/LorDecoder/output/posting/most_popular_deck.png"
    elif type == "region_pie":
        location = "/home/khun/LorDecoder/output/posting/region_pie.png"

    img = {'photo': ('img.jpg', open(location, 'rb'))}

    # Получаем ссылку для загрузки изображений
    method_url = 'https://api.vk.com/method/photos.getWallUploadServer?'
    data = dict(access_token=token, gid=gid, v='5.126')
    response = requests.post(method_url, data)
    result = json.loads(response.text)

    upload_url = result['response']['upload_url']

    # Загружаем изображение на url
    response = requests.post(upload_url, files=img)
    result = json.loads(response.text)

    # Сохраняем фото на сервере и получаем id
    method_url = 'https://api.vk.com/method/photos.saveWallPhoto?'
    data = dict(access_token=token, gid=gid, photo=result['photo'], hash=result['hash'], server=result['server'], v='5.126')
    response = requests.post(method_url, data)
    result = json.loads(response.text)['response'][0]
    result = "photo{}_{}".format(result["owner_id"], result["id"])

    return result  

def generate_player_data(message):
    headers = {
        "X-Riot-Token": os.getenv("RIOT_API_KEY")
    }

    r = requests.get('https://www.perdere.ru:4444/api/v1/get_leaderboard')

    r = r.json()
    r = r["players"]

    message += "Топ10 игроков из России:\n"
    russian_top = []

    for each in r:
        is_russian = requests.get("https://www.perdere.ru:4444/api/v1/check_ru?name=" + each["name"])
        is_russian = is_russian.json()
        is_russian = is_russian["isRu"]

        if is_russian:
            russian_top.append(each)

        if len(russian_top) > 9:
            break

    i = 0
    for i, player in enumerate(russian_top):
        player_string = "%s(%s). %s %s LP\n" % ((i+1), player["rank"], player["name"], player["lp"])
        message += player_string

    return message

def generate_normal_post():
    photo_ids = []
    message = "Папешикам ку, \n"

    try:
        message += generate_player_stats()
        photo_ids.append(upload_image("random_deck"))
        photo_ids.append(upload_image("most_popular_deck"))
        photo_ids.append(upload_image("region_pie"))
        message += "\n"
        message += ("&#10084;" * 10)
        message += "\n"
    except Exception as e:
        traceback.print_exc()
        message += "Не удалось получить статистику игроков. Блип-блоп.\n"

    try:
        player_message = generate_player_data("")
        message += player_message
    except:
        traceback.print_exc()
        message += "Не удалось получить данные игроков. Блип-блоп.\n"

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
