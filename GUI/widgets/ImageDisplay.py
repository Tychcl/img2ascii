import customtkinter as ctk
from PIL import Image

class ImageDisplay(ctk.CTkFrame):
    """Виджет для отображения изображения"""
    
    def __init__(self, master=None, title="Изображение", **kwargs):
        super().__init__(master, **kwargs)
        
        self.title = title
        self.current_image = None
        
        self.create_widgets()
    
    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text=self.title, font=("Arial", 12))
        self.title_label.pack(pady=(5, 0))
        
        self.image_label = ctk.CTkLabel(self, text="", width=150, height=150)
        self.image_label.pack(pady=5, padx=5, fill="both", expand=True)
    
    def set_image(self, image):
        """Установить изображение для отображения"""
        if image:
            img_copy = image.copy()
            img_copy.thumbnail((140, 140))
            
            ctk_img = ctk.CTkImage(
                light_image=img_copy,
                dark_image=img_copy,
                size=img_copy.size
            )
            
            self.image_label.configure(image=ctk_img, text="")
            self.current_image = image
        else:
            self.image_label.configure(image=None, text="Нет изображения")