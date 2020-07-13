# coding=utf-8
import os
from dotenv import load_dotenv, find_dotenv
import vk_api
import requests
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from datetime import datetime
from main import generate_image
from cardsearch import find_card
from banbot import BanRoom
import time
import re
import traceback

allowed_code_list = ["код:", "код" ,"code", "code:"]

base_time = datetime(1970,1,1)

# vk_session = vk_api.VkApi(token=os.environ['VKAPI_KEY'])

load_dotenv(find_dotenv())

vk_session = vk_api.VkApi(token=os.getenv("VKAPI_KEY"))
longpoll = VkBotLongPoll(vk_session, "196727308")
vk = vk_session.get_api()
while True:
    try:
        for event in longpoll.listen():
            print(event)
            if event.type == VkBotEventType.MESSAGE_NEW and event.message.text:
                # print(event.message.text)

                message_text = re.sub('\[.*\],?\s*','',event.message.text)
                # print(message_text)

                peer_id = event.message["peer_id"]
                user_get=vk.users.get(user_ids = (event.message.from_id))
                user_get=user_get[0]
                first_name=user_get['first_name']

                try:
                    args = re.sub("[^\w\-\/]", " ", message_text).split()
                    # print(parameter)
                    # print(args)
                    if args[0].lower() in allowed_code_list and len(args) == 2:
                        try:
                            generate_image(args[1], user_get["id"])

                            server = vk.photos.getMessagesUploadServer()
                            b = requests.post(server['upload_url'], files={'photo': open('output/output.png', 'rb')}).json()
                            params = {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']}
                            c = vk.photos.saveMessagesPhoto(**params)[0]
                            d = "photo{}_{}".format(c["owner_id"], c["id"])

                            vk.messages.send(peer_id=peer_id,
                                message="", random_id=(datetime.utcnow()-base_time).total_seconds(), attachment = d)
                        except TypeError:
                            vk.messages.send(peer_id=peer_id,
                                message='Блип-блоп, глупый бот не пониимет код', random_id=(datetime.utcnow()-base_time).total_seconds())
                    elif args[0].lower() == "карта":
                        try:
                            source = 0 # 0 for PM, 1 for group chat
                            if event.message.from_id == event.message.peer_id:
                                source = 0
                            else:
                                source = 1
                            code = find_card(source, args[1:])
                            # print('ru_ru/img/cards/' + code + '.png')
                            server = vk.photos.getMessagesUploadServer()
                            b = requests.post(server['upload_url'], files={'photo': open('ru_ru/img/cards/' + code + '.png', 'rb')}).json()
                            params = {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']}
                            c = vk.photos.saveMessagesPhoto(**params)[0]
                            d = "photo{}_{}".format(c["owner_id"], c["id"])

                            vk.messages.send(peer_id=peer_id,
                                message="", random_id=(datetime.utcnow()-base_time).total_seconds(), attachment = d)
                        except:
                            traceback.print_exc()
                            if source == 0:
                                vk.messages.send(peer_id=peer_id,
                                    message='Блип-блоп, глупый бот не нашёл карту', random_id=(datetime.utcnow()-base_time).total_seconds())
                    # elif args[0].lower() == "привет":
                    #     room = BanRoom()

                except ValueError:
                    pass
    except requests.exceptions.ReadTimeout:
        print("\n Переподключение к серверам ВК \n")
        time.sleep(3)
