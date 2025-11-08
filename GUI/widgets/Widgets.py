import customtkinter
from customtkinter import filedialog

class OFD(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.grid_columnconfigure((0, 0), weight=1)
        self.PathLabel = customtkinter.CTkLabel(self, text="your path", font=("Arial", 10))
        self.PathLabel.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.ImagePathButton = customtkinter.CTkButton(self, text="Image", 
            command=self.OpenFileDialog, width=50, height=25, 
            corner_radius=10)
        self.ImagePathButton.grid(row=0, column=1, sticky="w", padx=5, pady=5)
    
    def OpenFileDialog(self):
        path = filedialog.askopenfilename(
        filetypes = (("Images",("*.png","*.bmp","*.jpg","*.jpeg")),
                    ("PNG","*.png"),("BMP","*.bmp"),
                    ("JPG","*.jpg"),("JPEG","*.jpeg")))
        self.master.ImagePath = path
        self.PathLabel.configure(text=path)

        