import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os

class ImageSelector(ctk.CTkFrame):
    """Виджет для выбора изображения"""
    
    def __init__(self, master=None, on_image_selected=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_image_selected = on_image_selected
        self.current_image = None
        
        self.create_widgets()
        
    def create_widgets(self):
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
        """Выбрать файл через диалог"""
        file_path = filedialog.askopenfilename(
            title="Выберите картинку",
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif *.webp"),
            ]
        )
        
        if file_path:
            self.entry.delete(0, "end")
            self.entry.insert(0, file_path)
            self.load_image()
    
    def load_image(self):
        """Загрузить картинку"""
        path = self.entry.get().strip()
        
        if not path:
            return
        
        try:
            if not os.path.exists(path):
                return
            
            img = Image.open(path)
            self.current_image = img
            
            if self.on_image_selected:
                self.on_image_selected(img)
            
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
    
    def get_image(self):
        """Получить текущее изображение"""
        return self.current_image