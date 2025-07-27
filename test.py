from PIL import Image, ImageDraw, ImageFont
import os

global FileInfo,CharSet
FileInfo: dict
CharSet: str = " .:coP0?@■"

RatioX = 14/7
RatioY = 7/14

CharSize = {"x" : 8, "y" : 8} #хранит размер символа по х и у
FontRatioX = {"cour.ttf":1 , "consolas.ttf":0.80108695652}

def resize_image(original_image: Image, size: tuple) -> Image:
    if size is None:
        return original_image.resize((round(original_image.width / CharSize["x"] * RatioX), round(original_image.height / CharSize["y"])), Image.LANCZOS)
    else:
        return original_image.resize(size, Image.LANCZOS)
    
def mono_image(resized_image: Image) -> Image:
    return resized_image.convert("L")

def ascii_image(gray_scale_image: Image) -> str:
    ascii_str = ""
    dv = 255 / (len(CharSet)-1)
    for y in range(gray_scale_image.height):
        for x in range(gray_scale_image.width):
            ascii_str += CharSet[round(gray_scale_image.getpixel((x, y)) / dv)]
        ascii_str += "\n"
    return ascii_str

def ascii2image_monochrome(ascii_str: str, background: tuple, foreground: tuple) -> str | None:
    lines = [line.rstrip() for line in ascii_str.split('\n') if line.strip()]
    if not lines:
        return None
    ascii_str = "\n".join(lines)
    width = max(len(line) for line in lines)
    height = len(lines)
    RX = width / height
    font = "cour.ttf"
    img = Image.new("RGB", (round(width * 5 * FontRatioX[font]), round(height * CharSize["y"] * RX)), background)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(f"resources/fonts/{font}", CharSize["x"])
    draw.multiline_text((0,0), ascii_str, font=font, fill=foreground)
    save = f"result/{FileInfo["Name"]}/{FileInfo["Name"]}.{FileInfo["Format"]}"
    img.save(save)
    return save

def convert_image(path2image: str, color_invert: bool = False, char_set_invert: bool = False, resize: bool = True, size: tuple = None):
    global FileInfo, CharSet
    if not os.path.exists(path2image):
        return None

    file: list = path2image.split("/")[-1].split(".")
    FileInfo = {"Name" : file[0], "Format" : file[1]}
    CharSet = CharSet[::-1 if not char_set_invert else 1]
    if color_invert:
        background: tuple = (255, 255, 255)
        foreground: tuple = (0, 0, 0)
    else:
        background: tuple = (0, 0, 0)
        foreground: tuple = (255, 255, 255)

    original_image: Image = Image.open(path2image)
    resized_image: Image = resize_image(original_image, size) if resize else original_image
    gray_scale_image: Image = mono_image(resized_image)

    ascii_str: str = ascii_image(gray_scale_image)

    os.makedirs(f"result/{FileInfo["Name"]}", exist_ok=True)
    txt = f"result/{FileInfo["Name"]}/{FileInfo["Name"]}.txt"
    with open(txt, "w", encoding="utf-8") as f:
        f.write(ascii_str)
    print(f"txt: {os.path.abspath(txt)}")
    print(f"img: {ascii2image_monochrome(ascii_str, background, foreground)}")