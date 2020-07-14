from command_enum import Command
from mode_enum import Mode
import re
from main import generate_image
from cardsearch import find_card
import requests
import traceback

class Commander:

    def __init__(self):
        # Текущий, предыдущий режимы
        self.now_mode = Mode.default
        self.last_mode = Mode.default

        self.last_command = None
        # Для запомминания ответов пользователя
        self.last_ans = None

    def change_mode(self, to_mode):

        self.last_mode = self.now_mode
        self.now_mode = to_mode

        self.last_ans = None

    def input(self, server, msg, sender, source_id):
        message_text = re.sub('\[.*\],?\s*','', msg)

        source = 0 # 0 for PM, 1 for group chat
        if sender["id"] == source_id:
            source = 0
        else:
            source = 1

        try:
            args = re.sub("[^\w\-\/]", " ", message_text).split()
            # print(parameter)
            # print(args)
            if args[0].lower() in Command.code_list.value and len(args) == 2:
                try:
                    generate_image(args[1], sender["id"])
                    d = server.upload_deck_image()

                    print(d)
                    return ["", d]
                except TypeError:
                    return ["Блип-блоп, глупый бот не пониимет код", ""]

            elif args[0].lower() == "карта":
                try:
                    code = find_card(source, args[1:])
                    # print('ru_ru/img/cards/' + code + '.png')
                    d = server.upload_card_image(code)

                    return["", d]
                except:
                    traceback.print_exc()
                    if source == 0:
                        return["Блип-блоп, глупый бот не нашёл карту", ""]

        except ValueError:
            pass
