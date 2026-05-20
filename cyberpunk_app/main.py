"""
Точка входа приложения Cyberpunk Character Sheet
"""

import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from PyQt5.QtCore import Qt

from cyberpunk_app.core import CyberpunkCharacterSheet
from cyberpunk_app.styles import ThemeManager


def main():
    """Основная функция запуска приложения"""
    app = QApplication(sys.argv)
    
    # Установка иконки приложения
    icon_path = "icon.ico"
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Установка стиля приложения
    app.setStyle("Fusion")
    
    # Инициализация палитры стандартной темой
    themes = ThemeManager.get_themes()
    standard_theme = themes["Стандарт"]
    
    palette = QPalette()
    palette.setColor(QPalette.Window, standard_theme["bg_color"])
    palette.setColor(QPalette.WindowText, standard_theme["fg_color"])
    palette.setColor(QPalette.Base, standard_theme["section_bg"])
    palette.setColor(QPalette.AlternateBase, standard_theme["table_bg_color"])
    palette.setColor(QPalette.ToolTipBase, standard_theme["fg_color"])
    palette.setColor(QPalette.ToolTipText, standard_theme["bg_color"])
    palette.setColor(QPalette.Text, standard_theme["fg_color"])
    palette.setColor(QPalette.Button, standard_theme["bg_color"])
    palette.setColor(QPalette.ButtonText, standard_theme["fg_color"])
    palette.setColor(QPalette.BrightText, standard_theme["accent_color"])
    palette.setColor(QPalette.Highlight, standard_theme["accent_color"])
    palette.setColor(QPalette.HighlightedText, standard_theme["table_header_fg"])
    app.setPalette(palette)
    
    # Установка шрифта
    font = QFont("Courier New", 10)
    app.setFont(font)
    
    # Создание и показ главного окна
    window = CyberpunkCharacterSheet()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
