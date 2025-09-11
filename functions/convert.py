from PIL import Image, ImageOps
from functions.filter import mega_sobel
import os

global FileInfo,CharSet
FileInfo: dict
CharSet: str = " .:coP0?@■"

RatioX = 14/7
RatioY = 7/14

CharSize = {"x" : 8, "y" : 8} #хранит размер символа по х и у

def resize_image(image: Image, size: tuple) -> Image:
    x,y = size
    return image.resize(size, Image.LANCZOS), image.resize((round(x * RatioX), y), Image.LANCZOS)
    
def mono_image(resized_image: Image) -> Image:
    return resized_image.convert("L")

def ascii_text(gray_scale_image: Image) -> list[str]:
    list = []
    dv = 255 / (len(CharSet)-1)
    for y in range(gray_scale_image.height):
        str = ""
        for x in range(gray_scale_image.width):
            str += CharSet[round(gray_scale_image.getpixel((x, y)) / dv)]
        list.append(str)
    return list #[line.strip() for line in ascii_str.split('\n') if line.strip()]

def ascii_image(gray_scale_image: Image):
    list = []
    dv = 255 / (len(CharSet)-1)
    for y in range(gray_scale_image.height):
        str = []
        for x in range(gray_scale_image.width):
            str.append(round(gray_scale_image.getpixel((x, y)) / dv))
        list.append(str)
    return list

def ascii2image_monochrome(ascii_gray_scale_list, color_invert: bool = False) -> Image:
    width = max(len(line) for line in ascii_gray_scale_list)
    height = len(ascii_gray_scale_list)
    chars_img = Image.open('resources/chars/fillASCII.png').convert("L")
    chars = []
    rng = range(len(CharSet))
    for i in reversed(rng) if color_invert else rng:
        left = i * CharSize["x"]
        right = left + CharSize["x"]
        # Обрезаем изображение для получения отдельного символа
        char = chars_img.crop((left, 0, right, CharSize["y"]))
        chars.append(char)
    image = Image.new("L", (width * CharSize["x"], height * CharSize["y"]), color="black")
    for y in range(height):
        paste_y = y * CharSize["y"]
        for x in range(width):
            paste_x = x * CharSize["x"]
            image.paste(chars[ascii_gray_scale_list[y][x]], (paste_x, paste_y))
    return image

def convert_image(path2image: str,
                  color_invert: bool = False, char_set_invert: bool = False,
                  size: tuple = None) -> Image:
    global FileInfo, CharSet
    if not os.path.exists(path2image):
        return None

    file: list[str] = path2image.split("/")[-1].split(".")
    FileInfo = {"Name" : file[0], "Format" : file[1]}
    CharSet = CharSet[::1 if char_set_invert else -1]

    image: Image = Image.open(path2image)
    if size is None:
        size = (round(image.width / CharSize["x"]), round(image.height / CharSize["y"]))

    resized_img, resized_txt= resize_image(image, size)

    gray_scale_img: Image = mono_image(resized_img)
    gray_scale_txt: Image = mono_image(resized_txt)

    ascii_img = ascii_image(gray_scale_img)
    final_img: Image = ascii2image_monochrome(ascii_img, color_invert)

    ascii_txt: list[str] = ascii_text(gray_scale_txt)
    
    os.makedirs(f"result/{FileInfo["Name"]}", exist_ok=True)

    txt = f"result/{FileInfo["Name"]}/{FileInfo["Name"]}.txt"
    with open(txt, "w", encoding="utf-8") as f:
        f.write("\n".join(ascii_txt))
    
    img = f"result/{FileInfo["Name"]}/{FileInfo["Name"]}.{FileInfo["Format"]}"
    final_img.save(img)
    final_img.show()

    print(f"txt: {os.path.abspath(txt)}")
    print(f"img: {os.path.abspath(img)}")