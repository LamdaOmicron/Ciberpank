"""
Вкладка оружия персонажа
"""

from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QGroupBox, QPushButton, QHeaderView, QAbstractItemView
)
from .base_tab import BaseTab


class WeaponsTab(BaseTab):
    """Вкладка для управления оружием"""
    
    def __init__(self, parent=None):
        super().__init__(parent, "Оружие")
        self.weapons_data = []
        self._init_ui()
    
    def _init_ui(self):
        """Инициализация UI"""
        # Таблица оружия
        weapons_group = QGroupBox("Вооружение")
        weapons_layout = QVBoxLayout()
        
        self.weapons_table = QTableWidget()
        self.weapons_table.setColumnCount(8)
        self.weapons_table.setHorizontalHeaderLabels([
            "#", "Название", "Тип", "Скрытность", 
            "Доступность", "Урон", "Надежность", "Примечание"
        ])
        
        header = self.weapons_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(7, QHeaderView.Stretch)
        
        self.weapons_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        weapons_layout.addWidget(self.weapons_table)
        weapons_group.setLayout(weapons_layout)
        self.layout.addWidget(weapons_group)
        
        # Кнопки действий
        buttons_layout = QHBoxLayout()
        
        self.add_weapon_btn = QPushButton("Добавить оружие")
        self.remove_weapon_btn = QPushButton("Удалить оружие")
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.add_weapon_btn)
        buttons_layout.addWidget(self.remove_weapon_btn)
        
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
            self.weapons_table.setStyleSheet(style.get_table_style())
