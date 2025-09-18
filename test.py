from functions.ascii import txt_char_set, divine
from PIL import Image, ImageOps

example_image = Image.new("L", (len(txt_char_set), len(txt_char_set)), color=127)

for y in range(len(txt_char_set)):
    for x in range(len(txt_char_set)):
        example_image.putpixel((x,y),round(x * divine))

ImageOps.invert(example_image).save("t.png")