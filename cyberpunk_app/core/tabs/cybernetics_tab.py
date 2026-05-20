"""
Вкладка кибернетики персонажа
"""

from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QGroupBox, QPushButton, QHeaderView, QAbstractItemView
)
from .base_tab import BaseTab


class CyberneticsTab(BaseTab):
    """Вкладка для управления киберимплантами"""
    
    def __init__(self, parent=None):
        super().__init__(parent, "Кибернетика")
        self.cybernetics_data = []
        self._init_ui()
    
    def _init_ui(self):
        """Инициализация UI"""
        # Таблица имплантов
        cyber_group = QGroupBox("Киберимпланты")
        cyber_layout = QVBoxLayout()
        
        self.cyber_table = QTableWidget()
        self.cyber_table.setColumnCount(4)
        self.cyber_table.setHorizontalHeaderLabels(["Название", "Humanity Loss", "Стоимость", "Описание"])
        
        header = self.cyber_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        
        self.cyber_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        cyber_layout.addWidget(self.cyber_table)
        cyber_group.setLayout(cyber_layout)
        self.layout.addWidget(cyber_group)
        
        # Статистика humanity
        stats_layout = QHBoxLayout()
        stats_layout.addWidget(QLabel("Текущая Humanity:"))
        self.humanity_label = QLabel("0")
        stats_layout.addWidget(self.humanity_label)
        stats_layout.addWidget(QLabel("Потеряно:"))
        self.loss_label = QLabel("0")
        stats_layout.addWidget(self.loss_label)
        stats_layout.addStretch()
        self.layout.addLayout(stats_layout)
        
        # Кнопки действий
        buttons_layout = QHBoxLayout()
        
        self.add_cyber_btn = QPushButton("Добавить имплант")
        self.remove_cyber_btn = QPushButton("Удалить имплант")
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.add_cyber_btn)
        buttons_layout.addWidget(self.remove_cyber_btn)
        
        self.layout.addLayout(buttons_layout)
    
    def update_styles(self):
        """Обновление стилей"""
        super().update_styles()
        if self.style_provider:
            style = self.style_provider
            for group in self.findChildren(QGroupBox):
                group.setStyleSheet(style.get_group_box_style())
            for btn in self.findChildren(QPushButton):
                btn.setStyleSheet(style.get_button_style())
            self.cyber_table.setStyleSheet(style.get_table_style())
