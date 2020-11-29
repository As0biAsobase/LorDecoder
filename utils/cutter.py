from PIL import Image
import json
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

cost_font = ImageFont.truetype("../fonts/Roboto-Black.ttf", 28)
name_font = ImageFont.truetype("../fonts/YanoneKaffeesatz-Medium.ttf", 38)

jdata = json.loads(open("../cards_data/card_data.json",  encoding='utf-8').read())
result = []
i=1
for dict in jdata:
    if True:

        result.append({"supertype" : dict["supertype"], "type" : dict["type"], "name" : dict["name"], "cost" : dict["cost"], "cardCode" :  dict["cardCode"], "regionRef" :  dict["regionRef"]})

        background = Image.new('RGBA', (600, 110), (255, 255, 255, 0))

        img = Image.open("../ru_ru/img/cards/" + dict["cardCode"] + ".png")
        w, h = img.size
        img = img.crop((100, 175, w-150, h - 675))
        img = img.resize((350, 70))

        background.paste(img, (250,0))

        gradient = Image.open("../gradients/big/"+ dict["regionRef"] +".png")
        gradient = gradient.resize((600, 70))

        # img = img.convert("RGBA")
        background.paste(gradient, (0, 0),  mask=gradient)
        background.paste(Image.new('RGBA', (35, 56), (66, 114, 245, 255)), (7, 7))

        draw = ImageDraw.Draw(background)
        if (dict["cost"] >= 10):
            draw.text((8, 20), str(dict["cost"]), font=cost_font, fill='rgb(255, 255, 255)')
        else:
            draw.text((16, 20), str(dict["cost"]), font=cost_font, fill='rgb(255, 255, 255)')
        x, y = 50, 25
        text = dict["name"]
        draw.text((x, y-2), text, (0,0,0), font=name_font)
        draw.text((x, y+2), text,(0,0,0),font=name_font)
        draw.text((x-2, y), text, (0,0,0), font=name_font)
        draw.text((x+2, y), text, (0,0,0),font=name_font)
        draw.text((x, y), text, font=name_font, fill='rgb(255, 255, 255)')

        background = background.crop((0, 0, 600, 70))
        background.save("../processed/" + dict["cardCode"] + ".png")

        print(str(i) + " " + dict["cardCode"])
        i+=1

#
# with open("cards.json", "w", encoding='utf-8') as fp:
#     json.dump(result, fp, ensure_ascii=False)
