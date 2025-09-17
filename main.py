from tkinter import filedialog
from functions.convert import convert_image
from functions.new import convert
import os


def OFD() -> str:
    return filedialog.askopenfilename(
        filetypes = (("Images",("*.png","*.bmp","*.jpg","*.jpeg")),
                    ("PNG","*.png"),("BMP","*.bmp"),
                    ("JPG","*.jpg"),("JPEG","*.jpeg")))

if __name__ == "__main__":
    file = OFD()
    print(os.path.splitext(file))
    #print(convert(path=file))
