"""
Менеджер тем приложения
Управляет цветовыми схемами и темами оформления
"""

from PyQt5.QtGui import QColor


class ThemeManager:
    """Класс для управления темами приложения"""
    
    THEMES = {
        "Стандарт": {
            "bg_color": QColor(13, 13, 13),
            "fg_color": QColor(0, 255, 0),
            "accent_color": QColor(249, 59, 71),
            "section_bg": QColor(26, 26, 26),
            "table_border_color": QColor(69, 206, 162),
            "table_bg_color": QColor(34, 34, 34),
            "table_header_bg": QColor(249, 59, 71),
            "table_header_fg": QColor(13, 13, 13),
            "red_color": "#ff0000",
            "yellow_color": "#ffff00",
            "green_color": "#00ff00"
        },
        "Синий/Черная": {
            "bg_color": QColor(13, 13, 13),
            "fg_color": QColor(0, 150, 255),
            "accent_color": QColor(0, 100, 200),
            "section_bg": QColor(26, 26, 40),
            "table_border_color": QColor(0, 150, 255),
            "table_bg_color": QColor(34, 34, 50),
            "table_header_bg": QColor(0, 100, 200),
            "table_header_fg": QColor(13, 13, 13),
            "red_color": "#ff5555",
            "yellow_color": "#ffff88",
            "green_color": "#55ff55"
        },
        "Коричневая/Телесная": {
            "bg_color": QColor(40, 30, 25),
            "fg_color": QColor(210, 180, 140),
            "accent_color": QColor(180, 100, 80),
            "section_bg": QColor(60, 45, 35),
            "table_border_color": QColor(180, 140, 100),
            "table_bg_color": QColor(70, 55, 45),
            "table_header_bg": QColor(180, 100, 80),
            "table_header_fg": QColor(40, 30, 25),
            "red_color": "#cc4444",
            "yellow_color": "#ddcc44",
            "green_color": "#88cc44"
        },
        "Светлая/Серебристая": {
            "bg_color": QColor(255, 218, 185),  # Персиковый
            "fg_color": QColor(101, 67, 33),    # Темно-коричневый
            "accent_color": QColor(205, 133, 63),  # Персиково-коричневый
            "section_bg": QColor(245, 222, 179),   # Бежевый
            "table_border_color": QColor(210, 180, 140),  # Темный бежевый
            "table_bg_color": QColor(255, 239, 213),  # Светлый персиковый
            "table_header_bg": QColor(205, 133, 63),  # Персиково-коричневый
            "table_header_fg": QColor(255, 255, 255),  # Белый
            "red_color": "#cd5c5c",  # Индийский красный
            "yellow_color": "#daa520",  # Золотистый
            "green_color": "#6b8e23"  # Оливковый
        }
    }
    
    @classmethod
    def get_themes(cls) -> dict:
        """Возвращает доступные темы"""
        return cls.THEMES.copy()
    
    @classmethod
    def get_theme(cls, name: str) -> dict:
        """Возвращает конкретную тему по имени"""
        return cls.THEMES.get(name, cls.THEMES["Стандарт"])
    
    @classmethod
    def get_theme_names(cls) -> list:
        """Возвращает список имен доступных тем"""
        return list(cls.THEMES.keys())
