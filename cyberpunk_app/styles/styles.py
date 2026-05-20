"""
Провайдер стилей для UI компонентов
Генерирует CSS-подобные стили для PyQt5 виджетов
"""

from typing import Optional


class StyleProvider:
    """Класс для генерации стилей UI компонентов"""
    
    def __init__(self, theme: dict):
        """
        Инициализация провайдера стилей
        
        Args:
            theme: Словарь с цветами темы
        """
        self.theme = theme
    
    def get_group_box_style(self) -> str:
        """Возвращает стиль для QGroupBox"""
        return f"""
            QGroupBox {{
                background-color: {self._get_color('section_bg')};
                color: {self._get_color('fg_color')};
                border: 2px solid {self._get_color('accent_color')};
                border-radius: 5px;
                margin-top: 10px;
                font-family: 'Courier New';
                font-weight: bold;
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: {self._get_color('accent_color')};
            }}
        """
    
    def get_line_edit_style(self) -> str:
        """Возвращает стиль для QLineEdit"""
        return f"""
            QLineEdit {{
                background-color: {self._get_color('bg_color')};
                color: {self._get_color('fg_color')};
                border: 1px solid {self._get_color('table_border_color')};
                padding: 5px;
                font-family: 'Courier New';
                font-size: 10pt;
                border-radius: 3px;
            }}
            
            QLineEdit:focus {{
                border: 1px solid {self._get_color('accent_color')};
            }}
            
            QLineEdit:disabled {{
                background-color: #2a2a2a;
                color: #888888;
            }}
        """
    
    def get_text_edit_style(self) -> str:
        """Возвращает стиль для QTextEdit"""
        return f"""
            QTextEdit {{
                background-color: {self._get_color('bg_color')};
                color: {self._get_color('fg_color')};
                border: 1px solid {self._get_color('table_border_color')};
                padding: 5px;
                font-family: 'Courier New';
                font-size: 10pt;
                border-radius: 3px;
            }}
            
            QTextEdit:focus {{
                border: 1px solid {self._get_color('accent_color')};
            }}
        """
    
    def get_button_style(self, variant: str = 'default') -> str:
        """
        Возвращает стиль для QPushButton
        
        Args:
            variant: Вариант стиля ('default', 'danger', 'success')
        """
        base_style = f"""
            QPushButton {{
                background-color: {self._get_color('bg_color')};
                color: {self._get_color('fg_color')};
                border: 1px solid {self._get_color('accent_color')};
                padding: 5px 10px;
                font-weight: bold;
                font-family: 'Courier New';
                border-radius: 3px;
            }}
            
            QPushButton:hover {{
                background-color: #333333;
            }}
            
            QPushButton:pressed {{
                background-color: #555555;
            }}
            
            QPushButton:disabled {{
                background-color: #2a2a2a;
                color: #666666;
                border: 1px solid #444444;
            }}
        """
        
        if variant == 'danger':
            base_style += """
                QPushButton#dangerButton {
                    border: 1px solid #ff4444;
                }
                
                QPushButton#dangerButton:hover {
                    background-color: #552222;
                }
            """
        elif variant == 'success':
            base_style += """
                QPushButton#successButton {
                    border: 1px solid #44ff44;
                }
                
                QPushButton#successButton:hover {
                    background-color: #225522;
                }
            """
        
        return base_style
    
    def get_tree_widget_style(self) -> str:
        """Возвращает стиль для QTreeWidget"""
        return f"""
            QTreeWidget {{
                background-color: {self._get_color('bg_color')};
                color: {self._get_color('fg_color')};
                border: 1px solid {self._get_color('table_border_color')};
                font-family: 'Courier New';
                font-size: 10pt;
                border-radius: 3px;
            }}
            
            QTreeWidget::item {{
                padding: 5px;
            }}
            
            QTreeWidget::item:selected {{
                background-color: #444444;
                color: {self._get_color('fg_color')};
            }}
            
            QTreeWidget::item:hover {{
                background-color: #333333;
            }}
            
            QHeaderView::section {{
                background-color: {self._get_color('table_header_bg')};
                color: {self._get_color('table_header_fg')};
                padding: 4px;
                border: 1px solid {self._get_color('table_border_color')};
                font-weight: bold;
            }}
        """
    
    def get_table_style(self) -> str:
        """Возвращает стиль для QTableWidget"""
        return f"""
            QTableWidget {{
                background-color: {self._get_color('table_bg_color')};
                color: {self._get_color('fg_color')};
                gridline-color: {self._get_color('table_border_color')};
                font-family: 'Courier New';
                font-size: 10pt;
                border: 1px solid {self._get_color('table_border_color')};
            }}
            
            QTableWidget::item {{
                padding: 4px;
            }}
            
            QTableWidget::item:selected {{
                background-color: #444444;
                color: {self._get_color('fg_color')};
            }}
            
            QHeaderView::section {{
                background-color: {self._get_color('table_header_bg')};
                color: {self._get_color('table_header_fg')};
                padding: 4px;
                border: 1px solid {self._get_color('table_border_color')};
                font-weight: bold;
            }}
        """
    
    def get_combo_box_style(self) -> str:
        """Возвращает стиль для QComboBox"""
        return f"""
            QComboBox {{
                background-color: {self._get_color('bg_color')};
                color: {self._get_color('fg_color')};
                border: 1px solid {self._get_color('table_border_color')};
                padding: 5px;
                font-family: 'Courier New';
                border-radius: 3px;
            }}
            
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {self._get_color('fg_color')};
                margin-right: 5px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {self._get_color('bg_color')};
                color: {self._get_color('fg_color')};
                border: 1px solid {self._get_color('table_border_color')};
                selection-background-color: {self._get_color('accent_color')};
            }}
        """
    
    def get_scroll_area_style(self) -> str:
        """Возвращает стиль для QScrollArea"""
        return f"""
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
            
            QScrollBar:vertical {{
                background-color: {self._get_color('bg_color')};
                width: 12px;
                border-radius: 6px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {self._get_color('accent_color')};
                border-radius: 6px;
                min-height: 20px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: #ff6666;
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar:horizontal {{
                background-color: {self._get_color('bg_color')};
                height: 12px;
                border-radius: 6px;
            }}
            
            QScrollBar::handle:horizontal {{
                background-color: {self._get_color('accent_color')};
                border-radius: 6px;
                min-width: 20px;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background-color: #ff6666;
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """
    
    def get_tab_widget_style(self) -> str:
        """Возвращает стиль для QTabWidget"""
        return f"""
            QTabWidget::pane {{
                border: 1px solid {self._get_color('accent_color')};
                border-radius: 5px;
                background-color: {self._get_color('bg_color')};
            }}
            
            QTabBar::tab {{
                background-color: {self._get_color('section_bg')};
                color: {self._get_color('fg_color')};
                padding: 8px 15px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-family: 'Courier New';
                font-weight: bold;
            }}
            
            QTabBar::tab:selected {{
                background-color: {self._get_color('bg_color')};
                border-bottom: 2px solid {self._get_color('accent_color')};
            }}
            
            QTabBar::tab:hover {{
                background-color: #333333;
            }}
        """
    
    def get_menu_style(self) -> str:
        """Возвращает стиль для меню"""
        return f"""
            QMenuBar {{
                background-color: {self._get_color('section_bg')};
                color: {self._get_color('fg_color')};
                border-bottom: 1px solid {self._get_color('accent_color')};
                font-family: 'Courier New';
            }}
            
            QMenuBar::item {{
                padding: 5px 10px;
            }}
            
            QMenuBar::item:selected {{
                background-color: {self._get_color('accent_color')};
                color: {self._get_color('table_header_fg')};
            }}
            
            QMenu {{
                background-color: {self._get_color('bg_color')};
                color: {self._get_color('fg_color')};
                border: 1px solid {self._get_color('accent_color')};
                font-family: 'Courier New';
            }}
            
            QMenu::item {{
                padding: 5px 20px;
            }}
            
            QMenu::item:selected {{
                background-color: {self._get_color('accent_color')};
                color: {self._get_color('table_header_fg')};
            }}
        """
    
    def _get_color(self, key: str) -> str:
        """
        Получает цвет из темы по ключу
        
        Args:
            key: Ключ цвета в словаре темы
            
        Returns:
            Строковое представление цвета (hex)
        """
        color = self.theme.get(key, '#ffffff')
        if hasattr(color, 'name'):
            return color.name()
        return color
