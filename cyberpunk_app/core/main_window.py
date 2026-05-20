"""
Главное окно приложения Character Sheet
"""

import os
import sys
import json
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, 
    QMenuBar, QMenu, QAction, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from PyQt5.QtCore import Qt

from ..styles import ThemeManager, StyleProvider
from ..utils.logger import LoggerMixin, setup_logger


class CyberpunkCharacterSheet(QMainWindow, LoggerMixin):
    """
    Главное окно приложения для управления персонажем Cyberpunk
    
    Содержит вкладки для всех разделов листа персонажа:
    - Основная информация
    - Навыки
    - Кибернетика
    - Оружие
    - Экипировка
    - Lifepath
    - Cyberdeck
    """
    
    def __init__(self):
        """Инициализация главного окна"""
        super().__init__()
        self.logger.info("Инициализация главного окна")
        
        # Настройка окна
        self.setWindowTitle("CYBERPUNK 2020 - Character Sheet")
        self.setGeometry(100, 100, 1200, 800)
        
        # Инициализация темы
        self.current_theme = "Стандарт"
        self._init_theme_attributes(self.current_theme)
        self.style_provider = StyleProvider(self._current_theme_data)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Вкладки
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Хранилища данных
        self.stats_entries = {}
        self.skill_entries = {}
        self.current_image_path = ""
        
        # Инициализация разделов
        self._create_tabs()
        
        # Создание меню
        self._create_menu()
        
        # Применение темы
        self.apply_theme(self.current_theme)
    
    def _init_theme_attributes(self, theme_name: str):
        """Инициализирует атрибуты темы значениями из выбранной темы"""
        themes = ThemeManager.get_themes()
        self._current_theme_data = themes.get(theme_name, themes["Стандарт"])
        
        # Копируем цвета в атрибуты для совместимости
        theme = self._current_theme_data
        self.bg_color = theme["bg_color"]
        self.fg_color = theme["fg_color"]
        self.accent_color = theme["accent_color"]
        self.section_bg = theme["section_bg"]
        self.table_border_color = theme["table_border_color"]
        self.table_bg_color = theme["table_bg_color"]
        self.table_header_bg = theme["table_header_bg"]
        self.table_header_fg = theme["table_header_fg"]
        self.red_color = theme["red_color"]
        self.yellow_color = theme["yellow_color"]
        self.green_color = theme["green_color"]
    
    def apply_theme(self, theme_name: str):
        """
        Применяет выбранную тему ко всему приложению
        
        Args:
            theme_name: Название темы для применения
        """
        themes = ThemeManager.get_themes()
        if theme_name not in themes:
            self.logger.warning(f"Тема '{theme_name}' не найдена, используется стандартная")
            theme_name = "Стандарт"
        
        theme = themes[theme_name]
        self.current_theme = theme_name
        self._current_theme_data = theme
        self.style_provider = StyleProvider(theme)
        
        # Обновляем атрибуты цветов
        self._init_theme_attributes(theme_name)
        
        # Применяем палитру к приложению
        self._apply_palette(theme)
        
        # Обновляем стили
        self.update_styles()
        self.logger.info(f"Применена тема: {theme_name}")
    
    def _apply_palette(self, theme: dict):
        """Устанавливает палитру приложения на основе темы"""
        app = QApplication.instance()
        palette = QPalette()
        
        palette.setColor(QPalette.Window, theme["bg_color"])
        palette.setColor(QPalette.WindowText, theme["fg_color"])
        palette.setColor(QPalette.Base, theme["section_bg"])
        palette.setColor(QPalette.AlternateBase, theme["table_bg_color"])
        palette.setColor(QPalette.ToolTipBase, theme["fg_color"])
        palette.setColor(QPalette.ToolTipText, theme["bg_color"])
        palette.setColor(QPalette.Text, theme["fg_color"])
        palette.setColor(QPalette.Button, theme["bg_color"])
        palette.setColor(QPalette.ButtonText, theme["fg_color"])
        palette.setColor(QPalette.BrightText, theme["accent_color"])
        palette.setColor(QPalette.Highlight, theme["accent_color"])
        palette.setColor(QPalette.HighlightedText, theme["table_header_fg"])
        
        app.setPalette(palette)
    
    def update_styles(self):
        """Обновляет стили всех элементов интерфейса"""
        self.setStyleSheet(self._get_main_style())
        self.tabs.setStyleSheet(self._get_tab_style())
        
        # Обновляем стили всех вкладок
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if hasattr(tab, 'update_styles'):
                tab.update_styles()
        
        # Обновляем стили меню
        if hasattr(self, 'menu_bar'):
            self.menu_bar.setStyleSheet(self.style_provider.get_menu_style())
    
    def _create_tabs(self):
        """Создает и добавляет все вкладки"""
        # Здесь будут вызовы методов создания вкладок
        # Пока создадим заглушки
        from .tabs import (
            MainTab, SkillsTab, CyberneticsTab,
            WeaponsTab, EquipmentTab, LifepathTab, CyberdeckTab
        )
        
        self.main_tab = MainTab(self)
        self.skills_tab = SkillsTab(self)
        self.cybernetics_tab = CyberneticsTab(self)
        self.weapons_tab = WeaponsTab(self)
        self.equipment_tab = EquipmentTab(self)
        self.lifepath_tab = LifepathTab(self)
        self.cyberdeck_tab = CyberdeckTab(self)
        
        self.tabs.addTab(self.main_tab, "Основное")
        self.tabs.addTab(self.skills_tab, "Навыки")
        self.tabs.addTab(self.cybernetics_tab, "Кибернетика")
        self.tabs.addTab(self.weapons_tab, "Оружие")
        self.tabs.addTab(self.equipment_tab, "Экипировка")
        self.tabs.addTab(self.lifepath_tab, "Lifepath")
        self.tabs.addTab(self.cyberdeck_tab, "Cyberdeck")
    
    def _create_menu(self):
        """Создает меню приложения"""
        self.menu_bar = self.menuBar()
        self.menu_bar.setStyleSheet(self.style_provider.get_menu_style())
        
        # Файл
        file_menu = self.menu_bar.addMenu("Файл")
        
        new_action = QAction("Новый персонаж", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_character)
        file_menu.addAction(new_action)
        
        save_action = QAction("Сохранить", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_character)
        file_menu.addAction(save_action)
        
        load_action = QAction("Загрузить", self)
        load_action.setShortcut("Ctrl+O")
        load_action.triggered.connect(self.load_character)
        file_menu.addAction(load_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Тема
        theme_menu = self.menu_bar.addMenu("Тема")
        
        themes = ThemeManager.get_theme_names()
        for theme_name in themes:
            action = QAction(theme_name, self)
            action.triggered.connect(lambda checked, name=theme_name: self.apply_theme(name))
            theme_menu.addAction(action)
        
        # Справка
        help_menu = self.menu_bar.addMenu("Справка")
        
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    # Методы-заглушки для дальнейшего развития
    def new_character(self):
        """Создает нового персонажа"""
        reply = QMessageBox.question(
            self, 'Новый персонаж',
            'Все несохраненные данные будут потеряны. Продолжить?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.logger.info("Создание нового персонажа")
            # TODO: Реализовать сброс данных
    
    def save_character(self):
        """Сохраняет данные персонажа в файл"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить персонажа",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            self.logger.info(f"Сохранение персонажа в {file_path}")
            # TODO: Реализовать сохранение
    
    def load_character(self):
        """Загружает данные персонажа из файла"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Загрузить персонажа",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            self.logger.info(f"Загрузка персонажа из {file_path}")
            # TODO: Реализовать загрузку
    
    def show_about(self):
        """Показывает диалог о программе"""
        QMessageBox.about(
            self,
            "О программе",
            "Cyberpunk Character Sheet v1.0\n\n"
            "Приложение для создания и управления персонажами Cyberpunk 2020/RED"
        )
    
    # Методы стилей (делегирование к style_provider)
    def _get_main_style(self) -> str:
        """Возвращает стиль для главного окна"""
        return f"""
            QMainWindow {{
                background-color: {self.style_provider._get_color('bg_color')};
                color: {self.style_provider._get_color('fg_color')};
                font-family: 'Courier New';
                font-size: 10pt;
            }}
        """
    
    def _get_tab_style(self) -> str:
        """Возвращает стиль для вкладок"""
        return self.style_provider.get_tab_widget_style()
