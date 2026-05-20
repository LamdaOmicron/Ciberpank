"""
Вкладка навыков персонажа
"""

from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QTableWidget, QTableWidgetItem, QGroupBox, QPushButton,
    QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt

from .base_tab import BaseTab


class SkillsTab(BaseTab):
    """Вкладка для управления навыками персонажа"""
    
    def __init__(self, parent=None):
        super().__init__(parent, "Навыки")
        self.skills_data = []
        self._init_ui()
    
    def _init_ui(self):
        """Инициализация UI"""
        # Поиск и фильтры
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("Поиск:"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Введите название навыка...")
        filter_layout.addWidget(self.search_edit)
        
        filter_layout.addWidget(QLabel("Тип:"))
        self.type_filter = QLineEdit()
        self.type_filter.setPlaceholderText("Фильтр по типу...")
        filter_layout.addWidget(self.type_filter)
        
        self.layout.addLayout(filter_layout)
        
        # Таблица навыков
        skills_group = QGroupBox("Навыки")
        skills_layout = QVBoxLayout()
        
        self.skills_table = QTableWidget()
        self.skills_table.setColumnCount(4)
        self.skills_table.setHorizontalHeaderLabels(["Навык", "Значение", "Тип", ""])
        
        header = self.skills_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        self.skills_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.skills_table.setEditTriggers(QAbstractItemView.DoubleClicked)
        
        skills_layout.addWidget(self.skills_table)
        skills_group.setLayout(skills_layout)
        self.layout.addWidget(skills_group)
        
        # Кнопки действий
        buttons_layout = QHBoxLayout()
        
        self.add_skill_btn = QPushButton("Добавить навык")
        self.remove_skill_btn = QPushButton("Удалить навык")
        self.sort_skills_btn = QPushButton("Сортировать")
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.add_skill_btn)
        buttons_layout.addWidget(self.remove_skill_btn)
        buttons_layout.addWidget(self.sort_skills_btn)
        
        self.layout.addLayout(buttons_layout)
    
    def update_styles(self):
        """Обновление стилей"""
        super().update_styles()
        if self.style_provider:
            style = self.style_provider
            for group in self.findChildren(QGroupBox):
                group.setStyleSheet(style.get_group_box_style())
            for edit in self.findChildren(QLineEdit):
                edit.setStyleSheet(style.get_line_edit_style())
            for btn in self.findChildren(QPushButton):
                btn.setStyleSheet(style.get_button_style())
            self.skills_table.setStyleSheet(style.get_table_style())
