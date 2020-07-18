import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import time
from datetime import datetime
import requests
from commander import Commander

class Server:
    base_time = datetime(1970,1,1)

    def __init__(self, api_token, group_id, server_name: str="Empty"):
        # Даем серверу имя
        self.server_name = server_name

        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)

        # Для использования Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id)

        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()

        self.users = {}

    def send_msg(self, send_id, response):
        try:
            print([send_id, response[0], response[1], response[2]])
            self.vk_api.messages.send(peer_id=send_id,
                                  message=response[0],
                                  attachment=response[1],
                                  random_id=(datetime.utcnow()-Server.base_time).total_seconds(),
                                  keyboard=open(response[2] if len(response)>2 else "keyboards/empty.json", "r", encoding="UTF-8").read())
        except TypeError:
            pass

    def start(self):
        while True:
            try:
                for event in self.long_poll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW and event.message.text:
                        if event.object.from_id not in self.users:
                            self.users[event.object.from_id] = Commander()

                        if event.type == VkBotEventType.MESSAGE_NEW:
                            print(event.message.from_id)
                            sender = self.vk_api.users.get(user_ids = (event.message.from_id))
                            sender = sender[0]
                            # print(self.users[event.object.from_id].input(self, event.message.text, sender, event.message.peer_id))
                            self.send_msg(event.message.peer_id,
                                      self.users[event.object.from_id].input(self, event.message.text, sender, event.message.peer_id))

            except requests.exceptions.ReadTimeout:
                print("\n Переподключение к серверам ВК \n")
                time.sleep(100)

    def upload_deck_image(self):
        server = self.vk_api.photos.getMessagesUploadServer()
        b = requests.post(server['upload_url'], files={'photo': open('output/output.png', 'rb')}).json()
        params = {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']}
        c = self.vk_api.photos.saveMessagesPhoto(**params)[0]
        d = "photo{}_{}".format(c["owner_id"], c["id"])
        return d

    def upload_card_image(self, code):
        server = self.vk_api.photos.getMessagesUploadServer()
        b = requests.post(server['upload_url'], files={'photo': open('ru_ru/img/cards/' + code + '.png', 'rb')}).json()
        params = {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']}
        c = self.vk_api.photos.saveMessagesPhoto(**params)[0]
        d = "photo{}_{}".format(c["owner_id"], c["id"])
        return d

    def test(self):
        # Посылаем сообщение пользователю с указанным ID
        self.send_msg(151646757, "Привет-привет!")
