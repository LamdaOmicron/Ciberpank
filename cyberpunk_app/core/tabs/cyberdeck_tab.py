"""
Вкладка Cyberdeck для управления кибердекой и программами
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLabel, QLineEdit, QTextEdit, QPushButton, 
    QGroupBox, QTreeWidget, QTreeWidgetItem, QScrollArea
)
from PyQt5.QtCore import Qt

from .base_tab import BaseTab


class CyberdeckTab(BaseTab):
    """
    Вкладка для управления cyberdeck персонажа
    
    Содержит:
    - Характеристики деки
    - Список программ
    - Изображение/описание внешности
    """
    
    def __init__(self, parent=None):
        super().__init__(parent, "Cyberdeck")
        
        # Данные деки
        self.deck_data = {
            "model": "",
            "cpu": "",
            "price": "",
            "data_wall": "",
            "code_gate": "",
            "speed": "",
            "memory": "",
            "options": "",
            "appearance_desc": "",
            "image_path": None
        }
        self.programs = []
        self.total_mu = 0
        
        self._init_ui()
    
    def _init_ui(self):
        """Инициализация UI вкладки"""
        # Основной layout с горизонтальным разделением
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Левая панель - характеристики
        left_panel = self._create_left_panel()
        main_layout.addLayout(left_panel, 1)
        
        # Правая панель - программы
        right_panel = self._create_right_panel()
        main_layout.addLayout(right_panel, 2)
        
        self.layout.addLayout(main_layout)
    
    def _create_left_panel(self):
        """Создает левую панель с характеристиками деки"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Блок характеристик
        specs_group = QGroupBox("Характеристики деки")
        specs_layout = QFormLayout()
        
        self.model_edit = QLineEdit()
        self.cpu_edit = QLineEdit()
        self.price_edit = QLineEdit()
        self.data_wall_edit = QLineEdit()
        self.code_gate_edit = QLineEdit()
        self.speed_edit = QLineEdit()
        self.memory_edit = QLineEdit()
        self.memory_edit.setPlaceholderText("Введите число")
        
        specs_layout.addRow("Модель:", self.model_edit)
        specs_layout.addRow("ЦПУ:", self.cpu_edit)
        specs_layout.addRow("Цена:", self.price_edit)
        specs_layout.addRow("Стена данных:", self.data_wall_edit)
        specs_layout.addRow("Код-ворота:", self.code_gate_edit)
        specs_layout.addRow("Скорость:", self.speed_edit)
        specs_layout.addRow("Память (MU):", self.memory_edit)
        
        # Статус памяти
        self.memory_status = QLabel("Используется: 0 / Доступно: 0")
        self.memory_status.setStyleSheet("color: #ff5555; font-weight: bold;")
        specs_layout.addRow("Статус памяти:", self.memory_status)
        
        specs_group.setLayout(specs_layout)
        layout.addWidget(specs_group)
        
        # Блок опций
        options_group = QGroupBox("Опции")
        options_layout = QVBoxLayout()
        self.options_edit = QTextEdit()
        self.options_edit.setPlaceholderText("Введите дополнительные опции...")
        options_layout.addWidget(self.options_edit)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Блок изображения
        appearance_group = QGroupBox("Внешний вид")
        appearance_layout = QVBoxLayout()
        
        self.image_label = QLabel("Нет изображения")
        self.image_label.setMinimumSize(350, 350)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 5px;
            }
        """)
        
        self.load_image_btn = QPushButton("Загрузить изображение")
        
        appearance_layout.addWidget(self.image_label, 1)
        appearance_layout.addWidget(self.load_image_btn)
        appearance_group.setLayout(appearance_layout)
        layout.addWidget(appearance_group, 1)
        
        return layout
    
    def _create_right_panel(self):
        """Создает правую панель со списком программ"""
        layout = QVBoxLayout()
        
        # Заголовок с кнопками
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Программы"))
        
        self.load_program_btn = QPushButton("Загрузить программу")
        self.remove_program_btn = QPushButton("Удалить программу")
        self.remove_program_btn.setEnabled(False)
        self.prepare_all_btn = QPushButton("Подготовить все")
        self.create_program_btn = QPushButton("Написать программу")
        
        header_layout.addStretch()
        header_layout.addWidget(self.prepare_all_btn)
        header_layout.addWidget(self.remove_program_btn)
        header_layout.addWidget(self.load_program_btn)
        header_layout.addWidget(self.create_program_btn)
        
        layout.addLayout(header_layout)
        
        # Таблица программ
        self.programs_tree = QTreeWidget()
        self.programs_tree.setHeaderLabels([
            "#", "Название", "Сложность", "MU", "Стоимость", "Статус", ""
        ])
        self.programs_tree.setColumnWidth(0, 50)
        
        layout.addWidget(self.programs_tree)
        
        # Детали программы
        details_group = QGroupBox("Детали программы")
        details_layout = QVBoxLayout()
        self.program_details = QTextEdit()
        self.program_details.setReadOnly(True)
        details_layout.addWidget(self.program_details)
        details_group.setLayout(details_layout)
        layout.addWidget(details_group)
        
        return layout
    
    def update_styles(self):
        """Обновляет стили элементов вкладки"""
        super().update_styles()
        
        if self.style_provider:
            style = self.style_provider
            
            # Применяем стили к элементам
            for group in self.findChildren(QGroupBox):
                group.setStyleSheet(style.get_group_box_style())
            
            for edit in self.findChildren(QLineEdit):
                edit.setStyleSheet(style.get_line_edit_style())
            
            for text_edit in self.findChildren(QTextEdit):
                text_edit.setStyleSheet(style.get_text_edit_style())
            
            for btn in self.findChildren(QPushButton):
                btn.setStyleSheet(style.get_button_style())
            
            self.programs_tree.setStyleSheet(style.get_tree_widget_style())
