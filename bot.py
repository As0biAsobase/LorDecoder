# coding=utf-8
import os
from dotenv import load_dotenv, find_dotenv
import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import datetime
from main import generate_image

base_time = datetime(1970,1,1)

# echo "export VKAPI_KEY=574b15b58c2a8c86474fe862c09f38d8b7826d4b3f4df70e48bd72fc7272b73100ab0eb7e962169334834" >> .env

# ROOT_DIR = os.path.dirname(os.path.abspath(os.path.dirname( __file__ )))
# # CONFIG_PATH = os.path.join(ROOT_DIR, 'DecoderBot')
# project_folder = os.path.expanduser(ROOT_DIR)  # adjust as appropriate
# print(project_folder)
load_dotenv(find_dotenv())
# print("jkjh")
vk_session = vk_api.VkApi(token=os.getenv("VKAPI_KEY"))
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        generate_image(event.text)

        server = vk.photos.getMessagesUploadServer()
        b = requests.post(server['upload_url'], files={'photo': open('output/output.png', 'rb')}).json()
        params = {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']}
        c = vk.photos.saveMessagesPhoto(**params)[0]
        d = "photo{}_{}".format(c["owner_id"], c["id"])

        vk.messages.send( #Отправляем сообщение
            user_id=event.user_id,
            message='test', random_id=(datetime.utcnow()-base_time).total_seconds(),
            attachment = d)
   #Слушаем longpoll, если пришло сообщение то:
        if event.text == 'test' or event.text == 'Второй вариант фразы': #Если написали заданную фразу
            if event.from_user: #Если написали в ЛС
                vk.messages.send( #Отправляем сообщение
                    user_id=event.user_id,
                    message='test', random_id=(datetime.utcnow()-base_time).total_seconds())
            elif event.from_chat: #Если написали в Беседе
                vk.messages.send( #Отправляем собщение
                    chat_id=event.chat_id,
                    message='Ваш текст')
