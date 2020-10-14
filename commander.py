from command_enum import Command
from mode_enum import Mode
import re
from main import generate_image
from cardsearch import find_card
from meta_stats import query_archetype_wr
from calculator import Calculator
import requests
import traceback
import json
from random import randrange, choice

class Commander:

    def __init__(self):
        # Текущий, предыдущий режимы
        self.now_mode = Mode.default
        self.last_mode = Mode.default

        self.last_command = None
        # Для запомминания ответов пользователя
        self.last_ans = None
        self.calculator_params = []

    def change_mode(self, to_mode):

        self.last_mode = self.now_mode
        self.now_mode = to_mode

        self.last_ans = None

    def input(self, server, msg, sender, source_id):
        # print(self.now_mode)
        message_text = re.sub('\[.*\],?\s*','', msg)

        source = 0 # 0 for PM, 1 for group chat
        if sender["id"] == source_id:
            source = 0
        else:
            source = 1

        keyboard = ""

        try:
            args = re.sub("[^\w\-\/]", " ", message_text).split()

            if len(args) == 0:
                if source == 0:
                    keyboard = "keyboards/default_keyboard.json"

                    return ["Блип-блоп, пустое сообщене", "", keyboard]
                else:
                    return ["", "", "keyboards/empty.json"]

            if self.now_mode == Mode.default:
                if args[0].lower() in Command.info_list.value:
                    if source == 0:
                        keyboard = "keyboards/default_keyboard.json"

                    return ["Вся информация в этой статье: vk.com/@natum_perdere-natum-perdere-instrukciya-po-primeneniu", "", keyboard]

                if args[0].lower() in Command.code_list.value and len(args) >= 2:
                    try:
                        generate_image(args, sender["id"])

                        if "пнг" in args:
                            d = server.upload_deck_file(sender["id"])
                        else:
                            d = server.upload_deck_image()

                        print(d)

                        if source == 0:
                            keyboard = "keyboards/default_keyboard.json"

                        return ["", d, keyboard]
                    except TypeError:
                        traceback.print_exc()
                        return ["Блип-блоп, глупый бот не пониимет код", "", keyboard]

                elif args[0].lower() == "карта":
                    try:
                        code = find_card(source, args[1:])
                        # print('ru_ru/img/cards/' + code + '.png')
                        if "пнг" in args:
                            d = server.upload_card_file(sender["id"], code)
                        else:
                            d = server.upload_card_image(code)


                        if source == 0:
                            keyboard = "keyboards/default_keyboard.json"

                        return["", d, keyboard]
                    except:
                        traceback.print_exc()
                        if source == 0:
                            return ["Блип-блоп, глупый бот не нашёл карту", "", keyboard]
                elif args[0].lower() == "iq":
                    try:
                        if sender["id"] == 177252253:
                            iq = 12
                        elif sender["id"] == 488352580:
                            iq = -3
                        else:
                            iq = randrange(100)

                        return [str(iq), "", keyboard]

                    except:
                        traceback.print_exc()
                elif args[0].lower() == "посрать":
                    try:
                        user_list = server.get_chat_users(source_id)
                        user = choice(user_list)
                        id = user["id"]
                        name = user["first_name"]
                        print(name)

                        # response_str = "@id" + str(sender["id"]) + " (" + sender["first_name"] +") пытался насрать под дверь стримеру, но попал в @id" + str(id) + " (" + name + ")"
                        response_str = "@id%s (%s) пытался насрать под дверь админам, но попал в @id%s (%s)" % (sender["id"], sender["first_name"], id, name)

                        return [response_str, "", keyboard]

                    except:
                        traceback.print_exc()
                else:
                    if source == 0:
                        keyboard = "keyboards/default_keyboard.json"

                        return ["Блип-блоп, не очень тебя понял", "", keyboard]


        except ValueError:
            pass
