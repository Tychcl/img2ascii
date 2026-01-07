import customtkinter as ctk
from widgets.ImageSelector import ImageSelector

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_default_color_theme("dark-blue")

        self.title("Ascii / Tychcl")
        self.geometry("400x400")
        self.iconbitmap("resources/icons/64.ico")
        
        self.setup_ui()
        
    def setup_ui(self):
        self.image_widget = ImageSelector(self)
        self.image_widget.pack(pady=10, padx=10, fill="x")
        
        self.image_area = ctk.CTkLabel(self, text="")
        self.image_area.pack(pady=10, padx=10, fill="both", expand=True)
        
    def button_callback(self):
        print("button pressed")

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()