import customtkinter as ctk

class EdgeSettings(ctk.CTkFrame):
    """Настройки границ в стиле основных параметров"""
    
    def __init__(self, master=None, on_settings_change=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_settings_change = on_settings_change
        self.dog_enabled = False
        
        self.create_widgets()
    
    def create_widgets(self):
        ctk.CTkLabel(
            self, 
            text="Параметры Границ", 
            font=("Arial", 14, "bold")
        ).pack(pady=(5, 10), anchor="center")
        
        self.create_slider_setting(
            text="Плотность:",
            var_name="sector_threshold_var",
            default_value=0.25,
            row=4
        )
        
        self.create_checkbox_slider_setting(
            text="Подавление шума:",
            var_name="preprocessing_var",
            default_value=0.90,
            row=1,
            enabled=False 
        )
        
        self.create_checkbox_slider_setting(
            text="Выделить грани:",
            var_name="dog_var",
            default_value=0.50,
            row=2,
            is_dog=True
        )
    
    def create_checkbox_slider_setting(self, text, var_name, default_value, row, is_dog=False, enabled=True):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="x", pady=3, padx=5)
        
        top_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=25)
        top_frame.pack(fill="x", padx=5)
        top_frame.pack_propagate(False)
        
        checkbox_var = ctk.BooleanVar(value=enabled if not is_dog else False)
        checkbox = ctk.CTkCheckBox(
            top_frame,
            text="",
            variable=checkbox_var,
            width=20,
            command=lambda: self.on_checkbox_toggle(checkbox_var.get(), var_name)
        )
        checkbox.pack(side="left", padx=(0, 10))
        setattr(self, f"{var_name.replace('var', 'checkbox')}", checkbox)
        setattr(self, f"{var_name.replace('var', 'checkbox_var')}", checkbox_var)
        
        label = ctk.CTkLabel(top_frame, text=text, width=120)
        label.pack(side="left", padx=(0, 10))
        
        var = ctk.DoubleVar(value=default_value)
        setattr(self, var_name, var)
        
        value_label = ctk.CTkLabel(top_frame, text=f"{default_value}", width=40)
        value_label.pack(side="right")
        setattr(self, var_name.replace("var", "value_label"), value_label)
        
        slider_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        slider_frame.pack(fill="x", padx=(30, 5), pady=(0, 5))
        
        slider = ctk.CTkSlider(
            slider_frame,
            from_=0,
            to=1,
            number_of_steps=100,
            variable=var,
            command=lambda val: self.on_slider_change(val, var_name),
            height=12,
            width=150
        )
        slider.pack(fill="x", expand=True)
        setattr(self, var_name.replace("var", "slider"), slider)
        
        if is_dog:
            self.dog_checkbox = checkbox
            self.dog_checkbox_var = checkbox_var
            self.dog_checkbox.configure(
                command=self.on_dog_checkbox_toggle
            )
            self.dog_enabled = False
            checkbox_var.set(False)
            slider.configure(state="disabled")
            value_label.configure(text_color="gray")
        else:
            if not enabled:
                slider.configure(state="disabled")
                value_label.configure(text_color="gray")
    
    def create_slider_setting(self, text, var_name, default_value, row):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="x", pady=3, padx=5)
        
        top_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=25)
        top_frame.pack(fill="x", padx=5)
        top_frame.pack_propagate(False)
        
        empty_space = ctk.CTkLabel(top_frame, text="", width=30)
        empty_space.pack(side="left", padx=(0, 0))
        
        label = ctk.CTkLabel(top_frame, text=text, width=120)
        label.pack(side="left", padx=(0, 10))
        
        var = ctk.DoubleVar(value=default_value)
        setattr(self, var_name, var)
        
        value_label = ctk.CTkLabel(top_frame, text=f"{default_value}", width=40)
        value_label.pack(side="left")
        setattr(self, var_name.replace("var", "value_label"), value_label)
        
        slider_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        slider_frame.pack(fill="x", padx=(30, 5), pady=(0, 5))
        
        slider = ctk.CTkSlider(
            slider_frame,
            from_=0,
            to=1,
            number_of_steps=100,
            variable=var,
            command=lambda val: self.on_slider_change(val, var_name),
            height=12,
            width=150
        )
        slider.pack(fill="x", expand=True)
        setattr(self, var_name.replace("var", "slider"), slider)
    
    def on_checkbox_toggle(self, state, var_name):
        slider = getattr(self, var_name.replace("var", "slider"))
        value_label = getattr(self, var_name.replace("var", "value_label"))
        
        if state:
            slider.configure(state="normal")
            value_label.configure(text_color=("black", "white"))
        else:
            slider.configure(state="disabled")
            value_label.configure(text_color="gray")
        
        self.on_change()
    
    def on_dog_checkbox_toggle(self):
        self.dog_enabled = self.dog_checkbox_var.get()
        
        if self.dog_enabled:
            self.dog_slider.configure(state="normal")
            self.dog_value_label.configure(text_color=("black", "white"))
        else:
            self.dog_slider.configure(state="disabled")
            self.dog_value_label.configure(text_color="gray")
        
        self.on_change()
    
    def on_slider_change(self, value, var_name):
        value_label = getattr(self, var_name.replace("var", "value_label"))
        value_label.configure(text=f"{value:.2f}")
        self.on_change()
    
    def on_change(self, *args):
        if self.on_settings_change:
            self.on_settings_change(self.get_settings())
    
    def get_settings(self):
        return {
            'preprocessing_bool': self.preprocessing_checkbox_var.get(),
            'preprocessing_value':  self.preprocessing_var.get() if self.preprocessing_checkbox_var.get() else 0.9,
            'dog_bool': self.dog_checkbox_var.get(),
            'dog_value':  self.dog_var.get() if self.dog_checkbox_var.get() else 0.5,
            'sector_threshold': self.sector_threshold_var.get()
        }