"""
ComboBox с поддержкой иконок
"""

import os
from PyQt5.QtWidgets import QComboBox


class IconComboBox(QComboBox):
    """
    Расширенный ComboBox с поддержкой иконок
    
    Позволяет устанавливать кастомную иконку для стрелки dropdown
    """
    
    def __init__(self, parent=None, custom_option_text: str = "Вести свой вариант"):
        """
        Инициализация ComboBox
        
        Args:
            parent: Родительский виджет
            custom_option_text: Текст для опции пользовательского значения
        """
        super().__init__(parent)
        self.setEditable(True)
        self._custom_option_text = custom_option_text
        self._icon_path = None
    
    def set_icon(self, icon_path: str):
        """
        Устанавливает иконку для dropdown стрелки
        
        Args:
            icon_path: Путь к файлу иконки
        """
        self._icon_path = icon_path
        if icon_path and os.path.exists(icon_path):
            self.setStyleSheet(f"""
                QComboBox::down-arrow {{
                    image: url({icon_path});
                    width: 16px;
                    height: 16px;
                }}
            """)
    
    def showPopup(self):
        """
        Показывает выпадающий список
        
        Если выбрано "Вести свой вариант", список не показывается
        """
        if self.currentText() == self._custom_option_text:
            return
        super().showPopup()
    
    @property
    def icon_path(self) -> str:
        """Возвращает путь к иконке"""
        return self._icon_path
    
    @property
    def custom_option_text(self) -> str:
        """Возвращает текст пользовательской опции"""
        return self._custom_option_text
