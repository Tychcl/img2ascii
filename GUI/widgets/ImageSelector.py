import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os

class ImageSelector(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text="Путь к файлу..."
        )
        self.entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        self.browse_btn = ctk.CTkButton(
            self,
            text="Обзор",
            width=60,
            command=self.browse_file
        )
        self.browse_btn.pack(side="left", padx=5, pady=5)
        
        self.load_btn = ctk.CTkButton(
            self,
            text="Открыть",
            width=60,
            command=self.load_image
        )
        self.load_btn.pack(side="left", padx=5, pady=5)
        
        self.entry.bind("<Return>", lambda e: self.load_image())
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите картинку",
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.bmp"),
            ]
        )
        
        if file_path:
            self.entry.delete(0, "end")
            self.entry.insert(0, file_path)
            self.load_image()
    
    def load_image(self):
        path = self.entry.get().strip()
        
        if not path:
            return
        
        if hasattr(self.master, 'image_area'):
            image_area = self.master.image_area
        else:
            for widget in self.master.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and widget != self:
                    image_area = widget
                    break
            else:
                return
        
        try:
            if not os.path.exists(path):
                image_area.configure(
                    image=None,
                    text="Нет такого файла",
                    text_color="red"
                )
                return
            
            img = Image.open(path)
            img.thumbnail((500, 400))
            
            ctk_img = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=img.size
            )
            
            image_area.configure(image=ctk_img, text="")
            
        except Exception:
            image_area.configure(
                image=None,
                text="Ошибка загрузки",
                text_color="red"
            )