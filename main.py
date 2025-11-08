from tkinter import filedialog
from functions.ascii import convert
import time

def OFD() -> str:
    return filedialog.askopenfilename(
        filetypes = (("Images",("*.png","*.bmp","*.jpg","*.jpeg")),
                    ("PNG","*.png"),("BMP","*.bmp"),
                    ("JPG","*.jpg"),("JPEG","*.jpeg")))

if __name__ == "__main__":
    file = OFD()
    start = time.time()
    print(convert(path=file, color_invert=True, color=True, fix_color=True))
    end = time.time()
    print(end - start)
