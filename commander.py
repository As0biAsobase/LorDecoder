from command_enum import Command
from mode_enum import Mode
from main import generate_image
from cardsearch import find_card
from meta_stats import query_archetype_wr
from calculator import Calculator
from deckchanges import get_highest_growth
from card_guesser import Guesser
from database import DBConnection

import requests
import traceback
import json
import re
import random
from random import randrange, choice


class Commander:

    def __init__(self):
        # Database connection object
        self.connection = DBConnection()
        # TODO: mode switching
        self.now_mode = Mode.default
        self.last_mode = Mode.default

        self.last_command = None
        # Should be used for mode switching
        self.last_ans = None
        # Calculator feature is deleted
        # TODO: Either delete it completed or re-implement
        self.calculator_params = []

        self.guesser = None

    def change_mode(self, to_mode):
        # Used for mode switching
        self.last_mode = self.now_mode
        self.now_mode = to_mode
        self.last_ans = None

    def input(self, server, msg, sender, source_id):
        # account for different ways bot can be mentioned in a chat
        message_text = re.sub('\[.*\],?\s*','', msg)

        source = 0 # 0 for PM, 1 for group chat
        if sender["id"] == source_id:
            source = 0
        else:
            source = 1

        keyboard = ""

        try:
            # split user message into command itself and arguments
            args = re.sub("[^\w\-\/]", " ", message_text).split()

            # empty message (i.e. emoji was sent)
            if len(args) == 0:
                if source == 0:
                    keyboard = "keyboards/default_keyboard.json"

                    return ["Блип-блоп, пустое сообщене", "", keyboard]
                else:
                    return ["", "", "keyboards/empty.json"]

            # default mode is only one atm
            if self.now_mode == Mode.default:
                # send link to info article
                if args[0].lower() in Command.info_list.value:
                    if source == 0:
                        keyboard = "keyboards/default_keyboard.json"

                    return ["Вся информация в этой статье: vk.com/@natum_perdere-natum-perdere-instrukciya-po-primeneniu", "", keyboard]

                # Process code and send deck image
                if args[0].lower() in Command.code_list.value and len(args) >= 2:
                    try:
                        generate_image(args, sender["id"], self.connection, "output/output.png")

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

                # Process card name and send matching image
                elif args[0].lower() in Command.card_list.value:
                    try:
                        code = find_card(source, args[1:], self.connection)
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
                elif args[0].lower() in Command.guesser_list.value:
                    try:
                        if source != 0:
                            if self.guesser == None:
                                randomize = random.random()
                                if randomize < 0.34:
                                    source = "flavorText"
                                elif randomize < 0.67:
                                    source = "flavorText"
                                else:
                                    source = "image"

                                increase = 1
                                decrease = 0

                                self.guesser = Guesser(source_id, increase, decrease, source)
                                if source != "image":
                                    self.guesser.generate_text_quiz(self.connection)
                                    d = ""
                                else:
                                    self.guesser.generate_image_quiz(self.connection)
                                    d = server.upload_quiz_image()
                            else:
                                return ["Сначала реши предыдущую загадку!", "", keyboard]

                            if source == 0:
                                keyboard = "keyboards/default_keyboard.json"

                            return[self.guesser.question, d, keyboard]
                    except:
                        traceback.print_exc()
                        if source == 0:
                            return ["Блип-блоп, глупый бот смог создать викторину", "", keyboard]

                elif args[0].lower() in Command.make_a_guess_list.value:
                    try:
                        if source != 0:
                            if self.guesser == None:
                                return ["Я ещё ничего не загадал...!", "", keyboard]
                            else:
                                if self.guesser.make_a_guess(args[1]) == True:
                                    self.connection.increaseUserRating(sender["id"], self.guesser.increase)

                                    text = "МОЛОДЕЦ!"

                                    result, rating = self.connection.getUserRating(sender["id"])
                                    text += "\nТвой счёт: %s. Место: %s" % (result["score"], rating)
                                    self.guesser = None
                                else:
                                    self.connection.decreaseUserRating(sender["id"], self.guesser.decrease)
                                    text = "Чел, ты..."

                                    result, rating = self.connection.getUserRating(sender["id"])
                                    text += "\nТвой счёт: %s. Место: %s" % (result["score"], rating)

                            if source == 0:
                                keyboard = "keyboards/default_keyboard.json"

                            return[text, "", keyboard]
                    except:
                        traceback.print_exc()
                        if source == 0:
                            return ["Блип-блоп, глупый бот смог создать викторину", "", keyboard]

                elif args[0].lower() in Command.show_leaderboard_list.value:
                    try:
                        if source != 0:
                            leaderboard = self.connection.getUserLeaderboard()
                            text = ""

                            for i in range(min(10, len(leaderboard))):
                                user = server.get_user_from_id(leaderboard[i]["user"])

                                text += "%s. @id%s (%s): %s \n" % (i+1, user["id"], user["first_name"], leaderboard[i]["score"])

                            if source == 0:
                                keyboard = "keyboards/default_keyboard.json"

                            return[text, "", keyboard]
                    except:
                        traceback.print_exc()
                        if source == 0:
                            return ["Блип-блоп, глупый бот смог создать викторину", "", keyboard]
                elif args[0].lower() == "колода" and args[1].lower() == "рвущая":
                    try:
                        r = requests.get('https://lor.mobalytics.gg/api/v2/meta/statistics/decks?sortBy=winRateDesc&from=0&count=100')

                        for deck in r.json()["decksStats"]:
                            if deck["matchesCollected"] > 2000:
                                my_deck = deck
                                break

                        generate_image(["moba", my_deck["cardsCode"]], sender["id"], self.connection, "output/output.png")

                        d = server.upload_deck_image()

                        winrate = round(my_deck["matchesWin"] / my_deck["matchesCollected"], 4) * 100
                        winrate = str(winrate)
                        winrate = winrate[0:5:]

                        if source == 0:
                            keyboard = "keyboards/default_keyboard.json"

                        response_str = "Колода: %s \nМатчей сыграно: %s \nПобед: %s\nВинрейт: %s%%" % (my_deck["cardsCode"], my_deck["matchesCollected"], my_deck["matchesWin"], winrate)

                        return [response_str, d, keyboard]
                    except:
                        traceback.print_exc()
                        if source == 0:
                            keyboard = "keyboards/default_keyboard.json"
                            return ["Блип-блоп, глупый бот улетел, хихи", "", keyboard]

                elif args[0].lower() == "колода" and args[1].lower() == "случайная":
                    try:
                        r = requests.get('https://lor.mobalytics.gg/api/v2/meta/statistics/decks?from=0&count=100')

                        r = r.json()
                        r = r["decksStats"]
                        my_deck = r[randrange(len(r)-1)]

                        generate_image(["moba", my_deck["cardsCode"]], sender["id"], self.connection, "output/output.png")

                        d = server.upload_deck_image()

                        winrate = round(my_deck["matchesWin"] / my_deck["matchesCollected"], 4) * 100
                        winrate = str(winrate)
                        winrate = winrate[0:5:]

                        if source == 0:
                            keyboard = "keyboards/default_keyboard.json"

                        response_str = "Колода: %s \nМатчей сыграно: %s \nПобед: %s\nВинрейт: %s%%" % (my_deck["cardsCode"], my_deck["matchesCollected"], my_deck["matchesWin"], winrate)

                        return [response_str, d, keyboard]
                    except:
                        traceback.print_exc()
                        if source == 0:
                            keyboard = "keyboards/default_keyboard.json"
                            return ["Блип-блоп, глупый бот улетел, хихи", "", keyboard]

                elif args[0].lower() == "колода" and args[1].lower() == "растущая":
                    try:
                        decks = get_highest_growth()
                        max_deck = decks[0]
                        max_previous = decks[1]

                        generate_image(["moba", max_deck["cardsCode"]], sender["id"], self.connection, "output/output.png")

                        d = server.upload_deck_image()

                        new_winrate = round(max_deck["matchesWin"] / max_deck["matchesCollected"], 4) * 100
                        old_winrate = round(max_previous["matchesWin"] / max_previous["matchesCollected"], 4) * 100

                        new_winrate = str(new_winrate)
                        new_winrate = new_winrate[0:5:]
                        old_winrate = str(old_winrate)
                        old_winrate = old_winrate[0:5:]

                        if source == 0:
                            keyboard = "keyboards/default_keyboard.json"

                        response_str = """Колода: %s \nМатчей сыграно: %s > %s \nПобед: %s > %s \nВинрейт: %s%% > %s""" % (max_deck["cardsCode"], max_previous["matchesCollected"], max_deck["matchesCollected"], max_previous["matchesWin"], max_deck["matchesWin"], old_winrate, new_winrate)

                        return [response_str, d, keyboard]
                    except:
                        traceback.print_exc()
                        if source == 0:
                            keyboard = "keyboards/default_keyboard.json"
                            return ["Блип-блоп, глупый бот улетел, хихи", "", keyboard]
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
                        # print(name)

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
