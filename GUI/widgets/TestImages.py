import customtkinter as ctk
from PIL import Image, ImageDraw
import sys
import os


class TestImagesWindow(ctk.CTkToplevel):
    """Окно с тестовыми изображениями"""
    
    def __init__(self, master=None, on_settings_change=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title("Ascii TEST / Tychcl")
        
        try:
            self.iconbitmap("resources/icons/64.ico")
        except:
            pass
        
        self.geometry("400x450")
        self.resizable(False, True)
        
        self.create_widgets()
        self.generate_test_images()
        
        # При закрытии окна
        self.protocol("WM_DELETE_WINDOW", self.hide_window)
    
    def create_widgets(self):
        # Заголовок
        ctk.CTkLabel(
            self, 
            text="Тестовые изображения (10x10 пикселей)", 
            font=("Arial", 12)
        ).pack(pady=10)
        
        # Фрейм для изображений
        self.images_frame = ctk.CTkFrame(self)
        self.images_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Создаем 3 пары (оригинал + результат)
        self.test_displays = []
        for i in range(4):
            frame = ctk.CTkFrame(self.images_frame)
            frame.pack(pady=5, fill="x")
            
            # Оригинал
            orig_frame = ctk.CTkFrame(frame)
            orig_frame.pack(side="left", padx=10, fill="both", expand=True)
            
            ctk.CTkLabel(orig_frame, text=f"Тест {i+1}").pack()
            display = ctk.CTkLabel(orig_frame, text="", width=60, height=60)
            display.pack(pady=5)
            
            # Результат
            result_frame = ctk.CTkFrame(frame)
            result_frame.pack(side="left", padx=10, fill="both", expand=True)
            
            ctk.CTkLabel(result_frame, text="Результат").pack()
            result_display = ctk.CTkLabel(result_frame, text="", width=60, height=60)
            result_display.pack(pady=5)
            
            self.test_displays.append((display, result_display))
    
    def generate_test_images(self):
        self.test_images = [Image.open("resources\examples\gradient.png"), 
                            Image.open("resources\examples\matrix.png"), 
                            Image.open("resources\examples\color.png"),
                            Image.open("resources\examples\circ.jpg")]
        self.update_displays()
    
    def update_displays(self):
        """Обновить отображение тестовых изображений"""
        for i, (orig_display, result_display) in enumerate(self.test_displays):
            if i < len(self.test_images):
                img = self.test_images[i]
                # Увеличиваем для отображения
                img_display = img.resize((60, 60), Image.NEAREST)
                
                # Отображаем оригинал
                ctk_img = ctk.CTkImage(
                    light_image=img_display,
                    dark_image=img_display,
                    size=img_display.size
                )
                orig_display.configure(image=ctk_img, text="")
                
                # Показываем заглушку для результата
                result_display.configure(
                    image=None, 
                    text="?", 
                    font=("Arial", 20)
                )
    
    def update_test_results(self, settings):
        """Обновить результаты преобразования тестовых изображений"""
        # TODO: Здесь будет вызов функции преобразования для тестовых изображений
        # с текущими настройками
        for i, img in enumerate(self.test_images):
            img_display = self.test_displays[i]
            dict.get
            img_display.conconfigure(image=convert(img.filename, 
                                                   settings.get('color_invert', False),
                                                   settings.get('color', False),
                                                   settings.get('fix_color', False)))
    
    def hide_window(self):
        """Скрыть окно вместо закрытия"""
        self.withdraw()
    
    def show_window(self):
        """Показать окно"""
        self.deiconify()
        self.lift()