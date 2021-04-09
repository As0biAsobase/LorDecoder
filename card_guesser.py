import random
import re

class Guesser:

    def __init__(self, chat):
        self.chat = chat
        self.correct_answer = None
        self.options = []
        self.question = ""
        pass

    def generate_quiz(self, connection):
        card_list = connection.getAllCards()
        self.options = random.sample(card_list, 4)
        self.correct_answer = random.choice(self.options)

        self.question = self.generate_question()


    def generate_question(self):
        question  = self.correct_answer["flavorText"]
        question += "\n Варианты ответа:"

        for i in range(len(self.options)):
            question += "\n %s. %s" % (i+1, self.options[i]["name"])
        return question

    def make_a_guess(self. guess):
        if len(guess) == 1:
            position = int(guess) - 1
            if self.options[position] == self.correct_answer:
                return True
            else:
                return False
        else:
            return False
