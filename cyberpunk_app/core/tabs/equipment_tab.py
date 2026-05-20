"""
Вкладка экипировки персонажа
"""

from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QGroupBox, QPushButton, QHeaderView, QAbstractItemView
)
from .base_tab import BaseTab


class EquipmentTab(BaseTab):
    """Вкладка для управления экипировкой"""
    
    def __init__(self, parent=None):
        super().__init__(parent, "Экипировка")
        self.equipment_data = []
        self._init_ui()
    
    def _init_ui(self):
        """Инициализация UI"""
        # Таблица экипировки
        equip_group = QGroupBox("Экипировка")
        equip_layout = QVBoxLayout()
        
        self.equipment_table = QTableWidget()
        self.equipment_table.setColumnCount(3)
        self.equipment_table.setHorizontalHeaderLabels(["Название", "Количество", "Описание"])
        
        header = self.equipment_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        self.equipment_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        equip_layout.addWidget(self.equipment_table)
        equip_group.setLayout(equip_layout)
        self.layout.addWidget(equip_group)
        
        # Кнопки действий
        buttons_layout = QHBoxLayout()
        
        self.add_equip_btn = QPushButton("Добавить предмет")
        self.remove_equip_btn = QPushButton("Удалить предмет")
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.add_equip_btn)
        buttons_layout.addWidget(self.remove_equip_btn)
        
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
            self.equipment_table.setStyleSheet(style.get_table_style())
