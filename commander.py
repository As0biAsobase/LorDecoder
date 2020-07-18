from command_enum import Command
from mode_enum import Mode
import re
from main import generate_image
from cardsearch import find_card
from calculator import Calculator
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
            # print(parameter)
            # print(args)
            if args[0].lower() in Command.ban_list.value and self.now_mode != Mode.ban and source == 0:
                self.change_mode(Mode.ban)
                self.last_command = args[0].lower()

                keyboard = "keyboards/ban_mode_selection.json"

                return ["Вы вошли в режим банов, выберите настроки (количество банов/количество колод)", "", keyboard]
            elif args[0].lower() in Command.calculator_list.value and self.now_mode != Mode.calculator and source == 0:
                self.change_mode(Mode.calculator)
                self.last_command = args[0].lower()

                keyboard = "keyboards/calculator/type.json"

                return ["Покулюляторим?", "", keyboard]
            elif args[0].lower() in Command.default_list.value and self.now_mode != Mode.default:
                self.change_mode(Mode.default)
                self.last_command = args[0].lower()

                keyboard = "keyboards/default_keyboard.json"

                return ["Вы вернулись в главное меню", "", keyboard]

            if args[0].lower() in Command.back_list.value:
                if self.now_mode != Mode.default:
                    self.change_mode(Mode.default)
                    self.last_command = args[0].lower()

                    keyboard = "keyboards/default_keyboard.json"

                    return ["Вы вернулись в главное меню", "", keyboard]

            if self.now_mode == Mode.default:
                if args[0].lower() in Command.info_list.value:
                    if source == 0:
                        keyboard = "keyboards/default_keyboard.json"

                    return ["Вся информация в этой статье: vk.com/@natum_perdere-natum-perdere-instrukciya-po-primeneniu", "", keyboard]

                if args[0].lower() in Command.code_list.value and len(args) == 2:
                    try:
                        generate_image(args[1], sender["id"])
                        d = server.upload_deck_image()

                        print(d)

                        if source == 0:
                            keyboard = "keyboards/default_keyboard.json"

                        return ["", d, keyboard]
                    except TypeError:
                        return ["Блип-блоп, глупый бот не пониимет код", "", keyboard]

                elif args[0].lower() == "карта":
                    try:
                        code = find_card(source, args[1:])
                        # print('ru_ru/img/cards/' + code + '.png')
                        d = server.upload_card_image(code)

                        if source == 0:
                            keyboard = "keyboards/default_keyboard.json"

                        return["", d, keyboard]
                    except:
                        traceback.print_exc()
                        if source == 0:
                            return["Блип-блоп, глупый бот не нашёл карту", "", keyboard]
                else:
                    keyboard = "keyboards/default_keyboard.json"

                    return["Блип-блоп, не очень тебя понял", "", keyboard]

            elif self.now_mode == Mode.calculator:
                if (len(self.calculator_params) == 0 or len(self.calculator_params) == 5) and args[0].lower() in Command.hypergeom_list.value:
                    self.calculator_params = []
                    self.calculator_params.append("hypergeom")


                    return["Блип-блоп калькуятор, введите размер колоды (population size)", "", "keyboards/empty.json"]

                elif len(args) == 1 and args[0].isdigit():
                    if len(self.calculator_params) == 1:
                        self.calculator_params.append(args[0])

                        return["Размер колоды: " + str(args[0]) + "\nСколько нужных карт всего?", "", "keyboards/empty.json"]
                    elif len(self.calculator_params) == 2:
                        self.calculator_params.append(args[0])

                        return["Нужных карт: " + str(args[0]) + "\nСколько подровались?", "", "keyboards/empty.json"]
                    elif len(self.calculator_params) == 3:
                        self.calculator_params.append(args[0])

                        return["Подровались " + str(args[0]) + " раз \nСколько хотим увидеть?", "", "keyboards/empty.json"]
                    elif len(self.calculator_params) == 4:
                        self.calculator_params.append(args[0])

                        с = Calculator()

                        self.change_mode(Mode.default)
                        keyboard = "keyboards/default_keyboard.json"
                        print(self.calculator_params)
                        return["Вероятность данного блип-блопа: " +
                        str(round(с.hypergeom_pmf(int(self.calculator_params[1]), int(self.calculator_params[2]), int(self.calculator_params[3]), int(self.calculator_params[4])), 2))
                        , "", keyboard]



        except ValueError:
            pass
