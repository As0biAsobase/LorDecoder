import json

def find_card(source, args, connection):
    costs = ["0", "1", "2", "3", "4", "5", "6",
                "7", "8", "9", "10", "11", "12"]

    name = ""
    cost = None
    attack = None
    health = None

    type = "1"
    for each in args:
        type_counter = 0
        if each.lower()[0] == "ы":
            for c in each:
                if c.lower()[0] == "ы":
                    type_counter += 1
                else:
                    break
        elif each not in costs and not ("/" in each) and each != "пнг":
            name += each + " "
        elif each in costs and not ("/" in each):
            cost = int(each)
        elif "/" in each:
            stats = each.split("/")

            if each.endswith("/"):
                attack = int(stats[0])
            elif each.endswith("/"):
                health = int(stats[0])
            else:
                attack = int(stats[0])
                health = int(stats[1])

    print(name)
    print(type_counter)
    print(cost)
    print(attack)
    print(health)


    name = name.strip()
    name = name.lower()

    result = ""

    found = False

    result = connection.getCodeByName(name)

    if type_counter > 0:
        result += "T%s" % (type_counter)

    return result