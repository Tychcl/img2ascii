import customtkinter as ctk

class EdgeSettings(ctk.CTkFrame):
    """Настройки границ в стиле основных параметров"""
    
    def __init__(self, master=None, on_settings_change=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_settings_change = on_settings_change
        self.dog_enabled = False
        
        self.create_widgets()
    
    def create_widgets(self):
        # Заголовок (опционально, можно убрать если не нужен)
        ctk.CTkLabel(
            self, 
            text="Параметры Границ", 
            font=("Arial", 14, "bold")
        ).pack(pady=(5, 5), anchor="center")
        
        # Препроцессинг - слайдер с меткой как в MainSettings
        self.create_slider_setting(
            text="Подавление шума:",
            var_name="preprocessing_var",
            default_value=0.9,
            row=0
        )
        
        # DoG чекбокс - как чекбоксы в MainSettings
        self.dog_var = ctk.BooleanVar(value=False)
        self.dog_cb = ctk.CTkCheckBox(
            self,
            text="DoG фильтр",
            variable=self.dog_var,
            command=self.on_dog_toggle
        )
        self.dog_cb.pack(pady=3, padx=5, anchor="w")
        
        # Детализация DoG - слайдер с меткой
        self.create_slider_setting(
            text="Детализация DoG:",
            var_name="detail_var",
            default_value=0.5,
            row=1
        )
        
        # Изначально отключаем детализацию
        self.detail_slider.configure(state="disabled")
        self.detail_value_label.configure(text_color="gray")
    
    def create_slider_setting(self, text, var_name, default_value, row):
        """Создать настройку со слайдером в стиле MainSettings"""
        # Фрейм для одной настройки
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", pady=3, padx=5)
        
        # Метка слева
        label = ctk.CTkLabel(frame, text=text, width=120)
        label.pack(side="left", padx=(0, 10))
        
        # Слайдер
        var = ctk.DoubleVar(value=default_value)
        setattr(self, var_name, var)
        
        slider = ctk.CTkSlider(
            frame,
            from_=0,
            to=1,
            number_of_steps=10,
            variable=var,
            command=self.on_change,
            height=12,
            width=150
        )
        slider.pack(side="left", padx=5, fill="x", expand=True)
        
        # Значение справа
        value_label = ctk.CTkLabel(frame, text=f"{default_value}", width=40)
        value_label.pack(side="left")
        
        # Сохраняем ссылки
        setattr(self, var_name.replace("var", "slider"), slider)
        setattr(self, var_name.replace("var", "value_label"), value_label)
    
    def on_dog_toggle(self):
        """Включить/выключить DoG фильтр"""
        self.dog_enabled = self.dog_var.get()
        
        if self.dog_enabled:
            self.detail_slider.configure(state="normal")
            self.detail_value_label.configure(text_color=("black", "white"))
        else:
            self.detail_slider.configure(state="disabled")
            self.detail_value_label.configure(text_color="gray")
        
        self.on_change()
    
    def on_change(self, *args):
        if self.on_settings_change:
            self.on_settings_change(self.get_settings())
    
    def get_settings(self):
        """Получить текущие настройки границ"""
        return {
            'preprocessing': self.preprocessing_var.get(),
            'DoG': self.dog_enabled,
            'detail': self.detail_var.get() if self.dog_enabled else 0.5
        }