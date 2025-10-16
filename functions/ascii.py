from PIL import Image, ImageOps
import numpy as np
import os
from functions.filter import mega_sobel
#Если вы будете изменять символы или менять из размер
#То для начала убедитесь, что вы изменили картинку в ресурсах

char_size: tuple = {"x": 8, "y": 8} #размер символа на картинке (x,y)
char_ratio: tuple = {"x":14/7, "y":7/14} #соотношение сторон (x,y)

file_info: dict = {"path": None, "name": None, "extension": None}
#строка изначально перевернута из за того, что так результат выглядит лучше " .:coP0?@■"
txt_char_set: str = "■@?0Poc:. "
#делитель для получения символа по яркости
divine: float = 255 / (len(txt_char_set)-1)
img_char_set: list[Image] = []
chars_img = Image.open("resources/chars/fillASCII.png")
for i in range(len(txt_char_set)):
    left = i * char_size["x"]
    right = left + char_size["x"]
    img_char = chars_img.crop((left, 0, right, char_size["y"]))
    img_char_set.append(img_char.convert("L"))

def image_resize(image: Image, size: tuple) -> Image:
    """Resize img.
    Args:
        image (Image): image you need to resize
        size (tuple): size you need (x,y)"""
    return image.resize(size, Image.LANCZOS)

def image_luminance(image: Image) -> list[list[int]]:
    """Get luminance list.
    Args:
        image (Image): brightness map from image
    Returns:
        list[list[int]]: brightness map"""
    img_array = np.array(image.convert("L"))
    result = np.round(img_array / divine).astype(int)
    return result.tolist()

def img_ascii(map: list[list[int]], color_invert: bool) -> Image:
    """Get ascii img art from brightness map.
    Args:
        list (list[list[int]]): brightness map 
        color_invert (bool): Inverts order of char list for img ascii. White color of img will turn black on final img if True
    Returns:
        Image: ascii art"""
    char_set: list[Image] = img_char_set[::-1] if color_invert else img_char_set
    y_size = len(map)
    x_size = len(map[0])
    final_image = Image.new("L", (x_size * char_size["x"], y_size * char_size["y"]), color="black")
    for y in range(y_size):
        y_paste = y * char_size["y"]
        for x in range(x_size):
            x_paste = x * char_size["x"]
            final_image.paste(char_set[map[y][x]], (x_paste, y_paste))
    return final_image

def img_color_ascii(map: list[list[int]], color_invert: bool, fix_color:bool, image: Image) -> Image:
    """Get ascii img art from brightness map.
    Args:
        list (list[list[int]]): brightness map 
        color_invert (bool): Inverts order of char list for img ascii. White color of img will turn black on final img if True
        image (Image): resized image for colors
    Returns:
        Image: ascii art"""
    load = image.load()
    char_set: list[Image] = img_char_set[::-1] if color_invert else img_char_set
    y_size = len(map)
    x_size = len(map[0])
    final_image = Image.new("RGB", (x_size * char_size["x"], y_size * char_size["y"]), color="black")
    for y in range(y_size):
        y_paste = y * char_size["y"]
        for x in range(x_size):
            x_paste = x * char_size["x"]
            if(fix_color and color_invert and map[y][x] in [1,0]):
                color = (255,255,255)
            else:
                color = load[x,y]
            final_image.paste(ImageOps.colorize(char_set[map[y][x]], (0,0,0), color), (x_paste, y_paste))
    return final_image

def txt_ascii(map: list[list[int]], chars_invert: bool) -> Image:
    """Get ascii txt art from brightness map.
    Args:
        list (list[list[int]]): brightness map 
        chars_invert (bool): Inverts order of char list for txt ascii. White color of img will turn ' ' if True
    Returns:
        Image: ascii art"""
    char_set: str = txt_char_set[::-1] if chars_invert else txt_char_set
    y_size = len(map)
    x_size = len(map[0])
    final_txt: str = ""
    for y in range(y_size):
        s: str = "\n"
        for x in range(x_size):
            s += char_set[map[y][x]]
        final_txt += s
    return final_txt.strip('\n')

def convert(path:str, 
            color_invert: bool = False, chars_invert: bool = False,
            txt_need: bool = False, img_need: bool = True,
            use_y_ratio: bool = False, 
            color: bool = False, fix_color: bool = False) -> tuple[str] | None:
    """Convert img to ascii.
    Convert img to ascii art as img or as txt file. Saves into Result/{img file name}/img or txt file

    Args:
        path (str): Path to img file
        color_invert (bool): Inverts order of char list for img ascii. White color of img will turn black on final img if True
        chars_invert (bool): Inverts order of char list for txt ascii. White color of img will turn '■' if True
        txt_need (bool): Convert img to txt ascii if True
        img_need (bool): Convert img to img ascii if True
        use_y_ratio (bool): used X ratio if False, then txt is bigger, else txt is smaller
       
    Returns:
        tuple[str]: Paths to saved img or txt file, if not saved path is None"""
    #Обработка, чтобы просто так не выполнять действия, если ничего не надо
    if not txt_need and not img_need or not os.path.exists(path):
        return None

    global file_info
    final_img_path: str = None
    final_txt_path: str = None

    file_info["path"] = path
    file_info["name"], file_info["extension"] = os.path.splitext(os.path.basename(path))

    original_image: Image = Image.open(path)

    x_size, y_size = original_image.size
    x_size = round(x_size / char_size["x"])
    y_size = round(y_size / char_size["y"])

    os.makedirs(f"result/{file_info["name"]}", exist_ok=True)

    if txt_need:
        size:tuple =(x_size, round(y_size * char_ratio["y"])) if use_y_ratio else (round(x_size * char_ratio["x"]), y_size)
        image: Image = image_resize(original_image, size)
        luminance: list[list[int]] = image_luminance(image)
        final_txt: str = txt_ascii(luminance, chars_invert)
        save: str = f"result/{file_info["name"]}/{file_info["name"]}.txt"
        with open(save, "w", encoding='utf-8') as f:
            f.write(final_txt)
        final_txt_path = os.path.abspath(save)

    if img_need:
        image: Image = image_resize(original_image, (x_size, y_size))
        luminance: list[list[int]] = image_luminance(image)
        if(not color):
            final_image: Image = img_ascii(luminance, color_invert)
        else:
            final_image: Image = img_color_ascii(luminance, color_invert, fix_color, image)
        save: str = f"result/{file_info["name"]}/{file_info["name"]}{file_info["extension"]}"
        final_image.save(save)
        final_img_path = os.path.abspath(save)

    return (final_txt_path, final_img_path)