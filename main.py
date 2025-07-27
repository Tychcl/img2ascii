from tkinter import filedialog
from test import convert_image

def OFD() -> str:
    return filedialog.askopenfilename(
        filetypes = (("Images",("*.png","*.bmp","*.jpg","*.jpeg")),
                    ("PNG","*.png"),("BMP","*.bmp"),
                    ("JPG","*.jpg"),("JPEG","*.jpeg")))

if __name__ == "__main__":
    file = OFD()
    convert_image(path2image=file)
