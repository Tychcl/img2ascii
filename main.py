from tkinter import filedialog
from functions.ascii import convert, img_char_set
from PIL import Image, ImageOps
import numpy as np

def OFD() -> str:
    return filedialog.askopenfilename(
        filetypes = (("Images",("*.png","*.bmp","*.jpg","*.jpeg")),
                    ("PNG","*.png"),("BMP","*.bmp"),
                    ("JPG","*.jpg"),("JPEG","*.jpeg")))

if __name__ == "__main__":
    file = OFD()
    print(convert(path=file, color=True, fix_color=True))
