import random
import re

class Guesser:
    factions = [
        "Иония",
        "Ноксус",
        "Демасия",
        "Пилтовер и Заун",
        "Фрельйорд",
        "Сумрачные острова",
        "Билджвотер",
        "Таргон",
        "Шурима"
    ]

    def __init__(self, chat):
        self.chat = chat
        self.correct_answer = None
        self.options = []
        self.question = ""
        pass

    def generate_quiz(self, connection):
        card_list = connection.getCardsByRegion(random.choice(Guesser.factions))
        self.options = random.sample(card_list, 4)
        self.correct_answer = random.choice(self.options)

        self.question = self.generate_question()


    def generate_question(self):
        question  = self.obfuscate_text(self.correct_answer["flavorText"])
        question += "\n Варианты ответа:"

        for i in range(len(self.options)):
            if self.options[i]["supertype"] == "Чемпион":
                if len(self.options[i]["cardCode"]) > 6:
                    name = self.options[i]["name"] + " 2"
                else:
                    name = self.options[i]["name"]
            else:
                name = self.options[i]["name"]

            question += "\n %s. %s" % (i+1, name)
        return question

    def obfuscate_text(self, text):
        text = text.split()
        new_text = ""
        for each in text:
            if random.random() < 0.25:
                new_text += "*** "
            else:
                new_text += each + " "

        return new_text

    def make_a_guess(self, guess):
        if len(guess) == 1:
            position = int(guess) - 1
            if self.options[position] == self.correct_answer:
                return True
            else:
                return False
        else:
            return False
