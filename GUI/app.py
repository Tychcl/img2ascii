import customtkinter as ctk
from widgets.ImageSelector import ImageSelector
from widgets.ImageDisplay import ImageDisplay
from widgets.MainSettings import MainSettings
from widgets.EdgeSettings import EdgeSettings
from tkinter import filedialog
from PIL import Image
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # папка GUI
project_root = os.path.dirname(parent_dir)  # корень проекта
sys.path.insert(0, project_root)
#from functions.ascii import convert


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_default_color_theme("dark-blue")

        self.title("Ascii / Tychcl")
        self.geometry("600x700")
        
        try:
            self.iconbitmap("resources/icons/64.ico")
        except:
            pass
        
        self.original_image = None
        self.result_image = None
        self.test_window = None
        
        # Хранилище настроек
        self.main_settings = {}
        self.edge_settings = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        # Верхняя часть: выбор изображения
        self.image_selector = ImageSelector(
            self, 
            on_image_selected=self.on_image_selected
        )
        self.image_selector.pack(pady=10, padx=10, fill="x")
        
        # Основная область
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Левая часть: изображения
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", padx=5, pady=5, fill="both", expand=True)
        
        # Оригинальное изображение
        self.original_display = ImageDisplay(left_frame, title="Оригинал")
        self.original_display.pack(pady=5, padx=5, fill="both", expand=True)
        
        # Результирующее изображение
        self.result_display = ImageDisplay(left_frame, title="Результат ASCII")
        self.result_display.pack(pady=5, padx=5, fill="both", expand=True)
        
        # Правая часть: настройки
        right_frame = ctk.CTkFrame(main_frame, width=300)
        right_frame.pack(side="right", padx=5, pady=5, fill="y")
        right_frame.pack_propagate(False)
        
        # Основные настройки
        self.main_settings_widget = MainSettings(
            right_frame,
            on_settings_change=self.on_main_settings_change
        )
        self.main_settings_widget.pack(pady=5, padx=5, fill="x")
        
        # Настройки границ (изначально скрыты)
        self.edge_settings_frame = ctk.CTkFrame(right_frame)

        # Убедись, что фон темный:
        self.edge_settings_frame.configure(fg_color="transparent")
        self.edge_settings_frame.pack(pady=0, padx=5, fill="x")
        
        self.edge_settings_widget = EdgeSettings(
            self.edge_settings_frame,
            on_settings_change=self.on_edge_settings_change
        )
        self.edge_settings_widget.pack(pady=0 ,fill="x")
        
        # Изначально скрываем настройки границ
        self.edge_settings_frame.pack_forget()
        
        # Нижняя часть: кнопки
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10, padx=10, fill="x")
        
        # Кнопка показа/скрытия тестовых изображений
        self.toggle_test_btn = ctk.CTkButton(
            right_frame,
            text="Использовать тестовое изображение",
            command=self.use_test_image,
            height=40
        )
        self.toggle_test_btn.pack(padx=5, pady=5, fill="x", side="bottom")
        
        # Кнопка преобразования
        self.convert_btn = ctk.CTkButton(
            button_frame,
            text="Преобразовать в ASCII",
            command=self.convert_to_ascii,
            height=40
        )
        self.convert_btn.pack(side="left", padx=10)
        
        # Кнопка сохранения
        self.save_btn = ctk.CTkButton(
            button_frame,
            text="Сохранить результат",
            command=self.save_result,
            height=40
        )
        self.save_btn.pack(side="left", padx=10)
        
        # Кнопка открытия папки
        self.open_folder_btn = ctk.CTkButton(
            button_frame,
            text="Открыть папку",
            command=self.open_folder,
            height=40
        )
        self.open_folder_btn.pack(side="left", padx=10)
    
    def use_test_image(self):
        self.image_selector.entry.delete(0, "end")
        self.image_selector.entry.insert(0, os.path.abspath("resources/examples/Simple.jpg"))
        self.image_selector.load_image()
        self.on_image_selected(self.image_selector.current_image)
    
    def on_image_selected(self, image):
        """Обработчик выбора изображения"""
        self.original_image = image
        self.original_display.set_image(image)
    
    def on_main_settings_change(self, settings):
        """Обработчик изменения основных настроек"""
        self.main_settings = settings
        
        # Управляем видимостью настроек границ
        if settings.get('edge', False):
            self.edge_settings_frame.pack(pady=5, padx=5, fill="x")
        else:
            self.edge_settings_frame.pack_forget()
        
        self.update_all_settings()
    
    def on_edge_settings_change(self, settings):
        """Обработчик изменения настроек границ"""
        self.edge_settings = settings
        self.update_all_settings()
    
    def update_all_settings(self):
        """Объединить все настройки и отправить обновление"""
        # Объединяем настройки
        all_settings = {**self.main_settings}

        # Добавляем настройки границ только если edge включен
        if self.main_settings.get('edge', False):
            all_settings.update(self.edge_settings)
        else:
            # Если границы выключены, используем значения по умолчанию
            all_settings.update({
                'preprocessing': 0.9,
                'DoG': False,
                'detail': 0.5
            })

        # Обновляем тестовые изображения если окно открыто И СУЩЕСТВУЕТ
    
    def convert_to_ascii(self):
        """Преобразовать изображение в ASCII арт"""
        if not self.original_image:
            return

        try:
            # Пробуем разные варианты импорта
            try:
                from functions.ascii import convert
            except ImportError:
                # Альтернативный путь
                import sys
                sys.path.append(os.path.dirname(os.path.dirname(__file__)))
                from functions.ascii import convert

            # Получаем все текущие настройки
            all_settings = {**self.main_settings}
            if self.main_settings.get('edge', False):
                all_settings.update(self.edge_settings)
            else:
                all_settings.update({
                    'preprocessing': 0.0,
                    'DoG': False,
                    'detail': 0.5
                })

            # Вызываем функцию преобразования
            result = convert(
                self.original_image,
                all_settings.get('color_invert', False),
                all_settings.get('color', False),
                all_settings.get('fix_color', False)
            )
            self.result_image = result[0]
            self.result_display.set_image(self.result_image)
            self.save_path = result[1]
        
        except ImportError as e:
            print(f"Ошибка импорта: {e}")
            print(f"Текущий sys.path: {sys.path}")
            print(f"Текущая директория: {os.getcwd()}")
            # Показываем сообщение об ошибке
            import tkinter.messagebox as mb
            mb.showerror("Ошибка", "Не удалось загрузить модуль ascii.py")
    
    def save_result(self):
        """Сохранить результат"""
        if not self.result_image:
            return
        
        try:
            self.result_image.save(self.save_path)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def open_folder(self):
        """Открыть папку с результатами"""
        import subprocess
        subprocess.Popen(f'explorer "Result"')

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()