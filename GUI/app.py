import customtkinter
from customtkinter import filedialog
from frames.scroll import ScrollFrame

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_default_color_theme("dark-blue")

        self.title("Ascii / Tychcl")
        self.geometry("400x400")
        self.iconbitmap("resources/icons/64.ico")
        self.grid_columnconfigure((0, 1), weight=1)

        self.ImagePathButton = customtkinter.CTkButton(self, text="CTkButton", command=self.OpenFileDialog)
        self.ImagePathButton.grid(row=0, column=0, padx=(3, 0), pady=3)

    def OpenFileDialog(self):
        self.ImagePath = filedialog.askopenfilename(
        filetypes = (("Images",("*.png","*.bmp","*.jpg","*.jpeg")),
                    ("PNG","*.png"),("BMP","*.bmp"),
                    ("JPG","*.jpg"),("JPEG","*.jpeg")))
        
    def button_callback(self):
        print("button pressed")

app = App()
app.mainloop()