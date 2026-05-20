"""
Базовый класс для всех вкладок приложения
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from typing import Optional


class BaseTab(QWidget):
    """
    Базовый класс для вкладок приложения
    
    Предоставляет общую функциональность:
    - Хранение ссылки на родительское окно
    - Метод обновления стилей
    - Базовая структура layout
    """
    
    def __init__(self, parent: Optional[QWidget] = None, tab_name: str = ""):
        """
        Инициализация базовой вкладки
        
        Args:
            parent: Родительский виджет (обычно главное окно)
            tab_name: Название вкладки
        """
        super().__init__(parent)
        self.parent_window = parent
        self.tab_name = tab_name
        
        # Основной layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        
        # Ссылка на style_provider родительского окна
        self.style_provider = None
        if hasattr(parent, 'style_provider'):
            self.style_provider = parent.style_provider
    
    def update_styles(self):
        """
        Обновляет стили элементов вкладки
        
        Переопределяется в дочерних классах
        """
        if self.style_provider:
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: {self.style_provider._get_color('bg_color')};
                    color: {self.style_provider._get_color('fg_color')};
                    font-family: 'Courier New';
                }}
            """)
    
    def get_style_provider(self):
        """Возвращает провайдер стилей"""
        return self.style_provider
