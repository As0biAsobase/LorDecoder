import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api import VkUpload
import time
from datetime import datetime
import requests
from commander import Commander
import traceback
from datetime import datetime

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
        # self.vk = self.vk.get_api()
        self.vk = self.vk.get_api()

        self.upload = VkUpload(self.vk)

        self.users = {}
        self.msg_counter = 0

    def send_msg(self, send_id, response):
        try:
            print([send_id, response[0], response[1], response[2]])

            self.vk.messages.send(peer_id=send_id,
                                  message=response[0],
                                  attachment=response[1],
                                  random_id=(datetime.utcnow()-Server.base_time).total_seconds(),
                                  keyboard=open(response[2] if response[2] else "keyboards/empty.json", "r", encoding="UTF-8").read())
        except TypeError:
            pass
        except vk_api.exceptions.ApiError:
            traceback.print_exc()
            print("Факир был пьян, сообщение не отправилось")

    def start(self):
        while True:
            try:
                for event in self.long_poll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW and event.message.text:
                        self.msg_counter += 1

                        now = datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                        if event.message.peer_id not in self.users:
                            self.users[event.message.peer_id] = Commander()

                        print("%s Users since last restart: %s, messages since last restart:%s" % (dt_string, len(self.users), self.msg_counter))

                        if event.type == VkBotEventType.MESSAGE_NEW:
                            # print(event.message.from_id)
                            sender = self.vk.users.get(user_ids = (event.message.from_id))
                            sender = sender[0]
                            # print([event.message.peer_id, event.message.from_id])
                            self.send_msg(event.message.peer_id,
                                      self.users[event.message.peer_id].input(self, event.message.text, sender, event.message.peer_id))

            except requests.exceptions.ReadTimeout:
                print("\n Переподключение к серверам ВК \n")
                time.sleep(100)
            except KeyboardInterrupt:
                sys.exit()
            except:
                print("\n Что-то пошло не так \n")
                traceback.print_exc()

    def upload_deck_image(self):
        server = self.vk.photos.getMessagesUploadServer()
        b = requests.post(server['upload_url'], files={'photo': open('output/output.png', 'rb')}).json()
        params = {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']}
        c = self.vk.photos.saveMessagesPhoto(**params)[0]
        d = "photo{}_{}".format(c["owner_id"], c["id"])
        return d

    def upload_deck_file(self, sender):
        server = self.vk.docs.getMessagesUploadServer(peer_id = sender)
        b = requests.post(server['upload_url'], files={'file': open('output/output.png', 'rb')})
        # print(b.text)
        params = {'file': b.json()['file']}
        c = self.vk.docs.save(**params)
        # print(c["doc"])
        d = "doc{}_{}".format(c["doc"]["owner_id"], c["doc"]["id"])
        return d

    def upload_card_image(self, code):
        server = self.vk.photos.getMessagesUploadServer()
        b = requests.post(server['upload_url'], files={'photo': open('ru_ru/img/cards/' + code + '.png', 'rb')}).json()
        params = {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']}
        c = self.vk.photos.saveMessagesPhoto(**params)[0]
        d = "photo{}_{}".format(c["owner_id"], c["id"])
        return d

    def upload_card_file(self, sender, code):
        server = self.vk.docs.getMessagesUploadServer(peer_id = sender)
        b = requests.post(server['upload_url'], files={'file': open('ru_ru/img/cards/' + code + '.png', 'rb')})
        params = {'file': b.json()['file']}
        c = self.vk.docs.save(**params)
        d = "doc{}_{}".format(c["doc"]["owner_id"], c["doc"]["id"])
        return d

    def test(self):
        # Посылаем сообщение пользователю с указанным ID
        self.send_msg(151646757, "Привет-привет!")

    def get_user_from_id(self, user_id):
        response = self.vk.users.get(user_ids=int(user_id))
        response = response[0]
        return response

    def get_chat_users(self, peer_id):
        response = self.vk.messages.getConversationMembers(peer_id=peer_id)


        return response["profiles"]
