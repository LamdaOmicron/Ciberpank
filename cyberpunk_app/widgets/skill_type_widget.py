"""
Виджет для отображения типа навыка
Переключаемый виджет с цветовой индикацией
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QBrush, QFont, QColor, QPen
from PyQt5.QtCore import Qt, QRect


class SkillTypeWidget(QWidget):
    """
    Виджет для отображения и переключения типа навыка
    
    Состояния:
        0: Чип (зеленый)
        1: Проф (розовый)
        2: Доп (желтый)
        3: Обычный (белый)
    """
    
    STATE_COLORS = {
        0: (QColor(0, 255, 0), "Чип"),
        1: (QColor(240, 0, 160), "Проф"),
        2: (QColor(255, 255, 0), "Доп"),
        3: (QColor(255, 255, 255), "Обыч")
    }
    
    def __init__(self, parent=None, initial_state: int = 3):
        """
        Инициализация виджета
        
        Args:
            parent: Родительский виджет
            initial_state: Начальное состояние (0-3)
        """
        super().__init__(parent)
        self._state = initial_state
        self.setFixedSize(80, 25)
        self.setToolTip("Кликните для изменения типа навыка")
    
    def paintEvent(self, event):
        """Отрисовка виджета"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Получаем цвет и текст для текущего состояния
        color, text = self.STATE_COLORS.get(self._state, (QColor(255, 255, 255), "?"))
        
        # Рисуем фон
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 3, 3)
        
        # Рисуем текст
        painter.setPen(QColor(0, 0, 0))
        font = QFont("Arial", 8, QFont.Bold)
        painter.setFont(font)
        painter.drawText(QRect(0, 0, self.width(), self.height()), Qt.AlignCenter, text)
        
        # Рисуем границу
        painter.setPen(QColor(100, 100, 100))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(0, 0, self.width() - 1, self.height() - 1, 3, 3)
    
    def mousePressEvent(self, event):
        """Обработка клика мыши - переключение состояния"""
        if event.button() == Qt.LeftButton:
            self._state = (self._state + 1) % len(self.STATE_COLORS)
            self.update()
        super().mousePressEvent(event)
    
    def get_state(self) -> int:
        """Возвращает текущее состояние"""
        return self._state
    
    def set_state(self, state: int):
        """
        Устанавливает состояние
        
        Args:
            state: Новое состояние (0-3)
        """
        if state in self.STATE_COLORS:
            self._state = state
            self.update()
    
    def state_name(self) -> str:
        """Возвращает имя текущего состояния"""
        return self.STATE_COLORS.get(self._state, ("?", "?"))[1]
