from enum import Enum


class Command(Enum):
    default_list = ["главная"]
    code_list = ["код:", "код" ,"code", "code:"]
    card_list = ["карта", "карта:", "card", "card:"]
    guesser_list = ["guess", "загадай"]
    make_a_guess_list = ["answer", "ответ"]
    show_leaderboard_list = ["guessers", "отгадчики"]
    ban_list = ["баны"]
    back_list = ["назад"]
    info_list = ["инфо"]
    hypergeom_list = ["гипергеометрический"]
