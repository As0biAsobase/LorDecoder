# coding=utf-8
import os
from dotenv import load_dotenv, find_dotenv
import vk_api
import requests
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from datetime import datetime
from main import generate_image
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

                message_text = re.sub('\[.*\],?\s?','',event.message.text)
                print(message_text)

                peer_id = event.message["peer_id"]
                user_get=vk.users.get(user_ids = (event.message.from_id))
                user_get=user_get[0]
                first_name=user_get['first_name']

                try:
                    command, parameter = message_text.split(" ")
                    # print(parameter)
                    if command.lower() in allowed_code_list:
                        try:
                            generate_image(parameter, user_get["id"])

                            server = vk.photos.getMessagesUploadServer()
                            b = requests.post(server['upload_url'], files={'photo': open('output/output.png', 'rb')}).json()
                            params = {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']}
                            c = vk.photos.saveMessagesPhoto(**params)[0]
                            d = "photo{}_{}".format(c["owner_id"], c["id"])

                            vk.messages.send(peer_id=peer_id,
                                message='Ты ' + first_name + "? Ну раз " + first_name + ", то держи картинку", random_id=(datetime.utcnow()-base_time).total_seconds(), attachment = d)
                        except TypeError:
                            vk.messages.send(peer_id=peer_id,
                                message='Блип-блоп, глупый бот не пониимет код', random_id=(datetime.utcnow()-base_time).total_seconds())
                except ValueError:
                    traceback.print_exc()
                     # print(message_text.split(" ")[0])
                     # pass
    except requests.exceptions.ReadTimeout:
        print("\n Переподключение к серверам ВК \n")
        time.sleep(3)
