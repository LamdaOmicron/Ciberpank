"""
Вкладка основной информации персонажа
"""

from PyQt5.QtWidgets import QLabel, QGridLayout, QLineEdit, QGroupBox, QComboBox
from .base_tab import BaseTab


class MainTab(BaseTab):
    """Вкладка с основной информацией о персонаже"""
    
    def __init__(self, parent=None):
        super().__init__(parent, "Основное")
        
        self._init_ui()
    
    def _init_ui(self):
        """Инициализация UI"""
        # Основная информация
        info_group = QGroupBox("Основная информация")
        info_layout = QGridLayout()
        
        self.name_edit = QLineEdit()
        self.role_edit = QLineEdit()
        self.streetdeal_edit = QComboBox()
        
        info_layout.addWidget(QLabel("Имя:"), 0, 0)
        info_layout.addWidget(self.name_edit, 0, 1)
        info_layout.addWidget(QLabel("Роль:"), 1, 0)
        info_layout.addWidget(self.role_edit, 1, 1)
        info_layout.addWidget(QLabel("Streetdeal:"), 2, 0)
        info_layout.addWidget(self.streetdeal_edit, 2, 1)
        
        info_group.setLayout(info_layout)
        self.layout.addWidget(info_group)
        
        # Характеристики
        stats_group = QGroupBox("Характеристики")
        stats_layout = QGridLayout()
        
        self.stat_edits = {}
        stats = ["INT", "REF", "DEX", "TECH", "COOL", "WILL", "LUCK", "MOVE", "BODY", "EMP"]
        
        for i, stat in enumerate(stats):
            row = i // 3
            col = (i % 3) * 2
            label = QLabel(f"{stat}:")
            edit = QLineEdit()
            self.stat_edits[stat.lower()] = edit
            stats_layout.addWidget(label, row, col)
            stats_layout.addWidget(edit, row, col + 1)
        
        stats_group.setLayout(stats_layout)
        self.layout.addWidget(stats_group)
        
        self.layout.addStretch()
    
    def update_styles(self):
        """Обновление стилей"""
        super().update_styles()
        if self.style_provider:
            style = self.style_provider
            for group in self.findChildren(QGroupBox):
                group.setStyleSheet(style.get_group_box_style())
            for edit in self.findChildren(QLineEdit):
                edit.setStyleSheet(style.get_line_edit_style())
            for combo in self.findChildren(QComboBox):
                combo.setStyleSheet(style.get_combo_box_style())
