from PIL import Image, ImageOps
import numpy as np
import os

char_size: tuple = {"x": 8, "y": 8}
char_ratio: tuple = {"x":14/7, "y":7/14}

file_info: dict = {"path": None, "name": None, "extension": None}
txt_char_set: str = "■@?0Poc:. "
divine: float = 255 / (len(txt_char_set)-1)
img_char_set_path = "resources/chars/fillASCII.png"

#class ascii:
#    def __init__(self, image_path: str):
#        self.image = 

def image_resize(image: Image, size: tuple) -> Image:
    """Resize img.
    Args:
        image (Image): image you need to resize
        size (tuple): size you need (x,y)"""
    return image.resize(size, Image.LANCZOS)

def image_luminance(image: Image) -> np.ndarray:
    """Get luminance list.
    Args:
        image (Image): brightness map from image
    Returns:
        np.ndarray: brightness map"""
    img_array = np.array(image.convert("L"))
    result = np.round(img_array / divine).astype(int)
    return result

def img_ascii(map: np.ndarray, color_invert: bool) -> Image:
    """Get ascii img art from brightness map.
    Args:
        map (np.ndarray): brightness map 
        color_invert (bool): Inverts order of char list for img ascii. White color of img will turn black on final img if True
    Returns:
        Image: ascii art"""
    img_char_set: list[np.ndarray] = np.hsplit(np.array(Image.open(img_char_set_path).convert("L")), len(txt_char_set))
    char_set: list[np.ndarray] = img_char_set[::-1] if color_invert else img_char_set
    y_size , x_size = map.shape
    final_image = np.zeros((y_size * char_size["y"], x_size * char_size["x"]), dtype=np.uint8)
    for y in range(y_size):
        y_paste = y * char_size["y"]
        for x in range(x_size):
            x_paste = x * char_size["x"]
            final_image[y_paste:y_paste+char_size["y"], x_paste:x_paste+char_size["x"]] = char_set[map[y][x]]
    return final_image

def img_color_ascii(map: np.ndarray, color_invert: bool, fix_color:bool, image: Image) -> Image:
    """Get ascii img art from brightness map.
    Args:
        list (list[list[int]]): brightness map 
        color_invert (bool): Inverts order of char list for img ascii. White color of img will turn black on final img if True
        image (Image): resized image for colors
    Returns:
        Image: ascii art"""
    load = np.array(image)
    if(fix_color and color_invert):
        load[(map == 0) | (map == 1)] = (255,255,255)

    img_char_set: list[np.ndarray] = np.hsplit(np.array(Image.open(img_char_set_path).convert("L")), len(txt_char_set))
    char_set: list[np.ndarray] = img_char_set[::-1] if color_invert else img_char_set
    char_set = [np.repeat(char_array[:, :, np.newaxis], 3, axis=2) for char_array in char_set]
    char_set = char_set / np.max(char_set)
    y_size , x_size = map.shape
    
    final_image = np.zeros((y_size * char_size["y"], x_size * char_size["x"], 3), dtype=np.uint8)
    for y in range(y_size):
        y_paste = y * char_size["y"]
        for x in range(x_size):
            x_paste = x * char_size["x"]
            char = char_set[map[y][x]] * load[y][x]
            final_image[y_paste:y_paste+char_size["y"], x_paste:x_paste+char_size["x"]] = char
    return final_image

def convert(path:str, 
            color_invert: bool = False, 
            color: bool = False, fix_color: bool = False) -> tuple[str] | None:
    """Convert img to ascii.
    Convert img to ascii art as img or as txt file. Saves into Result/{img file name}/img or txt file
    Args:
        path (str): Path to img file
        color_invert (bool): Inverts order of char list for img ascii. White color of img will turn black on final img if True
        chars_invert (bool): Inverts order of char list for txt ascii. White color of img will turn '■' if True    
    Returns:
        tuple[str]: Paths to saved img, if not saved path is None"""
    #Обработка, чтобы просто так не выполнять действия, если ничего не надо
    if not os.path.exists(path):
        return None

    global file_info

    file_info["path"] = path
    file_info["name"], file_info["extension"] = os.path.splitext(os.path.basename(path))

    original_image: Image = Image.open(path)

    x_size, y_size = original_image.size
    x_size = round(x_size / char_size["x"])
    y_size = round(y_size / char_size["y"])

    os.makedirs(f"result/{file_info["name"]}", exist_ok=True)

    image: Image = image_resize(original_image, (x_size, y_size))
    luminance: np.ndarray = image_luminance(image)
    if(color):
        final_image: np.ndarray = img_color_ascii(luminance, color_invert, fix_color, image)
    else:
        final_image: np.ndarray = img_ascii(luminance, color_invert)
    save: str = f"result/{file_info["name"]}/{file_info["name"]}{file_info["extension"]}"
    Image.fromarray(final_image).save(save)
    final_img_path = os.path.abspath(save)
    return final_img_path