"""
Переворачивающийся виджет (эффект карточки)
"""

from PyQt5.QtWidgets import QStackedWidget


class FlipWidget(QStackedWidget):
    """
    Виджет с эффектом переворачивания карточки
    
    Использует QStackedWidget для переключения между
    лицевой и обратной сторонами
    """
    
    def __init__(self, parent=None, min_width: int = 350, min_height: int = 350):
        """
        Инициализация виджета
        
        Args:
            parent: Родительский виджет
            min_width: Минимальная ширина
            min_height: Минимальная высота
        """
        super().__init__(parent)
        self.setMinimumSize(min_width, min_height)
    
    def flip(self):
        """Переключает сторону карточки"""
        current_index = self.currentIndex()
        self.setCurrentIndex(1 - current_index if self.count() > 1 else 0)
    
    def set_front(self, widget):
        """
        Устанавливает лицевую сторону
        
        Args:
            widget: Виджет для лицевой стороны
        """
        if self.count() > 0:
            self.removeWidget(self.widget(0))
        self.insertWidget(0, widget)
    
    def set_back(self, widget):
        """
        Устанавливает обратную сторону
        
        Args:
            widget: Виджет для обратной стороны
        """
        if self.count() > 1:
            self.removeWidget(self.widget(1))
        self.insertWidget(1, widget)
    
    def show_front(self):
        """Показывает лицевую сторону"""
        self.setCurrentIndex(0)
    
    def show_back(self):
        """Показывает обратную сторону"""
        if self.count() > 1:
            self.setCurrentIndex(1)
    
    @property
    def is_front_visible(self) -> bool:
        """Возвращает True, если видима лицевая сторона"""
        return self.currentIndex() == 0
