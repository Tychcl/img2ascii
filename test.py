from PIL import Image, ImageDraw, ImageFont
import os

global FileInfo,CharSet
FileInfo: dict
CharSet: str = " .:coP0?@■"

RatioX = 14/7
RatioY = 7/14

CharSize = {"x" : 8, "y" : 8} #хранит размер символа по х и у

def resize_image(image: Image, size: tuple) -> Image:
    return image.resize(size, Image.LANCZOS), image.resize((round(size[0] * RatioX), size[1]), Image.LANCZOS)
    
def mono_image(resized_image: Image) -> Image:
    return resized_image.convert("L")

def ascii_image(gray_scale_image: Image) -> list[str]:
    ascii_list = []
    dv = 255 / (len(CharSet)-1)
    for y in range(gray_scale_image.height):
        ascii_str = ""
        for x in range(gray_scale_image.width):
            ascii_str += CharSet[round(gray_scale_image.getpixel((x, y)) / dv)]
        ascii_list.append(ascii_str)
    return ascii_list #[line.strip() for line in ascii_str.split('\n') if line.strip()]

def ascii2image_monochrome(ascii_list: list[str], color_invert: bool) -> str | None:
    width = max(len(line) for line in ascii_list)
    height = len(ascii_list)
    print( width, height)

def convert_image(path2image: str,
                  color_invert: bool = False, char_set_invert: bool = False,
                  size: tuple = None) -> Image:
    global FileInfo, CharSet
    if not os.path.exists(path2image):
        return None

    file: list = path2image.split("/")[-1].split(".")
    FileInfo = {"Name" : file[0], "Format" : file[1]}
    CharSet = CharSet[::-1 if not char_set_invert else 1]

    image: Image = Image.open(path2image)
    if size is None:
        size = (round(image.width / CharSize["x"]), round(image.height / CharSize["y"]))

    resized_img, resized_txt = resize_image(image, size)
    gray_scale_img: Image = mono_image(resized_img)
    gray_scale_txt: Image = mono_image(resized_txt)
    ascii_img: list[str] = ascii_image(gray_scale_img)
    ascii_txt: list[str] = ascii_image(gray_scale_txt)

    os.makedirs(f"result/{FileInfo["Name"]}", exist_ok=True)
    txt = f"result/{FileInfo["Name"]}/{FileInfo["Name"]}.txt"
    with open(txt, "w", encoding="utf-8") as f:
        f.write("\n".join(ascii_txt))
    print(f"txt: {os.path.abspath(txt)}")
    print(f"img: {ascii2image_monochrome(ascii_img, color_invert)}")f