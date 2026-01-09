import customtkinter as ctk

class MainSettings(ctk.CTkFrame):
    """Основные настройки с включением/выключением границ"""
    
    def __init__(self, master=None, on_settings_change=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_settings_change = on_settings_change
        self.edge_enabled = False
        
        self.create_widgets()
    
    def create_widgets(self):
        # Заголовок
        ctk.CTkLabel(
            self, 
            text="Параметры", 
            font=("Arial", 14, "bold")
        ).pack(pady=(5, 5), anchor="center")
        
        # Основные чекбоксы
        self.color_invert_var = ctk.BooleanVar(value=False)
        self.color_invert_cb = ctk.CTkCheckBox(
            self,
            text="Инверсия символов\n\"■@?0Poc:. \"",
            variable=self.color_invert_var,
            command=self.on_change
        )
        self.color_invert_cb.pack(pady=3, padx=5, anchor="w")
        
        self.color_var = ctk.BooleanVar(value=False)
        self.color_cb = ctk.CTkCheckBox(
            self,
            text="Цветные символы",
            variable=self.color_var,
            command=self.on_change
        )
        self.color_cb.pack(pady=3, padx=5, anchor="w")
        
        self.fix_color_var = ctk.BooleanVar(value=False)
        self.fix_color_cb = ctk.CTkCheckBox(
            self,
            text="Коррекция цвета\nМеняет темный цвет на белый",
            variable=self.fix_color_var,
            command=self.on_change
        )
        self.fix_color_cb.pack(pady=3, padx=5, anchor="w")
        
        # Edge (включение/выключение границ)
        self.edge_var = ctk.BooleanVar(value=False)
        self.edge_cb = ctk.CTkCheckBox(
            self,
            text="Выделить границы",
            variable=self.edge_var,
            command=self.on_edge_toggle
        )
        self.edge_cb.pack(pady=3, padx=5, anchor="w")
    
    def on_edge_toggle(self):
        """Включить/выключить обработку границ"""
        self.edge_enabled = self.edge_var.get()
        self.on_change()
    
    def on_change(self):
        """Вызывается при изменении настроек"""
        self.color_invert_cb.configure(text=f"Инверсия символов\n\"{" .:coP0?@■" if self.color_invert_var.get() else "■@?0Poc:. "}\"")
        if self.on_settings_change:
            self.on_settings_change(self.get_settings())
    
    def get_settings(self):
        """Получить текущие настройки"""
        return {
            'color_invert': self.color_invert_var.get(),
            'color': self.color_var.get(),
            'fix_color': self.fix_color_var.get(),
            'edge': self.edge_enabled
        }