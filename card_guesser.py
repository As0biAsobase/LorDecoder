import random
import re
from PIL import Image, ImageOps
from PIL import ImageFilter
import PIL.ImageDraw as ImageDraw
import time

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

    def __init__(self, chat, increase, decrease, source, created_at):
        self.chat = chat
        self.correct_answer = None
        self.options = []
        self.question = ""

        self.increase = increase
        self.decrease = decrease
        self.source = source
        self.created_at = created_at

    def check_cd_passed(self, cd):
        elapsed = time.time() - self.created_at
        if (elapsed > cd):
            return True, 0
        else:
            return False, cd-elapsed

    def generate_text_quiz(self, connection):
        card_list = connection.getCardsByRegion(random.choice(Guesser.factions), "Set5")
        self.options = random.sample(card_list, 4)
        self.correct_answer = random.choice(self.options)

        self.question = self.generate_question()

    def generate_image_quiz(self, connection):
        card_list = connection.getCardsByRegion(random.choice(Guesser.factions), "Set5")
        self.options = random.sample(card_list, 4)
        self.correct_answer = random.choice(self.options)

        self.generate_image()
        self.question = self.generate_question()

    def generate_image(self):
        image = Image.open("/home/khun/LorDecoder/ru_ru/img/cards/%s-full.png" % (self.correct_answer["cardCode"]))
        width, height = image.size

        randomize = random.random()
        if randomize < 0.34:
            self.increase = 2
            self.decrease = 1

            image = image.filter(ImageFilter.GaussianBlur(radius=3))
        elif randomize < 0.90:
            self.increase = 1
            self.decrease = 0
        elif randomize < 0.98:
            self.increase = 5
            self.decrease = 4

            image = ImageOps.grayscale(image)
        else:
            self.increase = 20
            self.decrease = 19

            image = image.filter(ImageFilter.GaussianBlur(radius=3))
            image = ImageOps.grayscale(image)

        if self.correct_answer["type"] == "Боец":
            starting_width = random.randrange(0, width*0.875)
            starting_height = random.randrange(0, height*0.875)
            image = image.crop((starting_width, starting_height, starting_width+width*0.125, starting_height+height*0.125))
        else:
            starting_width = random.randrange(width*0.25, width*0.75)
            starting_height = random.randrange(height*0.25, height*0.75)
            image = image.crop((starting_width, starting_height, starting_width+width*0.125, starting_height+height*0.125))

        image.save('output/quiz.png')

    def generate_question(self):
        if self.source == "image":
            question = "Изображение:"
        elif self.source == "flavorText":
            question = "Флавор:\n"
            question += self.obfuscate_text(self.correct_answer["flavorText"])
        else:
            question = "Описание:\n"
            question += self.obfuscate_text(self.correct_answer["descriptionRaw"])
        question += "\n+%s/-%s" % (self.increase, self.decrease)
        question += "\n Варианты ответа:"

        for i in range(len(self.options)):
            if self.options[i]["supertype"] == "Чемпион" and self.options[i]["type"] == "Боец":
                if len(self.options[i]["cardCode"]) > 7:
                    name = self.options[i]["name"] + " 2"
                else:
                    name = self.options[i]["name"]
            else:
                name = self.options[i]["name"]

            question += "\n %s. %s" % (i+1, name)
        return question

    def obfuscate_text(self, text):
        randomize = random.random()
        chance_value = 0.25
        if randomize < 0.34:
            self.increase = 2
            self.decrease = 1
            chance_value = 0.3

        elif randomize < 0.90:
            self.increase = 1
            self.decrease = 0

            chance_value = 0.25
        elif randomize < 0.98:
            self.increase = 5
            self.decrease = 4

            chance_value = 0.5
        else:
            self.increase = 20
            self.decrease = 19

            text = text[::-1]
            chance_value = 0

        text = text.split()
        new_text = ""
        for each in text:
            if random.random() < chance_value and each != "–":
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
