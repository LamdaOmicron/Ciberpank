"""
Вкладка Lifepath для истории персонажа
"""

from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, QTextEdit,
    QGroupBox, QPushButton, QHeaderView, QAbstractItemView, QComboBox
)
from .base_tab import BaseTab


class LifepathTab(BaseTab):
    """Вкладка для управления историей персонажа (Lifepath)"""
    
    def __init__(self, parent=None):
        super().__init__(parent, "Lifepath")
        self.lifepath_data = {}
        self.events = []
        self._init_ui()
    
    def _init_ui(self):
        """Инициализация UI"""
        # Основные параметры lifepath
        params_group = QGroupBox("Параметры Lifepath")
        params_layout = QVBoxLayout()
        
        self.origin_combo = QComboBox()
        self.origin_combo.addItems(["", "Solo", "Netrunner", "Techie", "Medtech", "Media", "Fixer", "Lawman", "Nomad", "Corporate", "Rockerboy"])
        
        self.life_path_edit = QTextEdit()
        self.life_path_edit.setPlaceholderText("Описание жизненного пути...")
        self.life_path_edit.setMaximumHeight(100)
        
        params_layout.addWidget(QLabel("Происхождение:"))
        params_layout.addWidget(self.origin_combo)
        params_layout.addWidget(QLabel("Краткая история:"))
        params_layout.addWidget(self.life_path_edit)
        
        params_group.setLayout(params_layout)
        self.layout.addWidget(params_group)
        
        # Таблица событий
        events_group = QGroupBox("События жизни")
        events_layout = QVBoxLayout()
        
        self.events_table = QTableWidget()
        self.events_table.setColumnCount(3)
        self.events_table.setHorizontalHeaderLabels(["Год", "Событие", "Тип"])
        
        header = self.events_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        
        self.events_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        events_layout.addWidget(self.events_table)
        events_group.setLayout(events_layout)
        self.layout.addWidget(events_group)
        
        # Генераторы событий
        gen_layout = QHBoxLayout()
        
        self.gen_lucky_btn = QPushButton("Счастливое событие")
        self.gen_disaster_btn = QPushButton("Неудача")
        self.gen_life_btn = QPushButton("Жизненное событие")
        
        gen_layout.addWidget(self.gen_lucky_btn)
        gen_layout.addWidget(self.gen_disaster_btn)
        gen_layout.addWidget(self.gen_life_btn)
        gen_layout.addStretch()
        
        self.layout.addLayout(gen_layout)
        
        # Кнопки действий
        buttons_layout = QHBoxLayout()
        
        self.add_event_btn = QPushButton("Добавить событие")
        self.remove_event_btn = QPushButton("Удалить событие")
        self.add_sibling_btn = QPushButton("Добавить родственника")
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.add_sibling_btn)
        buttons_layout.addWidget(self.add_event_btn)
        buttons_layout.addWidget(self.remove_event_btn)
        
        self.layout.addLayout(buttons_layout)
    
    def update_styles(self):
        """Обновление стилей"""
        super().update_styles()
        if self.style_provider:
            style = self.style_provider
            for group in self.findChildren(QGroupBox):
                group.setStyleSheet(style.get_group_box_style())
            for edit in self.findChildren(QTextEdit):
                edit.setStyleSheet(style.get_text_edit_style())
            for btn in self.findChildren(QPushButton):
                btn.setStyleSheet(style.get_button_style())
            for combo in self.findChildren(QComboBox):
                combo.setStyleSheet(style.get_combo_box_style())
            self.events_table.setStyleSheet(style.get_table_style())
