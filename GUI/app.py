import customtkinter
from widgets.Widgets import OFD

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_default_color_theme("dark-blue")

        self.title("Ascii / Tychcl")
        self.geometry("400x400")
        self.iconbitmap("resources/icons/64.ico")
        self.grid_columnconfigure((0, 0), weight=1)

        self.OFD = OFD(master=self)
        self.OFD.grid(row=0, column=0, sticky="ew")
        
    def button_callback(self):
        print("button pressed")

app = App()
app.mainloop()