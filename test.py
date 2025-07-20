from PIL import Image
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
file = filedialog.askopenfilename(filetypes = (("Images",("*.png","*.bmp","*.jpg","*.jpeg")),
                                                   ("PNG","*.png"),("BMP","*.bmp"),
                                                   ("JPG","*.jpg"),("JPEG","*.jpeg")))

img = Image.open(file)
print(img.width, img.height)
resized = img.resize((round(img.width/8), round(img.height/8)))
resized.save("r.jpg")

img/  
├── src/  
│   ├── utils/  
│   │   ├── file_utils.py  
│   │   └── math_utils.py  
│   └── core/  
│       ├── api.py  
│       └── db.py  
├── tests/  
└── README.md  