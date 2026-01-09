import customtkinter as ctk
from PIL import Image

class ImageDisplay(ctk.CTkFrame):
    """Виджет для отображения изображения с адаптивным размером (процент от родителя)"""
    
    def __init__(self, master=None, title="Изображение", size_percent=0.8, **kwargs):
        """
        Args:
            master: Родительский виджет
            title: Заголовок виджета
            size_percent: Процент от размера родителя (0.0-1.0)
            **kwargs: Дополнительные параметры для CTkFrame
        """
        super().__init__(master, **kwargs)
        
        self.title = title
        self.size_percent = size_percent
        self.current_image = None
        self.current_ctk_image = None
        
        # Привязываем обработчик изменения размера
        self.bind('<Configure>', self.update_display_size)
        self.create_widgets()
    
    def create_widgets(self):
        # Заголовок
        self.title_label = ctk.CTkLabel(
            self, 
            text=self.title, 
            font=("Arial", 12)
        )
        self.title_label.pack(pady=(5, 0))
        # Фрейм для изображения (размер будет обновляться)
        self.image_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.image_frame.pack(pady=5, padx=5)
        
        # Метка для изображения
        self.image_label = ctk.CTkLabel(self.image_frame, text="")
        self.image_label.bind('<Button-1>', self.on_click)
        self.image_label.pack()
    
    def update_display_size(self, event=None):
        """Обновить размер области отображения при изменении размера виджета"""
        if event:
            # Вычисляем размер для изображения (процент от текущего размера)
            display_width = int(event.width * self.size_percent)
            display_height = int(event.height * self.size_percent)
            
            # Обновляем изображение, если оно есть
            if self.current_image:
                self.set_image(self.current_image)
    
    def set_image(self, image):
        """Установить изображение с масштабированием под текущий размер"""
        if image:
            img_copy = image.copy()
            
            # Получаем текущий размер виджета
            widget_width = self.winfo_width()
            widget_height = self.winfo_height()
            
            # Вычисляем размер для отображения
            display_width = int(widget_width * self.size_percent)
            display_height = int(widget_height * self.size_percent)
            
            # Если размеры еще не определены, используем минимальные
            if display_width < 10 or display_height < 10:
                display_width = 200
                display_height = 200
            
            # Масштабируем с сохранением пропорций
            img_copy.thumbnail((display_width, display_height), Image.Resampling.LANCZOS)
            
            ctk_img = ctk.CTkImage(
                light_image=img_copy,
                dark_image=img_copy,
                size=img_copy.size
            )
            
            self.image_label.configure(image=ctk_img, text="")
            self.current_image = image
            self.current_ctk_image = ctk_img
        else:
            self.image_label.configure(image=None, text="Нет изображения")
            
    def on_click(self, event=None):
        self.current_image.show()