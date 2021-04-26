from PIL import Image
import json
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

cost_font = ImageFont.truetype("../fonts/Roboto-Black.ttf", 34)

jdata = json.loads(open("../cards_data/card_data.json",  encoding='utf-8').read())
result = []
i=1
for dict in jdata:
    if True:

        result.append({"supertype" : dict["supertype"], "type" : dict["type"], "name" : dict["name"], "cost" : dict["cost"], "cardCode" :  dict["cardCode"], "regionRef" :  dict["regionRef"]})
        background = Image.new('RGBA', (600, 110), (255, 255, 255, 0))

        img = Image.open("../ru_ru/img/cards/" + dict["cardCode"] + ".png")
        w, h = img.size
        img = img.crop((75, 200, w-75, h - 650))

        if dict["type"] == "Место силы":
            type = "Landmark"
        elif dict["rarityRef"] == "Champion":
            type = "Champion"
        elif dict["type"] == "Заклинание":
            type = "Spell"
        else:
            type = "Ally"
        gradient = Image.open("../gradients/big/"+ type + "/" + dict["regionRef"] +".png")

        if type == "Ally" or type == "Champion":
            image_offset_top = 2
            image_crop_size_y = 68
            cost_left_offset = (22, 17)
            cost_top_offset = 15
            text_x, text_y = 70, 20
            size_x = 510
            size_y = 72
        elif type == "Landmark":
            image_offset_top = 1
            image_crop_size_y = 68
            cost_left_offset = (20, 16)
            cost_top_offset = 12
            text_x, text_y = 75, 20
            size_x = 510
            size_y = 70
        else:
            image_offset_top = 1
            image_crop_size_y = 67
            cost_left_offset = (28, 20)
            cost_top_offset = 20
            text_x, text_y = 75, 20
            size_x = 510
            size_y = 70

        img = img.resize((size_x-100, image_crop_size_y))
        background.paste(img, (78, image_offset_top))
        gradient = gradient.resize((size_x, size_y))

        # img = img.convert("RGBA")
        background.paste(gradient, (0, 0),  mask=gradient)
        # background.paste(Image.new('RGBA', (35, 56), (66, 114, 245, 255)), (7, 7))

        draw = ImageDraw.Draw(background)
        if (dict["cost"] >= 10):
            draw.text((cost_left_offset[1], cost_top_offset), str(dict["cost"]), font=cost_font, fill='rgb(255, 255, 255)')
        else:
            draw.text((cost_left_offset[0], cost_top_offset), str(dict["cost"]), font=cost_font, fill='rgb(255, 255, 255)')

        x, y = text_x, text_y
        text = dict["name"]
        if len(text) > 25:
            name_font = ImageFont.truetype("../fonts/YanoneKaffeesatz-Medium.ttf", 33)
        else:
            name_font = ImageFont.truetype("../fonts/YanoneKaffeesatz-Medium.ttf", 38)

        draw.text((x, y-2), text, (0,0,0), font=name_font)
        draw.text((x, y+2), text,(0,0,0),font=name_font)
        draw.text((x-2, y), text, (0,0,0), font=name_font)
        draw.text((x+2, y), text, (0,0,0),font=name_font)
        draw.text((x, y), text, font=name_font, fill='rgb(255, 255, 255)')

        # background = background.crop((0, 0, 600, 70))
        background.save("../processed/" + dict["cardCode"] + ".png")

        print("%s %s" % (i, dict["cardCode"]))
        i+=1

#
# with open("cards.json", "w", encoding='utf-8') as fp:
#     json.dump(result, fp, ensure_ascii=False)
