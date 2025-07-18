import tkinter as tk
from tkinter import filedialog
from convert import ConvertImage

def OFD() -> str:
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(filetypes = (("Images",("*.png","*.bmp","*.jpg","*.jpeg")),
                                                   ("PNG","*.png"),("BMP","*.bmp"),
                                                   ("JPG","*.jpg"),("JPEG","*.jpeg")))

if __name__ == "__main__":
    file = OFD()
    ConvertImage(Path2Img=file)
