from enum import Enum


class Command(Enum):
    default_list = ["главная"]
    code_list = ["код:", "код" ,"code", "code:"]
    card_list = ["карта", "карта:", "card", "card:"]
    ban_list = ["баны"]
    back_list = ["назад"]
    info_list = ["инфо"]
    calculator_list = ["калькулятор"]
    hypergeom_list = ["гипергеометрический"]
