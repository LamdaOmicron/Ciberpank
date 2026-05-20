import os
import sys
import json
import random
import traceback
import logging
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QFileDialog, QMessageBox, QGroupBox, QFrame, QToolTip,
    QCheckBox, QMenuBar, QMenu, QAction, QSizePolicy, QScrollArea, QInputDialog, QStyledItemDelegate,
    QTreeWidget, QTreeWidgetItem, QFormLayout, QStackedWidget
)
from PyQt5.QtGui import (
    QPixmap, QImage, QFont, QPalette, QColor, QIcon, QIntValidator, QPainter, QBrush
)
from PyQt5.QtCore import Qt, QSize, QRect, QEvent, QPoint

# Настройка логирования
logging.basicConfig(
    filename='cyberpunk_sheet.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Декоратор для валидации числовых полей
def validate_int_field(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректное числовое значение")
            return 0
    return wrapper

class ThemeManager:
    """Класс для управления темами приложения"""
    
    @staticmethod
    def get_themes():
        """Возвращает доступные темы"""
        return {
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
            "Коричная/Телесная": {
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
                "bg_color": QColor( 255, 218, 185),  # Персиковый
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

class CustomComboBoxDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        if index.column() == 1:  # Column for weapon type
            editor.addItems([
                "Пистолеты-Пулемёты (ПП)", "Дробовики (ДРБ)", "Винтовки (ВИН)",
                "Тяжелое вооружение (ТЯЖ)", "Оружие Ближнего Боя (ОББ)", 
                "Экзотическое Оружие (ЭКЗ)", "Вести свой вариант"
            ])
        elif index.column() == 3:  # Column for concealment
            editor.addItems([
                "Карманы (Карманы, штанины брюк или рукава)(Kар)",
                "Куртка (Куртка, пальто, оперативная кобура)(Кур)",
                "Длинный (Длинный плащ)(Д)", "Нет (Не может быть спрятано)(H)",
                "Вести свой вариант"
            ])
        elif index.column() == 4:  # Column for availability
            editor.addItems([
                "Отличная (O)", "Доступная (Д)", "Малая (M)", "Редкая (P)", "Вести свой вариант"
            ])
        elif index.column() == 7:  # Column for reliability
            editor.addItems([
                "Очень надёжное (OH)", "Обычное (ОБ)", "Ненадёжный (HH)", "Вести свой вариант"
            ])
        editor.setEditable(True)
        return editor

class SkillTypeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = 3  # 0: Чип, 1: Проф, 2: Доп, 3: Обычный
        self.setFixedSize(80, 25)  # Увеличим размер для текста
        self.setToolTip("Кликните для изменения типа навыка")
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Определяем цвет и текст в зависимости от состояния
        state_data = {
            0: (QColor(0, 255, 0), "Чип"),
            1: (QColor(240, 0, 160), "Проф"),
            2: (QColor(255, 255, 0), "Доп"),
            3: (QColor(255, 255, 255), "Обыч")
        }
        color, text = state_data.get(self.state, (QColor(255, 255, 255), "?"))
        
        # Рисуем прямоугольник с цветом состояния
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 3, 3)
        
        # Рисуем текст
        painter.setPen(QColor(0, 0, 0))  # Черный текст для контраста
        font = QFont("Arial", 8, QFont.Bold)
        painter.setFont(font)
        painter.drawText(QRect(0, 0, self.width(), self.height()), Qt.AlignCenter, text)
        
        # Рисуем границу
        painter.setPen(QColor(100, 100, 100))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(0, 0, self.width()-1, self.height()-1, 3, 3)
    
    def mousePressEvent(self, event):
        # Циклическое переключение состояний
        self.state = (self.state + 1) % 4
        self.update()
        super().mousePressEvent(event)
    
    def get_state(self):
        return self.state
    
    def set_state(self, state):
        self.state = state
        self.update()

class IconComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.custom_option_text = "Вести свой вариант"
        self.icon_path = None
        
    def set_icon(self, icon_path):
        self.icon_path = icon_path
        if icon_path and os.path.exists(icon_path):
            self.setStyleSheet(f"""
                QComboBox::down-arrow {{
                    image: url({icon_path});
                    width: 16px;
                    height: 16px;
                }}
            """)
        
    def showPopup(self):
        # При показе списка, если выбран "Вести свой вариант", скрываем список
        if self.currentText() == self.custom_option_text:
            return
        super().showPopup()

class FlipWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(350, 350)

class CyberdeckTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Основные цвета стиля киберпанк
        self.bg_color = QColor(13, 13, 13)
        self.fg_color = QColor(0, 255, 0)
        self.accent_color = QColor(249, 59, 71)
        self.section_bg = QColor(26, 26, 26)
        self.table_border_color = QColor(69, 206, 162)
        self.table_bg_color = QColor(34, 34, 34)
        self.table_header_bg = self.accent_color
        self.table_header_fg = self.bg_color
        
        # Основные данные
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
        self.icon_cache = {}
        
        self.init_ui()
        self.create_menu()
        self.update_memory_status()
        
    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Левая панель - характеристики деки
        left_panel = QVBoxLayout()
        left_panel.setSpacing(15)
        
        # Блок характеристик
        self.specs_group = QGroupBox("Характеристики деки")  # Сохраняем как атрибут
        self.specs_group.setStyleSheet(self.get_group_box_style())
        specs_layout = QFormLayout()
        
        self.model_edit = QLineEdit()
        self.model_edit.setStyleSheet(self.get_line_edit_style())
        self.cpu_edit = QLineEdit()
        self.cpu_edit.setStyleSheet(self.get_line_edit_style())
        self.price_edit = QLineEdit()
        self.price_edit.setStyleSheet(self.get_line_edit_style())
        self.data_wall_edit = QLineEdit()
        self.data_wall_edit.setStyleSheet(self.get_line_edit_style())
        self.code_gate_edit = QLineEdit()
        self.code_gate_edit.setStyleSheet(self.get_line_edit_style())
        self.speed_edit = QLineEdit()
        self.speed_edit.setStyleSheet(self.get_line_edit_style())
        self.memory_edit = QLineEdit()
        self.memory_edit.setStyleSheet(self.get_line_edit_style())
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
        
        self.specs_group.setLayout(specs_layout)
        left_panel.addWidget(self.specs_group)
        
        # Блок опций
        self.options_group = QGroupBox("Опции")  # Сохраняем как атрибут
        self.options_group.setStyleSheet(self.get_group_box_style())
        options_layout = QVBoxLayout()
        self.options_edit = QTextEdit()
        self.options_edit.setPlaceholderText("Введите дополнительные опции...")
        self.options_edit.setStyleSheet(self.get_text_edit_style())
        options_layout.addWidget(self.options_edit)
        self.options_group.setLayout(options_layout)
        left_panel.addWidget(self.options_group)
        
        # Блок изображения и описания внешности
        self.appearance_group = QGroupBox("Внешний вид")  # Сохраняем как атрибут
        self.appearance_group.setStyleSheet(self.get_group_box_style())
        appearance_layout = QVBoxLayout()
        
        # Создаем переворачивающийся виджет
        self.flip_widget = FlipWidget()
        
        # Лицевая сторона - изображение
        self.image_front = QWidget()
        front_layout = QVBoxLayout(self.image_front)
        
        self.image_label = QLabel()
        self.image_label.setMinimumSize(350, 350)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 5px;
            }
        """)
        self.image_label.setText("Нет изображения\n\n(Нажмите для описания внешности)")
        self.image_label.mousePressEvent = self.flip_card
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.load_image_btn = QPushButton("Загрузить изображение")
        self.load_image_btn.setStyleSheet(self.get_button_style())
        self.load_image_btn.clicked.connect(self.load_image)
        
        front_layout.addWidget(self.image_label, 1)
        front_layout.addWidget(self.load_image_btn)
        
        # Обратная сторона - описание внешности
        self.image_back = QWidget()
        back_layout = QVBoxLayout(self.image_back)
        
        back_label = QLabel("Описание внешности:")
        back_label.setStyleSheet("color: #ff00ff; font-weight: bold;")
        
        self.appearance_desc_edit = QTextEdit()
        self.appearance_desc_edit.setPlaceholderText("Опишите внешний вид вашей кибердеки...")
        self.appearance_desc_edit.setStyleSheet(self.get_text_edit_style())
        
        flip_back_btn = QPushButton("Вернуться к изображению")
        flip_back_btn.setStyleSheet(self.get_button_style())
        flip_back_btn.clicked.connect(self.flip_card)
        
        back_layout.addWidget(back_label)
        back_layout.addWidget(self.appearance_desc_edit, 1)
        back_layout.addWidget(flip_back_btn)
        
        # Добавляем обе стороны в переворачивающийся виджет
        self.flip_widget.addWidget(self.image_front)
        self.flip_widget.addWidget(self.image_back)
        
        appearance_layout.addWidget(self.flip_widget, 1)
        self.appearance_group.setLayout(appearance_layout)
        left_panel.addWidget(self.appearance_group, 1)
        
        # Правая панель - программы
        right_panel = QVBoxLayout()
        
        # Блок управления программами
        programs_header = QHBoxLayout()
        programs_header.addWidget(QLabel("Программы"))
        
        self.load_program_btn = QPushButton("Загрузить программу")
        self.load_program_btn.setStyleSheet(self.get_button_style())
        self.load_program_btn.clicked.connect(self.load_program)
        
        self.remove_program_btn = QPushButton("Удалить программу")
        self.remove_program_btn.setStyleSheet(self.get_button_style())
        self.remove_program_btn.clicked.connect(self.remove_program)
        self.remove_program_btn.setEnabled(False)
        
        self.prepare_all_btn = QPushButton("Подготовить все программы")
        self.prepare_all_btn.setStyleSheet(self.get_button_style())
        self.prepare_all_btn.clicked.connect(self.prepare_all_programs)
        
        # Новая кнопка для создания программы
        self.create_program_btn = QPushButton("Написать программу")
        self.create_program_btn.setStyleSheet(self.get_button_style())
        self.create_program_btn.clicked.connect(self.launch_program_creator)
        programs_header.addStretch()
        programs_header.addWidget(self.prepare_all_btn)
        programs_header.addWidget(self.remove_program_btn)
        programs_header.addWidget(self.load_program_btn)
        programs_header.addWidget(self.create_program_btn)
        right_panel.addLayout(programs_header)
        
        # Таблица программ
        self.programs_tree = QTreeWidget()
        self.programs_tree.setHeaderLabels(["#", "Название", "Сложность", "MU", "Стоимость", "Статус", ""])
        self.programs_tree.setColumnWidth(0, 50)
        self.programs_tree.setColumnWidth(1, 250)
        self.programs_tree.setColumnWidth(2, 100)
        self.programs_tree.setColumnWidth(3, 70)
        self.programs_tree.setColumnWidth(4, 100)
        self.programs_tree.setColumnWidth(5, 150)
        self.programs_tree.setSelectionMode(QAbstractItemView.SingleSelection)
        self.programs_tree.header().setSectionResizeMode(6, QHeaderView.Stretch)
        self.programs_tree.itemClicked.connect(self.on_program_selected)
        self.programs_tree.itemSelectionChanged.connect(self.update_remove_button_state)
        self.programs_tree.setStyleSheet(self.get_tree_widget_style())
        
        right_panel.addWidget(self.programs_tree, 1)
        
        # Блок описания программы
        self.details_group = QGroupBox("Описание программы")  # Сохраняем как атрибут
        self.details_group.setStyleSheet(self.get_group_box_style())
        details_layout = QVBoxLayout()
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setStyleSheet(self.get_text_edit_style())
        details_layout.addWidget(self.details_text)
        self.details_group.setLayout(details_layout)
        right_panel.addWidget(self.details_group)
        
        # Добавляем панели в главный лэйаут
        main_layout.addLayout(left_panel, 40)
        main_layout.addLayout(right_panel, 60)
        
        # Коннекты для сохранения данных
        self.model_edit.textChanged.connect(lambda: self.save_data('model'))
        self.cpu_edit.textChanged.connect(lambda: self.save_data('cpu'))
        self.price_edit.textChanged.connect(lambda: self.save_data('price'))
        self.data_wall_edit.textChanged.connect(lambda: self.save_data('data_wall'))
        self.code_gate_edit.textChanged.connect(lambda: self.save_data('code_gate'))
        self.speed_edit.textChanged.connect(lambda: self.save_data('speed'))
        self.memory_edit.textChanged.connect(self.on_memory_changed)
        self.options_edit.textChanged.connect(lambda: self.save_data('options'))
        self.appearance_desc_edit.textChanged.connect(lambda: self.save_data('appearance_desc'))
    
    def create_menu(self):
        menu_bar = QMenuBar(self)
        # Добавляем менюбар в layout
        layout = self.layout()
        if layout is not None:
            layout.setMenuBar(menu_bar)
    
    def save_data(self, field):
        if field == 'model':
            self.deck_data['model'] = self.model_edit.text()
        elif field == 'cpu':
            self.deck_data['cpu'] = self.cpu_edit.text()
        elif field == 'price':
            self.deck_data['price'] = self.price_edit.text()
        elif field == 'data_wall':
            self.deck_data['data_wall'] = self.data_wall_edit.text()
        elif field == 'code_gate':
            self.deck_data['code_gate'] = self.code_gate_edit.text()
        elif field == 'speed':
            self.deck_data['speed'] = self.speed_edit.text()
        elif field == 'memory':
            self.deck_data['memory'] = self.memory_edit.text()
        elif field == 'options':
            self.deck_data['options'] = self.options_edit.toPlainText()
        elif field == 'appearance_desc':
            self.deck_data['appearance_desc'] = self.appearance_desc_edit.toPlainText()
    
    def on_memory_changed(self):
        self.save_data('memory')
        self.update_memory_status()
    
    def update_memory_status(self):
        try:
            available_memory = int(self.memory_edit.text()) if self.memory_edit.text() else 0
        except ValueError:
            available_memory = 0
            
        used_memory = self.total_mu
        
        # Обновляем статус
        self.memory_status.setText(f"Используется: {used_memory} / Доступно: {available_memory}")
        
        # Меняем цвет в зависимости от загрузки
        if available_memory == 0:
            color = "#ff5555"
        elif used_memory > available_memory:
            color = "#ff0000"
        elif used_memory == available_memory:
            color = "#ffff00"
        else:
            color = "#55ff55"
            
        self.memory_status.setStyleSheet(f"color: {color}; font-weight: bold;")
        
        # Проверяем возможность загрузки программ
        self.load_program_btn.setEnabled(used_memory < available_memory)
    
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Выберите изображение", 
            "", 
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            self.deck_data['image_path'] = file_path
            self.set_deck_image(file_path)
    
    def set_deck_image(self, file_path):
        """Устанавливает изображение деки с уменьшенным размером"""
        if file_path and os.path.exists(file_path):
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                # Уменьшаем изображение до максимального размера 300x300
                pixmap = pixmap.scaled(
                    300, 300,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                
                # Создаем закругленное изображение
                rounded_pixmap = self.create_rounded_pixmap(pixmap, pixmap.width(), pixmap.height())
                self.image_label.setPixmap(rounded_pixmap)
                self.image_label.setText("")
                self.image_label.setAlignment(Qt.AlignCenter)
    
    def create_rounded_pixmap(self, pixmap, width, height):
        """Создает изображение с закругленными углами"""
        if width <= 0 or height <= 0:
            return pixmap
            
        scaled = pixmap.scaled(width, height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        
        result = QPixmap(width, height)
        result.fill(Qt.transparent)
        
        painter = QPainter(result)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        #path = QPainterPath()
        #path.addRoundedRect(0, 0, width, height, 10, 10)
        #painter.setClipPath(path)
        
        painter.drawPixmap(0, 0, scaled)
        
        painter.end()
        return result
    
    def get_program_icon(self, image_path, size=64):
        """Возвращает иконку программы с кэшированием"""
        if not image_path:
            return self.create_default_icon()
        
        # Проверяем кэш
        cache_key = f"{image_path}_{size}"
        if cache_key in self.icon_cache:
            return self.icon_cache[cache_key]
        
        try:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                return self.create_default_icon()
            
            rounded = self.create_rounded_pixmap(pixmap, size, size)
            icon = QIcon(rounded)
            self.icon_cache[cache_key] = icon
            return icon
            
        except Exception:
            return self.create_default_icon()
    
    def create_default_icon(self, size=64):
        """Создает иконку-заглушку"""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.darkGray)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.white)
        painter.setFont(QApplication.font())
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "🖥️")
        painter.end()
        
        rounded = self.create_rounded_pixmap(pixmap, size, size)
        return QIcon(rounded)
    
    def load_program(self):
        # Проверяем доступную память
        try:
            available_memory = int(self.memory_edit.text()) if self.memory_edit.text() else 0
        except ValueError:
            available_memory = 0
            
        if self.total_mu >= available_memory:
            QMessageBox.warning(
                self, 
                "Недостаточно памяти", 
                f"Невозможно загрузить программу! Используется {self.total_mu}MU из {available_memory}MU."
            )
            return
            
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Выберите файл программы", 
            "", 
            "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    program_data = json.load(f)
                
                # Проверяем память для программы
                mu = program_data.get('netrunners_count', 0)
                try:
                    mu = int(mu)
                except (ValueError, TypeError):
                    mu = 0
                
                if self.total_mu + mu > available_memory:
                    QMessageBox.warning(
                        self, 
                        "Недостаточно памяти", 
                        f"Недостаточно памяти для загрузки программы! Требуется: {mu}MU, доступно: {available_memory - self.total_mu}MU."
                    )
                    return
                
                # Добавляем программу
                self.programs.append(program_data)
                self.total_mu += mu
                self.update_memory_status()
                
                # Добавляем в дерево
                item = QTreeWidgetItem(self.programs_tree)
                item.setData(0, Qt.UserRole, len(self.programs) - 1)
                item.setText(0, str(len(self.programs)))
                item.setText(1, program_data.get('program_name', 'Без названия'))
                item.setText(2, str(program_data.get('strength', '?')))
                item.setText(3, str(mu))
                
                # Извлекаем стоимость
                cost = "?"
                result_text = program_data.get('result_text', '')
                for line in result_text.split('\n'):
                    if 'Стоимость:' in line:
                        cost = line.split(':')[1].strip().split()[0]
                        break
                item.setText(4, cost)
                
                # Добавляем кнопку статуса
                status_checkbox = QCheckBox("Готов к использованию")
                status_checkbox.setStyleSheet("""
                    QCheckBox {
                        color: #0f0;
                        background-color: transparent;
                        font-size: 12px;
                        padding: 5px;
                    }
                    QCheckBox::indicator {
                        width: 16px;
                        height: 16px;
                    }
                    QCheckBox::indicator:checked {
                        background-color: #ff5555;
                    }
                """)
                status_checkbox.setChecked(False)
                status_checkbox.stateChanged.connect(lambda state, idx=len(self.programs)-1: self.update_program_status(idx, state))
                self.programs_tree.setItemWidget(item, 5, status_checkbox)
                
                # Устанавливаем иконку
                icon_path = program_data.get('image_path', '')
                icon = self.get_program_icon(icon_path, 64)
                item.setIcon(6, icon)
                item.setText(6, "")
                
                # Выбираем новую программу
                self.programs_tree.setCurrentItem(item)
                
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить программу: {str(e)}")
    
    def update_program_status(self, program_index, state):
        """Обновляет статус программы"""
        if 0 <= program_index < len(self.programs):
            checkbox = self.programs_tree.itemWidget(self.programs_tree.topLevelItem(program_index), 5)
            if state == Qt.Checked:
                checkbox.setText("Использован")
                checkbox.setStyleSheet("""
                    QCheckBox {
                        color: #ff5555;
                        background-color: transparent;
                        font-size: 12px;
                        padding: 5px;
                    }
                    QCheckBox::indicator {
                        width: 16px;
                        height: 16px;
                    }
                    QCheckBox::indicator:checked {
                        background-color: #ff5555;
                    }
                """)
            else:
                checkbox.setText("Готов к использованию")
                checkbox.setStyleSheet("""
                    QCheckBox {
                        color: #0f0;
                        background-color: transparent;
                        font-size: 12px;
                        padding: 5px;
                    }
                    QCheckBox::indicator {
                        width: 16px;
                        height: 16px;
                    }
                    QCheckBox::indicator:checked {
                        background-color: #ff5555;
                    }
                """)
    
    def update_styles(self):
        """Обновляет стили всех элементов вкладки при смене темы"""
        # Обновляем стили групповых элементов
        self.specs_group.setStyleSheet(self.get_group_box_style())
        self.options_group.setStyleSheet(self.get_group_box_style())
        self.appearance_group.setStyleSheet(self.get_group_box_style())
        self.details_group.setStyleSheet(self.get_group_box_style())
        
        # Обновляем стили кнопок
        self.load_image_btn.setStyleSheet(self.get_button_style())
        self.load_program_btn.setStyleSheet(self.get_button_style())
        self.remove_program_btn.setStyleSheet(self.get_button_style())
        self.prepare_all_btn.setStyleSheet(self.get_button_style())
        self.create_program_btn.setStyleSheet(self.get_button_style())
        
        # Обновляем стили текстовых полей
        self.model_edit.setStyleSheet(self.get_line_edit_style())
        self.cpu_edit.setStyleSheet(self.get_line_edit_style())
        self.price_edit.setStyleSheet(self.get_line_edit_style())
        self.data_wall_edit.setStyleSheet(self.get_line_edit_style())
        self.code_gate_edit.setStyleSheet(self.get_line_edit_style())
        self.speed_edit.setStyleSheet(self.get_line_edit_style())
        self.memory_edit.setStyleSheet(self.get_line_edit_style())
        self.options_edit.setStyleSheet(self.get_text_edit_style())
        self.appearance_desc_edit.setStyleSheet(self.get_text_edit_style())
        
        # Обновляем стили таблицы
        self.programs_tree.setStyleSheet(self.get_tree_widget_style())
        
        # Обновляем стиль текстового поля описания
        self.details_text.setStyleSheet(self.get_text_edit_style())
        
        # Обновляем статус памяти
        self.update_memory_status()
    
    def prepare_all_programs(self):
        """Устанавливает все программы в состояние 'Готов к использованию'"""
        for i in range(self.programs_tree.topLevelItemCount()):
            checkbox = self.programs_tree.itemWidget(self.programs_tree.topLevelItem(i), 5)
            if checkbox:
                checkbox.setChecked(False)
                checkbox.setText("Готов к использованию")
                checkbox.setStyleSheet("""
                    QCheckBox {
                        color: #0f0;
                        background-color: transparent;
                        font-size: 12px;
                        padding: 5px;
                    }
                    QCheckBox::indicator {
                        width: 16px;
                        height: 16px;
                    }
                    QCheckBox::indicator:checked {
                        background-color: #ff5555;
                    }
                """)
    
    def on_program_selected(self, item, column):
        program_index = item.data(0, Qt.UserRole)
        if program_index is not None and 0 <= program_index < len(self.programs):
            self.show_program_details(self.programs[program_index])
    
    def show_program_details(self, program_data):
        details = f"<b>Название:</b> {program_data.get('program_name', 'Без названия')}<br>"
        
        # Извлекаем стоимость
        cost = "?"
        result_text = program_data.get('result_text', '')
        for line in result_text.split('\n'):
            if 'Стоимость:' in line:
                cost = line.split(':')[1].strip()
                break
        
        details += f"<b>Стоимость:</b> {cost}<br>"
        details += f"<b>Класс:</b> {', '.join(program_data.get('functions', []))}<br>"
        details += f"<b>Сила:</b> {program_data.get('strength', '?')}<br>"
        details += f"<b>MU:</b> {program_data.get('netrunners_count', '?')}<br>"
        
        # Параметры
        params = program_data.get('parameters', [])
        if params:
            details += "<br><b>Параметры:</b><ul>"
            for param in params:
                details += f"<li>{param.get('name', '')} (+{param.get('value', '')})</li>"
            details += "</ul>"
        
        # Описание
        description = program_data.get('description', '')
        if description:
            details += f"<br><b>Описание:</b><br>{description}"
        
        # Демон
        if program_data.get('is_demon', False):
            details += "<br><br><b>===== СИСТЕМА ДЕМОНА ====</b>"
            details += f"<br>Максимальное количество программ: {program_data.get('max_programs', 5)}"
            loaded = len(program_data.get('loaded_programs', []))
            details += f"<br>Загружено программ: {loaded}/{program_data.get('max_programs', 5)}"
        
        # Изображение программы
        icon_path = program_data.get('image_path', '')
        if icon_path and os.path.exists(icon_path):
            details += f"<br><br><img src='{icon_path}' width='200' />"
        
        self.details_text.setHtml(details)
    
    def update_remove_button_state(self):
        self.remove_program_btn.setEnabled(bool(self.programs_tree.selectedItems()))
    
    def remove_program(self):
        selected_items = self.programs_tree.selectedItems()
        if not selected_items:
            return
            
        item = selected_items[0]
        program_index = item.data(0, Qt.UserRole)
        
        if program_index is None:
            return
            
        # Удаляем программу
        if 0 <= program_index < len(self.programs):
            program_data = self.programs[program_index]
            mu = program_data.get('netrunners_count', 0)
            try:
                mu = int(mu)
            except (ValueError, TypeError):
                mu = 0
            self.total_mu -= mu
            del self.programs[program_index]
            
        # Удаляем из дерева
        self.programs_tree.takeTopLevelItem(self.programs_tree.indexOfTopLevelItem(item))
        
        # Обновляем нумерацию
        for i in range(self.programs_tree.topLevelItemCount()):
            top_item = self.programs_tree.topLevelItem(i)
            top_item.setText(0, str(i + 1))
            top_item.setData(0, Qt.UserRole, i)
        
        # Очищаем детали
        self.details_text.clear()
        self.update_remove_button_state()
        self.update_memory_status()
    
    def save_deck(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить кибердек",
            "",
            "Cyberdeck Files (*.cdk);;All Files (*)"
        )
        
        if not file_path:
            return
            
        if not file_path.lower().endswith('.cdk'):
            file_path += '.cdk'
        
        # Сохраняем статусы программ
        program_statuses = []
        for i in range(self.programs_tree.topLevelItemCount()):
            checkbox = self.programs_tree.itemWidget(self.programs_tree.topLevelItem(i), 5)
            program_statuses.append(checkbox.isChecked() if checkbox else False)
        
        save_data = {
            "deck": self.deck_data,
            "programs": self.programs,
            "program_statuses": program_statuses,
            "total_mu": self.total_mu
        }
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            QMessageBox.information(self, "Сохранено", "Кибердек успешно сохранен!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")
    
    def load_deck(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Загрузить кибердек",
            "",
            "Cyberdeck Files (*.cdk);;All Files (*)"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                load_data = json.load(f)
                
            # Восстанавливаем данные деки
            deck_data = load_data.get('deck', {})
            self.deck_data = deck_data
            
            # Обновляем UI
            self.model_edit.setText(deck_data.get('model', ''))
            self.cpu_edit.setText(deck_data.get('cpu', ''))
            self.price_edit.setText(deck_data.get('price', ''))
            self.data_wall_edit.setText(deck_data.get('data_wall', ''))
            self.code_gate_edit.setText(deck_data.get('code_gate', ''))
            self.speed_edit.setText(deck_data.get('speed', ''))
            self.memory_edit.setText(deck_data.get('memory', ''))
            self.options_edit.setPlainText(deck_data.get('options', ''))
            self.appearance_desc_edit.setPlainText(deck_data.get('appearance_desc', ''))
            
            # Восстанавливаем изображение
            image_path = deck_data.get('image_path')
            self.set_deck_image(image_path)
            
            # Загружаем программы
            self.programs = load_data.get('programs', [])
            self.total_mu = load_data.get('total_mu', 0)
            
            # Очищаем дерево
            self.programs_tree.clear()
            
            # Восстанавливаем статусы программ
            program_statuses = load_data.get('program_statuses', [])
            
            # Добавляем программы
            for i, program_data in enumerate(self.programs):
                item = QTreeWidgetItem(self.programs_tree)
                item.setData(0, Qt.UserRole, i)
                item.setText(0, str(i + 1))
                item.setText(1, program_data.get('program_name', 'Без названия'))
                item.setText(2, str(program_data.get('strength', '?')))
                
                mu = program_data.get('netrunners_count', '?')
                item.setText(3, str(mu))
                
                cost = "?"
                result_text = program_data.get('result_text', '')
                for line in result_text.split('\n'):
                    if 'Стоимость:' in line:
                        cost = line.split(':')[1].strip().split()[0]
                        break
                item.setText(4, cost)
                
                # Добавляем кнопку статуса
                status_checkbox = QCheckBox("Готов к использованию")
                status_checkbox.setStyleSheet("""
                    QCheckBox {
                        color: #0f0;
                        background-color: transparent;
                        font-size: 12px;
                        padding: 5px;
                    }
                    QCheckBox::indicator {
                        width: 16px;
                        height: 16px;
                    }
                    QCheckBox::indicator:checked {
                        background-color: #ff5555;
                    }
                """)
                
                # Восстанавливаем статус
                if i < len(program_statuses) and program_statuses[i]:
                    status_checkbox.setChecked(True)
                    status_checkbox.setText("Использован")
                    status_checkbox.setStyleSheet("""
                        QCheckBox {
                            color: #ff5555;
                            background-color: transparent;
                            font-size: 12px;
                            padding: 5px;
                        }
                        QCheckBox::indicator {
                            width: 16px;
                            height: 16px;
                        }
                        QCheckBox::indicator:checked {
                            background-color: #ff5555;
                        }
                    """)
                
                status_checkbox.stateChanged.connect(lambda state, idx=i: self.update_program_status(idx, state))
                self.programs_tree.setItemWidget(item, 5, status_checkbox)
                
                icon_path = program_data.get('image_path', '')
                icon = self.get_program_icon(icon_path, 64)
                item.setIcon(6, icon)
                item.setText(6, "")
            
            self.update_memory_status()
            QMessageBox.information(self, "Загружено", "Кибердек успешно загружен!")
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл: {str(e)}")
    
    def reset_template(self):
        reply = QMessageBox.question(
            self,
            "Сброс шаблона",
            "Вы уверены, что хотите сбросить все данные? Все несохраненные изменения будут потеряны.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
            
        # Сбрасываем данные
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
        self.icon_cache = {}
        
        # Обновляем UI
        self.model_edit.clear()
        self.cpu_edit.clear()
        self.price_edit.clear()
        self.data_wall_edit.clear()
        self.code_gate_edit.clear()
        self.speed_edit.clear()
        self.memory_edit.clear()
        self.options_edit.clear()
        self.appearance_desc_edit.clear()
        self.programs_tree.clear()
        self.details_text.clear()
        self.image_label.clear()
        self.image_label.setText("Нет изображения\n\n(Нажмите для описания внешности)")
        self.flip_widget.setCurrentIndex(0)  # Возвращаемся к лицевой стороне
        self.update_memory_status()
        
        QMessageBox.information(self, "Шаблон сброшен", "Все поля были сброшены к начальным значениям.")
    
    def show_about(self):
        about_text = """
        <h3>Cyberdeck Constructor 2020</h3>
        <p>Версия 1.2</p>
        <p>Программа для создания кибердеков в стиле Cyberpunk 2020</p>
        <p>© 2023 Ваша компания. Все права защищены.</p>
        <p>Создано с использованием Python и PyQt5</p>
        """
        QMessageBox.about(self, "О программе", about_text)
    
    def flip_card(self, event=None):
        """Переворачивает карточку с изображением на описание и обратно"""
        current_index = self.flip_widget.currentIndex()
        self.flip_widget.setCurrentIndex(1 - current_index)  # Переключаем между 0 и 1
    
    def launch_program_creator(self):
        """Запускает программу создания программ из файла program_creator.py"""
        try:
            # Запускаем файл program_creator.py с помощью интерпретатора Python
            subprocess.Popen([sys.executable, "CyberProgramCreator.py"])
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось запустить программу: {str(e)}")
    
    # Стилизация
    def get_group_box_style(self):
        return f"""
            QGroupBox {{
                background-color: {self.section_bg.name()};
                color: {self.accent_color.name()};
                border: 1px solid {self.accent_color.name()};
                border-radius: 5px;
                margin-top: 1ex;
                font-weight: bold;
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                background-color: {self.section_bg.name()};
                color: {self.accent_color.name()};
            }}
        """
    
    def get_line_edit_style(self):
        return f"""
            QLineEdit {{
                background-color: #333333;
                color: {self.fg_color.name()};
                border: 1px solid #555555;
                padding: 2px;
                font-family: 'Courier New';
            }}
        """
    
    def get_text_edit_style(self):
        return f"""
            QTextEdit {{
                background-color: #333333;
                color: {self.fg_color.name()};
                border: 1px solid #555555;
                font-family: 'Courier New';
            }}
        """
    
    def get_button_style(self):
        return f"""
            QPushButton {{
                background-color: {self.bg_color.name()};
                color: {self.fg_color.name()};
                border: 1px solid {self.accent_color.name()};
                padding: 5px;
                font-weight: bold;
                font-family: 'Courier New';
            }}
            
            QPushButton:hover {{
                background-color: #333333;
            }}
            
            QPushButton:pressed {{
                background-color: #555555;
            }}
        """
    
    def get_tree_widget_style(self):
        return f"""
            QTreeWidget {{
                background-color: {self.table_bg_color.name()};
                color: {self.fg_color.name()};
                gridline-color: {self.table_border_color.name()};
                font-family: 'Courier New';
                font-size: 10pt;
                border: 1px solid {self.table_border_color.name()};
            }}
            
            QHeaderView::section {{
                background-color: {self.table_header_bg.name()};
                color: {self.table_header_fg.name()};
                padding: 4px;
                border: 1px solid {self.table_border_color.name()};
                font-weight: bold;
            }}
            
            QTreeWidget::item {{
                padding: 4px;
            }}
            
            QTreeWidget::item:selected {{
                background-color: #444444;
                color: {self.fg_color.name()};
            }}
        """

class CyberpunkCharacterSheet(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CYBERPUNK 2020 - Character Sheet")
        self.setGeometry(100, 100, 1200, 800)
        
        # Инициализируем атрибуты темы значениями по умолчанию
        self.current_theme = "Стандарт"
        self.init_theme_attributes(self.current_theme)
        
        # Центральный виджет и основной лейаут
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Создаем вкладки
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Переменные для автоматических расчетов
        self.stats_entries = {}
        self.skill_entries = {}
        
        # Инициализация разделов
        self.create_main_section()
        self.create_skills_section()
        self.create_cybernetics_section()
        self.create_weapons_section()
        self.create_equipment_section()
        self.create_lifepath_section()
        self.create_cyberdeck_section() 
        
        # Создаем меню
        self.create_menu()
        
        # Текущий путь к изображению
        self.current_image_path = ""
        
        # Загрузка иконки для комбобоксов
        self.load_combo_icon("combo_icon.png")
        
        # Применяем тему (установит стили для всех элементов)
        self.apply_theme(self.current_theme)
    
    def init_theme_attributes(self, theme_name):
        """Инициализирует атрибуты темы значениями из выбранной темы"""
        themes = ThemeManager.get_themes()
        theme = themes[theme_name]
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
    
    def apply_theme(self, theme_name):
        """Применяет выбранную тему ко всему приложению"""
        themes = ThemeManager.get_themes()
        if theme_name in themes:
            theme = themes[theme_name]
            self.current_theme = theme_name
            
            # Обновляем цвета интерфейса
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
            
            # Применяем новую палитру к приложению
            app = QApplication.instance()
            palette = QPalette()
            palette.setColor(QPalette.Window, self.bg_color)
            palette.setColor(QPalette.WindowText, self.fg_color)
            palette.setColor(QPalette.Base, self.section_bg)
            palette.setColor(QPalette.AlternateBase, self.table_bg_color)
            palette.setColor(QPalette.ToolTipBase, self.fg_color)
            palette.setColor(QPalette.ToolTipText, self.bg_color)
            palette.setColor(QPalette.Text, self.fg_color)
            palette.setColor(QPalette.Button, self.bg_color)
            palette.setColor(QPalette.ButtonText, self.fg_color)
            palette.setColor(QPalette.BrightText, self.accent_color)
            palette.setColor(QPalette.Highlight, self.accent_color)
            palette.setColor(QPalette.HighlightedText, self.table_header_fg)
            app.setPalette(palette)
            
            # Обновляем стили всех элементов интерфейса
            self.update_styles()
    
    def update_styles(self):
        """Обновляет стили всех элементов интерфейса после смены темы"""
        # Обновляем стили главного окна
        self.setStyleSheet(self.get_main_style())
        self.tabs.setStyleSheet(self.get_tab_style())
        
        # Обновляем стили всех вкладок
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if hasattr(tab, 'update_styles'):
                tab.update_styles()
        
        # Обновляем стили меню
        self.menuBar().setStyleSheet(self.get_menu_style())
    
    def create_menu(self):
        menubar = self.menuBar()
        
        # Меню Файл
        file_menu = menubar.addMenu('Файл')
        
        new_action = QAction('Новый персонаж', self)
        new_action.triggered.connect(self.new_character)
        file_menu.addAction(new_action)
        
        save_action = QAction('Сохранить', self)
        save_action.triggered.connect(self.save_character)
        file_menu.addAction(save_action)
        
        load_action = QAction('Загрузить', self)
        load_action.triggered.connect(self.load_character)
        file_menu.addAction(load_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Выход', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Меню Темы
        theme_menu = menubar.addMenu('Темы')
        
        themes = ThemeManager.get_themes()
        for theme_name in themes.keys():
            theme_action = QAction(theme_name, self)
            theme_action.triggered.connect(lambda checked, name=theme_name: self.apply_theme(name))
            theme_menu.addAction(theme_action)
        
        # Меню Помощь
        help_menu = menubar.addMenu('Помощь')
        
        about_action = QAction('О программе', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def get_menu_style(self):
        return f"""
            QMenuBar {{
                background-color: {self.bg_color.name()};
                color: {self.fg_color.name()};
                font-family: 'Courier New';
            }}
            
            QMenuBar::item:selected {{
                background-color: {self.accent_color.name()};
                color: {self.table_header_fg.name()};
            }}
            
            QMenu {{
                background-color: {self.section_bg.name()};
                color: {self.fg_color.name()};
                border: 1px solid {self.accent_color.name()};
            }}
            
            QMenu::item:selected {{
                background-color: {self.accent_color.name()};
                color: {self.table_header_fg.name()};
            }}
        """
    
    def create_cyberdeck_section(self):
        """Создает вкладку кибердека"""
        cyberdeck_tab = CyberdeckTab()
        self.tabs.addTab(cyberdeck_tab, "Кибердека")
    
    def load_combo_icon(self, default_icon_path):
        # Попытка загрузить иконку из файла
        icon_path = default_icon_path
        if not os.path.exists(icon_path):
            # Создаем простую иконку программно, если файл не существует
            pixmap = QPixmap(16, 16)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(QColor(0, 255, 0)))
            painter.setPen(Qt.NoPen)
            painter.drawPolygon([QPoint(0, 4), QPoint(8, 12), QPoint(16, 4)])
            painter.end()
            pixmap.save(icon_path)
        
        # Установка иконки для всех комбобоксов
        self.set_combo_icons(icon_path)
    
    def set_combo_icons(self, icon_path):
        # Установка иконки для всех комбобоксов в интерфейсе
        for widget in self.findChildren(QComboBox):
            if hasattr(widget, 'set_icon'):
                widget.set_icon(icon_path)
    
    def create_menu(self):
        menubar = self.menuBar()
        
        # Меню Файл
        file_menu = menubar.addMenu('Файл')
        
        new_action = QAction('Новый персонаж', self)
        new_action.triggered.connect(self.new_character)
        file_menu.addAction(new_action)
        
        save_action = QAction('Сохранить', self)
        save_action.triggered.connect(self.save_character)
        file_menu.addAction(save_action)
        
        load_action = QAction('Загрузить', self)
        load_action.triggered.connect(self.load_character)
        file_menu.addAction(load_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Выход', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        theme_menu = menubar.addMenu('Темы')
        themes = ThemeManager.get_themes()
        for theme_name in themes.keys():
            theme_action = QAction(theme_name, self)
            theme_action.triggered.connect(lambda checked, name=theme_name: self.apply_theme(name))
            theme_menu.addAction(theme_action)
        
        # Меню Помощь
        help_menu = menubar.addMenu('Помощь')
        
        about_action = QAction('О программе', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def new_character(self):
        # Сброс всех полей
        for key in self.stats_entries:
            self.stats_entries[key].setText('0')
            
        # Сброс модификаторов
        for key in self.mod_entries:
            self.mod_entries[key].setText('0')
        
        self.char_name.setText('')
        self.role.setCurrentIndex(-1)
        self.eurodollar.setText('0')  # Сброс евродолларов
        
        # Сброс флажков урона
        self.set_damage_checkboxes(0)
        
        # Сброс таблиц
        self.cyber_table.setRowCount(0)
        self.weapons_table.setRowCount(0)
        self.equip_table.setRowCount(0)
        self.events_table.setRowCount(0)
        self.siblings_table.setRowCount(0)
        
        # Сброс изображения
        self.char_image.setPixmap(QPixmap())
        self.current_image_path = ""
        
        # Обновление расчетов
        self.update_derived_stats()
        
        # Сброс брони
        for part in self.armor_entries:
            self.armor_entries[part].setText('0')
        
        # Сброс типов навыков
        for skill_data in self.skill_entries.values():
            skill_data['type_widget'].set_state(3)  # Обычный
        
        QMessageBox.information(self, "Новый персонаж", "Создан новый лист персонажа")
    
    def save_character(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Сохранить персонажа", "", "Cyberpunk Character (*.cpc);;Все файлы (*)"
            )
            
            if not file_path:
                return
            
            if not file_path.endswith('.cpc'):
                file_path += '.cpc'
                
            character_data = {
                "name": self.char_name.text(),
                "role": self.role.currentText(),
                "eurodollar": self.eurodollar.text(),
                "damage": self.get_current_damage(),  # Сохранение текущего урона (количество флажков)
                "stats": {key: entry.text() for key, entry in self.stats_entries.items()},
                "mods": {key: entry.text() for key, entry in self.mod_entries.items()},
                "skills": self.get_skills_data(),
                "cybernetics": self.get_table_data(self.cyber_table),
                "weapons": self.get_table_data(self.weapons_table),
                "equipment": self.get_table_data(self.equip_table),
                "armor": {part: entry.text() for part, entry in self.armor_entries.items()},
                "lifepath": self.get_lifepath_data(),
                "image_path": self.current_image_path
            }
            
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(character_data, f, indent=2, ensure_ascii=False)
                QMessageBox.information(self, "Сохранение", f"Персонаж сохранен в {file_path}")
            except OSError as e:
                QMessageBox.critical(self, "Ошибка файла", f"Ошибка записи: {e}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить персонажа: {e}")
                logging.exception("Save error")
        except Exception as e:
            QMessageBox.critical(self, "Критическая ошибка", f"Ошибка при сохранении: {e}")
            logging.exception("Critical save error")
    
    def load_character(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Загрузить персонажа", "", "Cyberpunk Character (*.cpc);;Все файлы (*)"
            )
            
            if not file_path:
                return
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    character_data = json.load(f)
                
                # Блокируем сигналы для предотвращения множественных обновлений
                self.block_signals(True)
                
                # Загрузка основных данных
                self.char_name.setText(character_data.get('name', ''))
                role_text = character_data.get('role', '')
                role_index = self.role.findText(role_text)
                self.role.setCurrentIndex(role_index if role_index >= 0 else -1)
                
                # Загрузка евродолларов
                self.eurodollar.setText(character_data.get('eurodollar', '0'))
                
                # Загрузка урона и установка флажков
                damage = character_data.get('damage', 0)
                self.set_damage_checkboxes(damage)
                
                # Загрузка характеристик
                stats = character_data.get('stats', {})
                for key, entry in self.stats_entries.items():
                    value = stats.get(key, '0')
                    if value is None:
                        value = '0'
                    entry.setText(str(value))
                
                # Загрузка модификаторов
                mods = character_data.get('mods', {})
                for key, entry in self.mod_entries.items():
                    value = mods.get(key, '0')
                    if value is None:
                        value = '0'
                    entry.setText(str(value))
                
                # Загрузка навыков
                self.set_skills_data(character_data.get('skills', {}))
                
                # Загрузка табличных данных
                self.set_table_data(self.cyber_table, character_data.get('cybernetics', []))
                self.set_table_data(self.weapons_table, character_data.get('weapons', []))
                self.set_table_data(self.equip_table, character_data.get('equipment', []))
                
                # Загрузка брони
                armor_data = character_data.get('armor', {})
                for part, entry in self.armor_entries.items():
                    value = armor_data.get(part, '0')
                    entry.setText(str(value))
                
                # Загрузка жизненного пути
                self.set_lifepath_data(character_data.get('lifepath', {}))
                
                # Загрузка изображения
                image_path = character_data.get('image_path', '')
                if image_path and os.path.exists(image_path):
                    self.current_image_path = image_path
                    self.load_image_from_path(image_path)
                else:
                    self.current_image_path = ""
                
                # Разблокируем сигналы
                self.block_signals(False)
                
                # Обновление расчетов
                self.update_derived_stats()
                
                QMessageBox.information(self, "Загрузка", f"Персонаж загружен из {file_path}")
            except OSError as e:
                QMessageBox.critical(self, "Ошибка файла", f"Ошибка чтения: {e}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить персонажа: {e}")
                logging.exception("Load error")
        except Exception as e:
            QMessageBox.critical(self, "Критическая ошибка", f"Ошибка при загрузке: {e}")
            logging.exception("Critical load error")
    
    def block_signals(self, block):
        """Блокирует/разблокирует сигналы для предотвращения множественных обновлений"""
        # Блокировка сигналов характеристик
        for entry in self.stats_entries.values():
            entry.blockSignals(block)
        
        # Блокировка сигналов модификаторов
        for entry in self.mod_entries.values():
            entry.blockSignals(block)
        
        # Блокировка сигналов навыков
        for skill_data in self.skill_entries.values():
            skill_data['value'].blockSignals(block)
        
        # Блокировка сигнала флажков урона
        for checkbox in self.wound_checkboxes:
            checkbox.blockSignals(block)
    
    def get_skills_data(self):
        skills_data = {}
        for skill, data in self.skill_entries.items():
            skills_data[skill] = {
                "value": data['value'].text(),
                "skill_type": data['type_widget'].get_state(),
                "role": data.get('role', False)  # Для совместимости со старым формойтом
            }
        return skills_data
    
    def set_skills_data(self, skills_data):
        if not skills_data:
            return
            
        for skill, data in skills_data.items():
            if skill in self.skill_entries:
                # Значение навыка
                value = data.get('value', '0')
                if value is None:
                    value = '0'
                self.skill_entries[skill]['value'].setText(str(value))
                
                # Тип навыка
                if 'skill_type' in data:
                    # Новый формат
                    skill_type = data.get('skill_type', 3)
                    self.skill_entries[skill]['type_widget'].set_state(skill_type)
                else:
                    # Старый формат (для совместимости)
                    chip = data.get('chipped', False)
                    role = data.get('role', False)
                    if chip:
                        self.skill_entries[skill]['type_widget'].set_state(0)
                    elif role:
                        self.skill_entries[skill]['type_widget'].set_state(1)
                    else:
                        self.skill_entries[skill]['type_widget'].set_state(3)
    
    def get_table_data(self, table):
        data = []
        for row in range(table.rowCount()):
            row_data = []
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)
        return data
    
    def set_table_data(self, table, data):
        if not data:
            return
            
        table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                if value is None:
                    value = ""
                table.setItem(row, col, QTableWidgetItem(str(value)))
    
    def get_lifepath_data(self):
        return {
            "name": self.lp_name.text(),
            "gender": self.lp_gender.currentText(),
            "age": self.lp_age.text(),
            "birthplace": self.lp_birthplace.text(),
            "language": self.lp_language.text(),
            "clothes": self.lp_clothes.text(),
            "hairstyle": self.lp_hairstyle.text(),
            "feature": self.lp_feature.text(),
            "origin": self.lp_origin.currentText(),
            "trait": self.lp_trait.text(),
            "personality": self.lp_personality.text(),
            "values": self.lp_values.text(),
            "attitude": self.lp_attitude.text(),
            "item": self.lp_item.text(),
            "dream": self.lp_dream.text(),
            "phobias": self.lp_phobias.text(),
            "history": self.lp_history.toPlainText(),
            "events": self.get_table_data(self.events_table),
            "family_rating": self.family_rating.currentText(),
            "parent_status": self.parent_status.currentText(),
            "family_tragedy": self.family_tragedy.currentText(),
            "childhood_place": self.childhood_place.currentText(),
            "siblings": self.get_table_data(self.siblings_table)
        }
    
    def set_lifepath_data(self, data):
        if not data:
            return
            
        self.lp_name.setText(data.get('name', ''))
        
        # Загрузка пола
        gender_text = data.get('gender', '')
        if gender_text:
            gender_index = self.lp_gender.findText(gender_text)
            self.lp_gender.setCurrentIndex(gender_index if gender_index >= 0 else 0)
            
        self.lp_age.setText(data.get('age', ''))
        self.lp_birthplace.setText(data.get('birthplace', ''))
        self.lp_language.setText(data.get('language', ''))
        self.lp_clothes.setText(data.get('clothes', ''))
        self.lp_hairstyle.setText(data.get('hairstyle', ''))
        self.lp_feature.setText(data.get('feature', ''))
        
        # Загрузка модных течений
        origin_text = data.get('origin', '')
        if origin_text:
            origin_index = self.lp_origin.findText(origin_text)
            self.lp_origin.setCurrentIndex(origin_index if origin_index >= 0 else 0)
            
        self.lp_trait.setText(data.get('trait', ''))
        self.lp_personality.setText(data.get('personality', ''))
        self.lp_values.setText(data.get('values', ''))
        self.lp_attitude.setText(data.get('attitude', ''))
        self.lp_item.setText(data.get('item', ''))
        self.lp_dream.setText(data.get('dream', ''))
        self.lp_phobias.setText(data.get('phobias', ''))
        self.lp_history.setPlainText(data.get('history', ''))
        
        # Загрузка событий с сортировкой по годам
        events = data.get('events', [])
        if events:
            # Сортировка событий по году (первый столбец)
            try:
                events.sort(key=lambda x: int(x[0]) if x[0] else 0)
            except:
                pass
        self.set_table_data(self.events_table, events)
        
        # Загрузка семейных данных
        family_rating_text = data.get('family_rating', '')
        if family_rating_text:
            index = self.family_rating.findText(family_rating_text)
            self.family_rating.setCurrentIndex(index if index >= 0 else 0)
            
        parent_status_text = data.get('parent_status', '')
        if parent_status_text:
            index = self.parent_status.findText(parent_status_text)
            self.parent_status.setCurrentIndex(index if index >= 0 else 0)
            
        family_tragedy_text = data.get('family_tragedy', '')
        if family_tragedy_text:
            index = self.family_tragedy.findText(family_tragedy_text)
            self.family_tragedy.setCurrentIndex(index if index >= 0 else 0)
            
        childhood_place_text = data.get('childhood_place', '')
        if childhood_place_text:
            index = self.childhood_place.findText(childhood_place_text)
            self.childhood_place.setCurrentIndex(index if index >= 0 else 0)
        
        siblings = data.get('siblings', [])
        self.set_table_data(self.siblings_table, siblings)
    
    def show_about(self):
        about_text = (
            "CYBERPUNK 2020 Character Sheet\n"
            "Версия 0.11\n\n"
            "Интерактивный лист персонажа для настольной ролевой игры Cyberpunk 2020\n"
            "Разработано с использованием Python и PyQt5\n\n"
            "© 2023 Cyberpunk RPG Tools"
        )
        QMessageBox.about(self, "О программе", about_text)
    
    @validate_int_field
    def get_stat_value(self, key):
        """Получает числовое значение характеристики с обработкой ошибки"""
        return int(self.stats_entries[key].text() or 0)
    
    @validate_int_field
    def calculate_total_humanity_loss(self):
        """Вычисляет общую потерю человечности из кибернетики"""
        total = 0
        for row in range(self.cyber_table.rowCount()):
            item = self.cyber_table.item(row, 2)  # Колонка потери человечности
            if item and item.text().strip():
                total += int(item.text())
        return total
    
    def update_derived_stats(self):
        try:
            # Получаем основные значения
            body_val = self.get_stat_value('body')
            emp_val = self.get_stat_value('emp')
            move_val = self.get_stat_value('move')
            
            # Рассчитываем производные характеристики
            run_val = move_val * 3
            jump_val = run_val * 4
            carry_val = body_val * 10
            lift_val = body_val * 40
            humanity_val = emp_val * 10 - self.calculate_total_humanity_loss()
            save_val = body_val
            
            # Определяем MТЕЛ
            if body_val <= 2:
                mbody_val = "0 (Очень Слабый)"
            elif 3 <= body_val <= 4:
                mbody_val = "1 (Слабый)"
            elif 5 <= body_val <= 7:
                mbody_val = "2 (Средний)"
            elif 8 <= body_val <= 9:
                mbody_val = "3 (Сильный)"
            elif body_val == 10:
                mbody_val = "4 (Очень Сильный)"
            else:
                mbody_val = "5+ (Суперчеловек)"
            
            # Обновляем метки
            self.derived_labels['run'].setText(str(run_val))
            self.derived_labels['jump'].setText(str(jump_val))
            self.derived_labels['carry'].setText(str(carry_val))
            self.derived_labels['lift'].setText(str(lift_val))
            self.derived_labels['humanity'].setText(str(humanity_val))
            self.derived_labels['save'].setText(str(save_val))
            self.derived_labels['mbody'].setText(mbody_val)
            
            # Обновляем проверки здоровья
            self.update_health_checks()
            
        except Exception as e:
            logging.error(f"Error in update_derived_stats: {e}")
    
    def get_current_damage(self):
        """Возвращает текущий урон (количество отмеченных флажков)"""
        return sum(1 for checkbox in self.wound_checkboxes if checkbox.isChecked())

    def set_damage_checkboxes(self, damage):
        """Устанавливает флажки в соответствии с полученным уроном"""
        # Снимаем все флажки
        for checkbox in self.wound_checkboxes:
            checkbox.setChecked(False)
        # Устанавливаем флажки в соответствии с уроном
        for i in range(min(damage, 40)):
            self.wound_checkboxes[i].setChecked(True)
        
    def update_health_checks(self):
        """Обновляет проверки здоровья на основе текущего урона и СПБ"""
        try:
            # Получаем базовый СПБ
            base_save = int(self.derived_labels['save'].text() or 0)
            
            # Получаем текущий урон (количество отмеченных флажков)
            damage = self.get_current_damage()
            
            # Обновляем метку текущего урона
            self.current_damage_label.setText(str(damage))
            
            # Рассчитываем СПБ для стана
            stun_mod = max(0, (damage // 4) - 1)
            stun_save = base_save - stun_mod
            
            # Рассчитываем СПБ для смерти
            death_mod = max(0, ((damage - 12) // 4) - 1)
            death_save = base_save - death_mod
            
            # Обновляем метки
            self.stun_save_label.setText(str(stun_save))
            self.death_save_label.setText(str(death_save))
            
            # Устанавливаем цвет для СПБ (стан) в зависимости от значения
            if stun_save <= 0:
                stun_color = self.red_color
            elif 1 <= stun_save <= 4:
                stun_color = self.yellow_color
            else:  # 5 и выше
                stun_color = self.green_color
            self.stun_save_label.setStyleSheet(f"color: {stun_color}; font-weight: bold;")
            
            # Устанавливаем цвет для СПБ (смерть) в зависимости от значения
            if death_save <= 0:
                death_color = self.red_color
            elif 1 <= death_save <= 4:
                death_color = self.yellow_color
            else:
                death_color = self.green_color
            self.death_save_label.setStyleSheet(f"color: {death_color}; font-weight: bold;")
                
        except Exception as e:
            logging.error(f"Error in update_health_checks: {e}")
    
    def create_main_section(self):
        main_tab = QWidget()
        layout = QHBoxLayout(main_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # Левый столбец - изображение и основная информация
        left_frame = QGroupBox("Основная информация")
        left_frame.setStyleSheet(self.get_group_box_style())
        left_layout = QVBoxLayout(left_frame)
        
        # Изображение персонажа
        self.char_image = QLabel()
        self.char_image.setAlignment(Qt.AlignCenter)
        self.char_image.setMinimumSize(200, 300)
        self.char_image.setStyleSheet("""
            background-color: #333333;
            border: 1px solid #7fffd4;
        """)
        left_layout.addWidget(self.char_image)
        
        # Кнопка загрузки изображения
        load_btn = QPushButton("Загрузить изображение")
        load_btn.setStyleSheet(self.get_button_style())
        load_btn.clicked.connect(self.load_image)
        left_layout.addWidget(load_btn)
        
        # Основные поля
        info_group = QGroupBox("Персонаж")
        info_group.setStyleSheet(self.get_group_box_style())
        info_layout = QGridLayout(info_group)
        
        row = 0
        
        # Имя персонажа
        info_layout.addWidget(QLabel("Имя персонажа:"), row, 0)
        self.char_name = QLineEdit()
        self.char_name.setStyleSheet(self.get_line_edit_style())
        info_layout.addWidget(self.char_name, row, 1)
        row += 1
        
        # Роль
        info_layout.addWidget(QLabel("Роль:"), row, 0)
        self.role = IconComboBox()
        self.role.setStyleSheet(self.get_combo_box_style())
        self.role.addItems([
            'Соло', 'Нетранер', 'Техник', 'Мед-Техник', 'Медиа', 
            'Фиксер', 'Номад', 'Коп', 'Корпорат', 'Рокер'
        ])
        info_layout.addWidget(self.role, row, 1)
        row += 1
        
        # Евродолар
        info_layout.addWidget(QLabel("Евродолар:"), row, 0)
        self.eurodollar = QLineEdit("0")
        self.eurodollar.setValidator(QIntValidator(0, 10000000))
        self.eurodollar.setStyleSheet(self.get_line_edit_style())
        self.eurodollar.setToolTip("Финансовое состояние персонажа")
        info_layout.addWidget(self.eurodollar, row, 1)
        
        left_layout.addWidget(info_group)
        layout.addWidget(left_frame)
        
        # Правый столбец - характеристики
        right_frame = QWidget()
        right_layout = QVBoxLayout(right_frame)
        right_layout.setSpacing(15)
        

        # Основные характеристики
        stats_group = QGroupBox("ОСНОВНЫЕ ХАРАКТЕРИСТИКИ")
        stats_group.setStyleSheet(self.get_group_box_style())
        stats_layout = QGridLayout(stats_group)
        
        stats = [
            ('Интеллект (INT)', 'int', "Определяет умственные способности и аналитические навыки"),
            ('Рефлексы (REF)', 'ref', "Влияет на скорость реакции и ловкость"),
            ('Техника (TECH)', 'tech', "Определяет технические навыки и способность работать с механизмами"),
            ('Хладнокровие (COOL)', 'cool', "Влияет на самообладание и устойчивость к стрессу"),
            ('Привлекательность (ATT)', 'att', "Определяет внешнюю привлекательность и харизму"),
            ('Удача (LUCK)', 'luck', "Влияет на случайные события и шансы на успех"),
            ('Передвижение (ПЕР)', 'move', "Определяет скорость передвижения и маневренность"),
            ('Телосложение (BODY)', 'body', "Влияет на здоровье, силу и выносливость"),
            ('Эмпатия (EMP)', 'emp', "Определяет способность понимать других и потерю человечности"),
            ('Репутация (REP)', 'rep', "Влияет на социальное положение и авторитет")
        ]
        
        self.stats_entries = {}
        self.mod_entries = {}  # Новый словарь для модификаторов
        
        for i, (label, key, tooltip) in enumerate(stats):
            # Метка характеристики
            stats_layout.addWidget(QLabel(label), i, 0)
            
            # Поле для базового значения
            entry = QLineEdit("0")
            entry.setValidator(QIntValidator(0, 10))
            entry.setStyleSheet(self.get_line_edit_style())
            entry.setMaximumWidth(50)
            entry.textChanged.connect(self.update_derived_stats)
            stats_layout.addWidget(entry, i, 1)
            self.stats_entries[key] = entry
            entry.setToolTip(tooltip)
            
            # Разделитель "/"
            separator = QLabel("/")
            separator.setAlignment(Qt.AlignCenter)
            separator.setStyleSheet("color: #00ff00; font-weight: bold;")
            separator.setMaximumWidth(10)
            stats_layout.addWidget(separator, i, 2)
            
            # Поле для модификатора
            mod_entry = QLineEdit("0")
            mod_entry.setValidator(QIntValidator(-10, 10))
            mod_entry.setStyleSheet("""
                QLineEdit {
                    background-color: #333333;
                    color: #00ffff;  # Другой цвет для модификаторов
                    border: 1px solid #555555;
                    padding: 2px;
                    font-family: 'Courier New';
                }
            """)
            mod_entry.setMaximumWidth(50)
            mod_entry.textChanged.connect(self.update_derived_stats)
            stats_layout.addWidget(mod_entry, i, 3)
            self.mod_entries[key] = mod_entry
            mod_entry.setToolTip(f"Модификатор для {label}")
        
        right_layout.addWidget(stats_group)
        
        # Автоматически вычисляемые характеристики
        derived_group = QGroupBox("ВЫЧИСЛЯЕМЫЕ ХАРАКТЕРИСТИКИ")
        derived_group.setStyleSheet(self.get_group_box_style())
        derived_layout = QGridLayout(derived_group)
        
        derived_stats = [
            ('Бег (ПЕР*3)', 'run'),
            ('Прыжок (Бег*4)', 'jump'),
            ('Перенести (ТЕЛ*10)', 'carry'),
            ('Поднять (ТЕЛ*40)', 'lift'),
            ('Человечность (ЭМП*10 - потеря)', 'humanity'),
            ('СПАС (ТЕЛ)', 'save'),
            ('МТЕЛ (ТЕЛ)', 'mbody')
        ]
        
        self.derived_labels = {}
        for i, (label, key) in enumerate(derived_stats):
            derived_layout.addWidget(QLabel(label), i, 0)
            value_label = QLabel("0")
            value_label.setStyleSheet("color: #00ff00; font-weight: bold;")
            derived_layout.addWidget(value_label, i, 1)
            self.derived_labels[key] = value_label
        
        right_layout.addWidget(derived_group)
        
        # Здоровье и проверки
        health_group = QGroupBox("ЗДОРОВЬЕ И ПРОВЕРКИ")
        health_group.setStyleSheet(self.get_group_box_style())
        health_layout = QGridLayout(health_group)
        
        # Область для флажков урона с подписями справа
        wounds_frame = QFrame()
        wounds_frame.setStyleSheet("background-color: #1a1a1a; padding: 2px;")
        wounds_layout = QGridLayout(wounds_frame)
        wounds_layout.setHorizontalSpacing(2)  # Минимальное расстояние между флажками
        wounds_layout.setVerticalSpacing(2)
        
        # Создаем 40 флажков (10 рядов по 4) с подписями справа
        self.wound_checkboxes = []
        damage_types = [
            "Лёгкие",
            "Тяжёлые",
            "Критические",
            "Смертельные 0",
            "Смертельные 1",
            "Смертельные 2",
            "Смертельные 3",
            "Смертельные 4",
            "Смертельные 5",
            "Смертельные 6"
        ]
        
        for i in range(10):
            # Добавляем подпись типа урона слева
            damage_label = QLabel(damage_types[i])
            damage_label.setStyleSheet("color: #ffffff; font-weight: bold;")
            damage_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            wounds_layout.addWidget(damage_label, i, 0)
            
            # Добавляем 4 флажка с минимальным расстоянием между ними
            for j in range(4):
                checkbox = QCheckBox()
                checkbox.setStyleSheet("""
                    QCheckBox {
                        spacing: 0px;
                        padding: 0px;
                        margin: 0px;
                    }
                    QCheckBox::indicator {
                        width: 15px;
                        height: 15px;
                    }
                    QCheckBox::indicator:unchecked {
                        border: 1px solid #555555;
                        background-color: #333333;
                    }
                    QCheckBox::indicator:checked {
                        background-color: #ff0000;
                        border: 1px solid #ff0000;
                    }
                """)
                checkbox.stateChanged.connect(self.update_health_checks)
                wounds_layout.addWidget(checkbox, i, j + 1)
                self.wound_checkboxes.append(checkbox)
            
            # Добавляем подпись "Стан X" справа
            stun_label = QLabel(f"Стан {i}")
            stun_label.setStyleSheet("color: #00ff00; font-weight: bold;")
            stun_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            wounds_layout.addWidget(stun_label, i, 5)
        
        # Настраиваем пропорции колонок для автоматического подстраивания
        wounds_layout.setColumnStretch(0, 2)  # Подписи слева
        wounds_layout.setColumnStretch(1, 1)  # Флажки
        wounds_layout.setColumnStretch(2, 1)  # Флажки
        wounds_layout.setColumnStretch(3, 1)  # Флажки
        wounds_layout.setColumnStretch(4, 1)  # Флажки
        wounds_layout.setColumnStretch(5, 1)  # Подписи справа
        
        health_layout.addWidget(QLabel("Раны (каждая клетка = 1 урона):"), 0, 0)
        health_layout.addWidget(wounds_frame, 1, 0, 1, 2)
        right_layout.addWidget(health_group)
        
        # Броня по зонам
        armor_group = QGroupBox("БРОНЯ ПО ЗОНАМ")
        armor_group.setStyleSheet(self.get_group_box_style())
        armor_layout = QGridLayout(armor_group)
        
        body_parts = ['Голова', 'Торс', 'Правая рука', 'Левая рука', 'Правая нога', 'Левая нога']
        self.armor_entries = {}
        
        armor_layout.addWidget(QLabel("Часть тела"), 0, 0)
        armor_layout.addWidget(QLabel("Броня"), 0, 1)
        
        for i, part in enumerate(body_parts):
            armor_layout.addWidget(QLabel(part), i+1, 0)
            
            armor_entry = QLineEdit()
            armor_entry.setValidator(QIntValidator(0, 100))
            armor_entry.setStyleSheet(self.get_line_edit_style())
            armor_entry.setMaximumWidth(50)
            armor_layout.addWidget(armor_entry, i+1, 1)
            self.armor_entries[part] = armor_entry
        
        right_layout.addWidget(armor_group)
        
        # Добавляем правый столбец в основной лейаут
        layout.addWidget(right_frame)
        
        # Добавляем вкладку
        self.tabs.addTab(main_tab, "Основные характеристики")
    
    def create_skills_section(self):
        skills_tab = QWidget()
        layout = QVBoxLayout(skills_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Панель инструментов для навыков
        tools_frame = QFrame()
        tools_layout = QHBoxLayout(tools_frame)
        
        # Поле для поиска навыков
        search_label = QLabel("Поиск навыков:")
        search_label.setStyleSheet("color: #00ff00;")
        tools_layout.addWidget(search_label)
        
        self.skill_search = QLineEdit()
        self.skill_search.setStyleSheet(self.get_line_edit_style())
        self.skill_search.setPlaceholderText("Введите название навыка...")
        self.skill_search.textChanged.connect(self.filter_skills)
        tools_layout.addWidget(self.skill_search)
        
        # Выбор типа для фильтрации
        type_label = QLabel("Тип:")
        type_label.setStyleSheet("color: #00ff00;")
        tools_layout.addWidget(type_label)
        
        self.type_filter = IconComboBox()
        self.type_filter.setStyleSheet(self.get_combo_box_style())
        self.type_filter.addItems(["Все", "Чип", "Проф", "Доп", "Обыч"])
        self.type_filter.currentTextChanged.connect(self.filter_skills_by_type)
        tools_layout.addWidget(self.type_filter)
        layout.addWidget(tools_frame)
        
        # Реальные категории навыков Cyberpunk 2020
        skill_categories = {
            'Спецвозможности': ['Авторитет (Коп)', 'Харизма (Рокербой)', 'Чувство Боя (Соло)', 'Достоверность (Медиа)', 'Семья (Номад)',
                                'Интерфейс (Нетраннер)', 'Импровизированный Ремонт (Техник)', 'Медицинский Техник (Медтехник)', 'Ресурсы (Корпорат)', 'Уличная сделки (Фиксер)'],
            'Привлекательность': ['Уход за собой', 'Гардероб и стиль'],
            'Телосложение': ['Выносливость', 'Силовая подготовка', 'Плавание'],
            'Хладнокровие': ['Допрос', 'Запугивание', 'Ораторское искусство', 'Сопротивление(Пыткам/Наркотикам)', 'Знание улиц'],
            'Эмпатия': ['Понимание людей', 'Интервью', 'Лидерство', 'Соблазнение', 'Социальность', 'Убеждение и забалтывание', 'Выступление'],
            'Интеллект': ['Учёт', 'Антропология', 'Осведомлённость/Наблюдательность', 'Биология ', 'Ботаника', 'Химия ', 'Сочинение',
                          'Диагностика болезней', 'Образование и общие знания', 'Эксперт', 'Азартные игры', 'Геология', 'Скрываться/Избегать',
                          'История', 'Знание Языка', 'Поиск Информации', 'Математика', 'Физика', 'Программирование', 'Скрытное Наблюдение', 'Фондовый Рынок',
                          'Системные знания', 'Преподавание', 'Выживание в дикой местности', 'Зоология'],
            'Рефлексы': ['Стрельба из лука', 'Легкая атлетика', 'Драка', 'Танцы', 'Уклонение и Избегание', 'Вождение', 'Фехтование',
                          'Пистолеты', 'Тяжёлое вооружение', 'Мотоциклы', 'Управление тяжёлой техникой', 'Пилот (Вертолёты)[3]', 'Пилот (Неподвижное Крыло)[2]',
                          'Пилот (Дирижабль)[2]', 'Пилот (Транспорта с векторными двигателями)[3]', 'Винтовки', 'Скрытность[2]', 'Пистолеты-Пулеметы'],
            'Технические': ['Авиатехника[2]', 'Технологии AV[3]', 'Базовые технологии[2]', 'Эксплуатация Криокамеры', 'Конструирование "Кибердек"', 'Кибер-Технологии[2]',
                             'Подрывное дело[2]', 'Маскировка', 'Электроника', 'Электронная безопасность[2]', 'Первая помощь', 'Подделка', 'Вертолётная техника[3]',
                             'Закрашивать или Рисовать', 'Фотография и Кинофильмы', 'Фармацевтика[2]', 'Взлом замков', 'Карманная кража', 'Игра на инструментали', 'Оружейник[2]']
        }
        
        # Создаем вкладки для категорий
        self.skills_tabs = QTabWidget()
        self.skills_tabs.setStyleSheet(self.get_tab_style())
        layout.addWidget(self.skills_tabs)
        
        self.skill_entries = {}
        
        for category, skills in skill_categories.items():
            category_tab = QWidget()
            category_layout = QVBoxLayout(category_tab)
            category_layout.setAlignment(Qt.AlignTop)
            
            # Заголовок категории
            category_label = QLabel(category.upper())
            category_label.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    font-size: 14pt;
                    color: #ef0097;
                    text-align: center;
                    margin-bottom: 15px;
                }
            """)
            category_layout.addWidget(category_label)
            
            # Контейнер для навыков с возможностью прокрутки
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setStyleSheet("""
                QScrollArea {
                    background-color: #1a1a1a;
                    border: 1px solid #00ffff;
                }
                QScrollBar:vertical {
                    background: #0d0d0d;
                    width: 12px;
                }
                QScrollBar::handle:vertical {
                    background: #00ff00;
                }
            """)
            
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)
            scroll_layout.setAlignment(Qt.AlignTop)
            
            # Заголовки
            header_widget = QWidget()
            header_layout = QHBoxLayout(header_widget)
            header_layout.setContentsMargins(0, 0, 0, 10)
            
            # Заголовок для типа навыка
            type_header = QLabel("Тип")
            type_header.setAlignment(Qt.AlignCenter)
            type_header.setStyleSheet("color: #00ff00; font-weight: bold;")
            header_layout.addWidget(type_header)
            header_layout.addStretch(1)
            
            # Заголовок для названия навыка
            skill_header = QLabel("Навык")
            skill_header.setStyleSheet("color: #ef0097; font-weight: bold;")
            header_layout.addWidget(skill_header, 3)  # Больше места для названия
            
            # Заголовок для значения
            value_header = QLabel("Значение")
            value_header.setStyleSheet("color: #00ffff; font-weight: bold;")
            header_layout.addWidget(value_header, 1)  # Меньше места для значения
            
            scroll_layout.addWidget(header_widget)
            
            # Добавляем навыки с разделительными линиями
            for i, skill in enumerate(skills):
                skill_widget = QWidget()
                skill_layout = QHBoxLayout(skill_widget)
                skill_layout.setContentsMargins(5, 5, 5, 5)
                
                # Виджет типа навыка (цветной ползунок с текстом)
                type_widget = SkillTypeWidget()
                skill_layout.addWidget(type_widget)
                
                # Название навыка
                skill_label = QLabel(skill)
                skill_label.setStyleSheet("color: #ffffff; font-size: 11pt;")
                skill_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                skill_layout.addWidget(skill_label, 3)  # Больше места для названия
                
                # Поле для значения
                value_edit = QLineEdit("0")
                value_edit.setValidator(QIntValidator(0, 10))
                value_edit.setMaximumWidth(50)
                value_edit.setStyleSheet("""
                    QLineEdit {
                        background-color: #333333;
                        color: #00ff00;
                        border: 1px solid #555555;
                        padding: 3px;
                        font-family: 'Courier New';
                        font-size: 11pt;
                        text-align: center;
                    }
                    QLineEdit:hover {
                        background-color: #444444;
                    }
                """)
                skill_layout.addWidget(value_edit, 1)  # Меньше места для значения
                
                scroll_layout.addWidget(skill_widget)
                
                # Добавляем разделительную линию после каждого навыка
                if i < len(skills) - 1:
                    line = QFrame()
                    line.setFrameShape(QFrame.HLine)
                    line.setFrameShadow(QFrame.Sunken)
                    line.setStyleSheet("background-color: #555555; height: 1px;")
                    scroll_layout.addWidget(line)
                
                # Сохраняем элементы
                self.skill_entries[skill] = {
                    'value': value_edit,
                    'type_widget': type_widget,
                    'widget': skill_widget,
                    'category': category,
                    'visible': True
                }
            
            scroll_area.setWidget(scroll_content)
            category_layout.addWidget(scroll_area)
            self.skills_tabs.addTab(category_tab, category)
        
        self.tabs.addTab(skills_tab, "Навыки")
    
    def filter_skills(self, text):
        """Фильтрует навыки по тексту поиска"""
        text = text.lower()
        for skill_name, skill_data in self.skill_entries.items():
            # Показываем или скрываем виджет навыка в зависимости от совпадения
            if text in skill_name.lower() and skill_data['visible']:
                skill_data['widget'].show()
            else:
                skill_data['widget'].hide()
    
    def filter_skills_by_type(self, type_text):
        """Фильтрует навыки по типу"""
        type_map = {
            "Все": -1,
            "Чип": 0,
            "Проф": 1,
            "Доп": 2,
            "Обыч": 3
        }
        
        selected_type = type_map.get(type_text, -1)
        
        for skill_name, skill_data in self.skill_entries.items():
            if selected_type == -1 or skill_data['type_widget'].get_state() == selected_type:
                skill_data['visible'] = True
                # Показываем только если соответствует текстовому фильтру
                search_text = self.skill_search.text().lower()
                if search_text in skill_name.lower():
                    skill_data['widget'].show()
                else:
                    skill_data['widget'].hide()
            else:
                skill_data['visible'] = False
                skill_data['widget'].hide()
    
    def filter_acquired_skills(self, state):
        """Фильтрует навыки по приобретенным"""
        show_acquired = state == Qt.Checked
        
        for skill_name, skill_data in self.skill_entries.items():
            skill_value = int(skill_data['value'].text() or 0)
            
            if not show_acquired or skill_value > 0:
                skill_data['visible'] = True
                # Показываем только если соответствует текстовому фильтру и типу
                search_text = self.skill_search.text().lower()
                type_filter = self.type_filter.currentText()
                
                type_ok = (type_filter == "Все" or 
                          (type_filter == "Чип" and skill_data['type_widget'].get_state() == 0) or
                          (type_filter == "Проф" and skill_data['type_widget'].get_state() == 1) or
                          (type_filter == "Доп" and skill_data['type_widget'].get_state() == 2) or
                          (type_filter == "Обыч" and skill_data['type_widget'].get_state() == 3))
                
                if type_ok and (search_text in skill_name.lower() or not search_text):
                    skill_data['widget'].show()
                else:
                    skill_data['widget'].hide()
            else:
                skill_data['visible'] = False
                skill_data['widget'].hide()
    
    def sort_skills(self):
        options = ["По алфавиту (А-Я)", "По алфавиту (Я-А)", "По типу (чип)", "По типу (проф)", "По типу (доп)", "По типу (обыч)", "По значению (возр)", "По значению (убыв)"]
        option, ok = QInputDialog.getItem(
            self, "Сортировка навыков", "Выберите тип сортировки:", options, 0, False
        )
        
        if not ok:
            return
            
        # Временное отключение обновления интерфейса
        self.setUpdatesEnabled(False)
        
        # Собираем все виджеты навыков
        skill_widgets = []
        for skill_data in self.skill_entries.values():
            skill_widgets.append(skill_data['widget'])
        
        # Удаляем виджеты из контейнеров
        for skill_data in self.skill_entries.values():
            skill_data['widget'].setParent(None)
        
        # Сортировка в зависимости от выбранного варианта
        if option == "По алфавиту (А-Я)":
            sorted_skills = sorted(self.skill_entries.items(), key=lambda x: x[0])
        elif option == "По алфавиту (Я-А)":
            sorted_skills = sorted(self.skill_entries.items(), key=lambda x: x[0], reverse=True)
        elif option == "По типу (чип)":
            sorted_skills = sorted(self.skill_entries.items(), 
                                  key=lambda x: x[1]['type_widget'].get_state() == 0, 
                                  reverse=True)
        elif option == "По типу (проф)":
            sorted_skills = sorted(self.skill_entries.items(), 
                                  key=lambda x: x[1]['type_widget'].get_state() == 1, 
                                  reverse=True)
        elif option == "По типу (доп)":
            sorted_skills = sorted(self.skill_entries.items(), 
                                  key=lambda x: x[1]['type_widget'].get_state() == 2, 
                                  reverse=True)
        elif option == "По типу (обыч)":
            sorted_skills = sorted(self.skill_entries.items(), 
                                  key=lambda x: x[1]['type_widget'].get_state() == 3, 
                                  reverse=True)
        elif option == "По значению (возр)":
            sorted_skills = sorted(self.skill_entries.items(), 
                                  key=lambda x: int(x[1]['value'].text() or 0))
        elif option == "По значению (убыв)":
            sorted_skills = sorted(self.skill_entries.items(), 
                                  key=lambda x: int(x[1]['value'].text() or 0), 
                                  reverse=True)
        else:
            sorted_skills = self.skill_entries.items()
        
        # Добавляем виджеты обратно в контейнеры в отсортированном порядке
        for skill_name, skill_data in sorted_skills:
            # Находим контейнер для этой категории
            category = skill_data['category']
            for i in range(self.skills_tabs.count()):
                if self.skills_tabs.tabText(i) == category:
                    tab = self.skills_tabs.widget(i)
                    scroll_area = tab.findChild(QScrollArea)
                    scroll_content = scroll_area.widget()
                    scroll_layout = scroll_content.layout()
                    
                    # Добавляем виджет, если он должен быть видимым
                    if skill_data['visible']:
                        skill_data['widget'].show()
                    else:
                        skill_data['widget'].hide()
                        
                    scroll_layout.addWidget(skill_data['widget'])
                    break
        
        # Включаем обновление интерфейса
        self.setUpdatesEnabled(True)
    
    def create_cybernetics_section(self):
        cyber_tab = QWidget()
        layout = QVBoxLayout(cyber_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Таблица имплантов
        self.cyber_table = QTableWidget(0, 4)
        self.cyber_table.setHorizontalHeaderLabels(["Тип импланта", "Название", "Потеря человечности", "Стоимость (eb)"])
        self.cyber_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cyber_table.verticalHeader().setVisible(False)
        self.cyber_table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.cyber_table.setStyleSheet(self.get_table_style())
        layout.addWidget(self.cyber_table)
        
        # Поля для ввода нового импланта
        add_frame = QFrame()
        add_frame.setStyleSheet("background-color: #1a1a1a; padding: 10px;")
        add_layout = QHBoxLayout(add_frame)
        
        add_layout.addWidget(QLabel("Тип:"))
        self.cyber_type = IconComboBox()
        self.cyber_type.setStyleSheet(self.get_combo_box_style())
        self.cyber_type.addItems([
            'ФЭШН-оснащение', 'Нейро-Оснащение', 'Имплант-Размешеный внутри тела', 
            'Био-Импланты', 'Кибер-Оружие', 'Кибер-Оптика', 'Кибер-Аудио',
            'Кибер-Рука', 'Кибер-Нога', 'Кисти Рук и Ступни', 'Встраиваемые элементы в Кибер-Конечности',
            'Кибер оружие встраивания в Кибер-Конечности', 'Линейные Рамы', 'Нательные Пластины', 
        ])
        add_layout.addWidget(self.cyber_type)
        
        add_layout.addWidget(QLabel("Название:"))
        self.cyber_name = QLineEdit()
        self.cyber_name.setStyleSheet(self.get_line_edit_style())
        add_layout.addWidget(self.cyber_name)
        
        add_layout.addWidget(QLabel("Потеря чел-ти:"))
        self.cyber_hc = QLineEdit()
        self.cyber_hc.setValidator(QIntValidator(0, 100))
        self.cyber_hc.setStyleSheet(self.get_line_edit_style())
        self.cyber_hc.setMaximumWidth(80)
        add_layout.addWidget(self.cyber_hc)
        
        add_layout.addWidget(QLabel("Стоимость (eb):"))
        self.cyber_cost = QLineEdit()
        self.cyber_cost.setValidator(QIntValidator(0, 1000000))
        self.cyber_cost.setStyleSheet(self.get_line_edit_style())
        self.cyber_cost.setMaximumWidth(80)
        add_layout.addWidget(self.cyber_cost)
        
        # Кнопки
        btn_add = QPushButton("Добавить")
        btn_add.setStyleSheet(self.get_button_style())
        btn_add.clicked.connect(self.add_cyber_implant)
        
        btn_delete = QPushButton("Удалить")
        btn_delete.setStyleSheet(self.get_button_style())
        btn_delete.clicked.connect(lambda: self.delete_selected(self.cyber_table))
        
        add_layout.addWidget(btn_add)
        add_layout.addWidget(btn_delete)
        
        layout.addWidget(add_frame)
        
        # Итоговые значения
        total_frame = QFrame()
        total_frame.setStyleSheet("background-color: #1a1a1a; padding: 10px;")
        total_layout = QHBoxLayout(total_frame)
        
        total_layout.addWidget(QLabel("Общая потеря человечности:"))
        self.total_hc_label = QLabel("0")
        self.total_hc_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        total_layout.addWidget(self.total_hc_label)
        
        total_layout.addWidget(QLabel("Общая стоимость:"))
        self.total_cost_label = QLabel("0 eb")
        self.total_cost_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        total_layout.addWidget(self.total_cost_label)
        
        total_layout.addStretch()
        layout.addWidget(total_frame)
        
        self.tabs.addTab(cyber_tab, "Кибернетика")
    
    def add_cyber_implant(self):
        implant_type = self.cyber_type.currentText()
        name = self.cyber_name.text()
        hc = self.cyber_hc.text()
        cost = self.cyber_cost.text()
        
        if implant_type and name and hc and cost:
            row = self.cyber_table.rowCount()
            self.cyber_table.insertRow(row)
            self.cyber_table.setItem(row, 0, QTableWidgetItem(implant_type))
            self.cyber_table.setItem(row, 1, QTableWidgetItem(name))
            self.cyber_table.setItem(row, 2, QTableWidgetItem(hc))
            self.cyber_table.setItem(row, 3, QTableWidgetItem(cost))
            
            # Обновляем итоговые значения
            total_cost = 0
            total_hc = 0
            for i in range(self.cyber_table.rowCount()):
                try:
                    total_cost += int(self.cyber_table.item(i, 3).text())
                    total_hc += int(self.cyber_table.item(i, 2).text())
                except:
                    pass
            
            self.total_hc_label.setText(str(total_hc))
            self.total_cost_label.setText(f"{total_cost} eb")
            
            # Обновляем вычисляемые характеристики
            self.update_derived_stats()
            
            # Очищаем поля ввода
            self.cyber_type.setCurrentIndex(0)
            self.cyber_name.clear()
            self.cyber_hc.clear()
            self.cyber_cost.clear()
        else:
            QMessageBox.warning(self, "Внимание", "Все поля должны быть заполнены!")
    
    def create_weapons_section(self):
        weapons_tab = QWidget()
        layout = QVBoxLayout(weapons_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Таблица оружия
        self.weapons_table = QTableWidget(0, 8)
        self.weapons_table.setHorizontalHeaderLabels([
            "Название", "Тип", "Точность", "Скрытность", 
            "Доступность", "Урон", "Обойма", "Надежность"
        ])
        self.weapons_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.weapons_table.verticalHeader().setVisible(False)
        self.weapons_table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.weapons_table.setStyleSheet(self.get_table_style())
        
        # Устанавливаем делегат для колонок с выпадающими списками
        self.weapons_table.setItemDelegateForColumn(1, CustomComboBoxDelegate(self))
        self.weapons_table.setItemDelegateForColumn(3, CustomComboBoxDelegate(self))
        self.weapons_table.setItemDelegateForColumn(4, CustomComboBoxDelegate(self))
        self.weapons_table.setItemDelegateForColumn(7, CustomComboBoxDelegate(self))
        
        layout.addWidget(self.weapons_table)
        
        # Поля для ввода нового оружия
        add_frame = QFrame()
        add_frame.setStyleSheet("background-color: #1a1a1a; padding: 10px;")
        add_layout = QGridLayout(add_frame)
        
        # Поля для ввода
        fields = [
            ("Название:", "weapon_name", 0, 0),
            ("Тип:", "weapon_type", 0, 2),
            ("Точность:", "weapon_acc", 1, 0),
            ("Скрытность:", "weapon_conceal", 1, 2),
            ("Доступность:", "weapon_draw", 2, 0),
            ("Урон:", "weapon_dmg", 2, 2),
            ("Обойма:", "weapon_clip", 3, 0),
            ("Надежность:", "weapon_rel", 3, 2)
        ]
        
        self.weapon_entries = {}
        self.weapon_combo_entries = {}
        
        for label, name, row, col in fields:
            add_layout.addWidget(QLabel(label), row, col)
            
            if name in ["weapon_type", "weapon_conceal", "weapon_draw", "weapon_rel"]:
                # Это выпадающие списки
                combo = IconComboBox()
                combo.setStyleSheet(self.get_combo_box_style())
                
                if name == "weapon_type":
                    combo.addItems([
                        "Пистолеты-Пулемёты (ПП)", "Дробовики (ДРБ)", "Винтовки (ВИН)",
                        "Тяжелое вооружение (ТЯЖ)", "Оружие Ближнего Боя (ОББ)", 
                        "Экзотическое Оружие (ЭКЗ)", "Вести свой вариант"
                    ])
                elif name == "weapon_conceal":
                    combo.addItems([
                        "Карманы (Карманы, штанины брюк или рукава)(Kар)",
                        "Куртка (Куртка, пальто, оперативная кобура)(Кур)",
                        "Длинный (Длинный плащ)(Д)", "Нет (Не может быть спрятано)(H)",
                        "Вести свой вариант"
                    ])
                elif name == "weapon_draw":
                    combo.addItems([
                        "Отличная (O)", "Доступная (Д)", "Малая (M)", "Редкая (P)", "Вести свой вариант"
                    ])
                elif name == "weapon_rel":
                    combo.addItems([
                        "Очень надёжное (OH)", "Обычное (ОБ)", "Ненадёжный (HH)", "Вести свой вариант"
                    ])
                
                add_layout.addWidget(combo, row, col+1)
                self.weapon_combo_entries[name] = combo
            else:
                # Это текстовые поля
                entry = QLineEdit()
                entry.setStyleSheet(self.get_line_edit_style())
                add_layout.addWidget(entry, row, col+1)
                self.weapon_entries[name] = entry
        
        # Кнопки
        btn_frame = QFrame()
        btn_layout = QHBoxLayout(btn_frame)
        
        btn_add = QPushButton("Добавить")
        btn_add.setStyleSheet(self.get_button_style())
        btn_add.clicked.connect(self.add_weapon)
        
        btn_delete = QPushButton("Удалить")
        btn_delete.setStyleSheet(self.get_button_style())
        btn_delete.clicked.connect(lambda: self.delete_selected(self.weapons_table))
        
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_delete)
        
        add_layout.addWidget(btn_frame, 4, 0, 1, 4)
        layout.addWidget(add_frame)
        
        self.tabs.addTab(weapons_tab, "Оружие")
    
    def add_weapon(self):
        name = self.weapon_entries['weapon_name'].text()
        acc = self.weapon_entries['weapon_acc'].text()
        dmg = self.weapon_entries['weapon_dmg'].text()
        clip = self.weapon_entries['weapon_clip'].text()
        
        weapon_type = self.weapon_combo_entries['weapon_type'].currentText()
        conceal = self.weapon_combo_entries['weapon_conceal'].currentText()
        draw = self.weapon_combo_entries['weapon_draw'].currentText()
        rel = self.weapon_combo_entries['weapon_rel'].currentText()
        
        if name and weapon_type and acc and conceal and draw and dmg and clip and rel:
            row = self.weapons_table.rowCount()
            self.weapons_table.insertRow(row)
            self.weapons_table.setItem(row, 0, QTableWidgetItem(name))
            self.weapons_table.setItem(row, 1, QTableWidgetItem(weapon_type))
            self.weapons_table.setItem(row, 2, QTableWidgetItem(acc))
            self.weapons_table.setItem(row, 3, QTableWidgetItem(conceal))
            self.weapons_table.setItem(row, 4, QTableWidgetItem(draw))
            self.weapons_table.setItem(row, 5, QTableWidgetItem(dmg))
            self.weapons_table.setItem(row, 6, QTableWidgetItem(clip))
            self.weapons_table.setItem(row, 7, QTableWidgetItem(rel))
            
            # Очищаем поля ввода
            for entry in self.weapon_entries.values():
                entry.clear()
            for combo in self.weapon_combo_entries.values():
                combo.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Внимание", "Все поля должны быть заполнены!")
    
    def create_equipment_section(self):
        equip_tab = QWidget()
        layout = QVBoxLayout(equip_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Таблица снаряжения
        self.equip_table = QTableWidget(0, 5)
        self.equip_table.setHorizontalHeaderLabels(["Название", "Тип", "Цена (eb)", "Описание", "Вес (кг)"])
        self.equip_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.equip_table.verticalHeader().setVisible(False)
        self.equip_table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.equip_table.setStyleSheet(self.get_table_style())
        layout.addWidget(self.equip_table)
        
        # Поля для ввода нового снаряжения
        add_frame = QFrame()
        add_frame.setStyleSheet("background-color: #1a1a1a; padding: 10px;")
        add_layout = QGridLayout(add_frame)
        
        fields = [
            ("Название:", "equip_name"),
            ("Цена (eb):", "equip_price"),
            ("Описание:", "equip_desc"),
            ("Вес (кг):", "equip_weight")
        ]
        
        self.equip_entries = {}
        for i, (label, name) in enumerate(fields):
            add_layout.addWidget(QLabel(label), i, 0)
            entry = QLineEdit()
            entry.setStyleSheet(self.get_line_edit_style())
            
            if 'price' in name or 'weight' in name:
                entry.setValidator(QIntValidator(0, 1000000))
            
            add_layout.addWidget(entry, i, 1)
            self.equip_entries[name] = entry
        
        # Поле типа с выпадающим списком
        add_layout.addWidget(QLabel("Тип:"), 4, 0)
        self.equip_type = IconComboBox()
        self.equip_type.addItems([
            "Броня", "Особая экипировка", "Мода", "Инструменты", "Личная электроника", 
            "Системы данных", "Связь", "Наблюдение", "Развлечение", "Безопасность", 
            "Медицина", "Мебель", "Транспорт", "Образ Жизни", "Бакалея", "Жильё", 
            "Вести свой вариант"
        ])
        self.equip_type.setStyleSheet(self.get_combo_box_style())
        add_layout.addWidget(self.equip_type, 4, 1)
        
        # Кнопки
        btn_frame = QFrame()
        btn_layout = QHBoxLayout(btn_frame)
        
        btn_add = QPushButton("Добавить")
        btn_add.setStyleSheet(self.get_button_style())
        btn_add.clicked.connect(self.add_equipment)
        
        btn_delete = QPushButton("Удалить")
        btn_delete.setStyleSheet(self.get_button_style())
        btn_delete.clicked.connect(lambda: self.delete_selected(self.equip_table))
        
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_delete)
        
        add_layout.addWidget(btn_frame, 5, 0, 1, 2)
        layout.addWidget(add_frame)
        
        self.tabs.addTab(equip_tab, "Снаряжение")
    
    def add_equipment(self):
        name = self.equip_entries['equip_name'].text()
        equip_type = self.equip_type.currentText()
        price = self.equip_entries['equip_price'].text()
        desc = self.equip_entries['equip_desc'].text()
        weight = self.equip_entries['equip_weight'].text()
        
        if name and equip_type and price and desc and weight:
            row = self.equip_table.rowCount()
            self.equip_table.insertRow(row)
            self.equip_table.setItem(row, 0, QTableWidgetItem(name))
            self.equip_table.setItem(row, 1, QTableWidgetItem(equip_type))
            self.equip_table.setItem(row, 2, QTableWidgetItem(price))
            self.equip_table.setItem(row, 3, QTableWidgetItem(desc))
            self.equip_table.setItem(row, 4, QTableWidgetItem(weight))
            
            for entry in self.equip_entries.values():
                entry.clear()
            self.equip_type.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Внимание", "Все поля должны быть заполнены!")
    
    def create_lifepath_section(self):
        lifepath_tabs = QTabWidget()
        
        # Подраздел 1: Основная информация
        tab1 = QWidget()
        layout1 = QGridLayout(tab1)
        
        fields1 = [
            ("Имя:", "lp_name"),
            ("Пол:", "lp_gender"),
            ("Возраст:", "lp_age"),
            ("Этнос:", "lp_birthplace"),
            ("Язык:", "lp_language")
        ]
        
        for i, (label, name) in enumerate(fields1):
            layout1.addWidget(QLabel(label), i, 0)
            if name == "lp_gender":
                # Заменяем поле пола на выпадающий список
                combo = IconComboBox()
                combo.setStyleSheet(self.get_combo_box_style())
                combo.addItems(["Мужской", "Женский"])
                layout1.addWidget(combo, i, 1)
                setattr(self, name, combo)
            else:
                entry = QLineEdit()
                entry.setStyleSheet(self.get_line_edit_style())
                layout1.addWidget(entry, i, 1)
                setattr(self, name, entry)
        
        lifepath_tabs.addTab(tab1, "1. Основная информация")
        
        # Подраздел 2: Стиль
        tab2 = QWidget()
        layout2 = QGridLayout(tab2)
        
        fields2 = [
            ("Одежда:", "lp_clothes"),
            ("Прическа:", "lp_hairstyle"),
            ("Фишка:", "lp_feature"),
            ("Модные течений:", "lp_origin")
        ]
        
        for i, (label, name) in enumerate(fields2):
            layout2.addWidget(QLabel(label), i, 0)
            if name == "lp_origin":
                # Заменяем поле модных течений на выпадающий список
                combo = IconComboBox()
                combo.setStyleSheet(self.get_combo_box_style())
                combo.addItems([
                    "Универсальный шик", "Досуговая одежда", "Деловая одежда", 
                    "Высокая мода", "Городское сияние", "Вести свой вариант"
                ])
                layout2.addWidget(combo, i, 1)
                setattr(self, name, combo)
            else:
                entry = QLineEdit()
                entry.setStyleSheet(self.get_line_edit_style())
                layout2.addWidget(entry, i, 1)
                setattr(self, name, entry)
        
        lifepath_tabs.addTab(tab2, "2. Стиль")
        
        # Подраздел 3: Мотивы
        tab3 = QWidget()
        layout3 = QGridLayout(tab3)
        
        fields3 = [
            ("Черта характера:", "lp_trait"),
            ("Важная личность:", "lp_personality"),
            ("Личные ценности:", "lp_values"),
            ("Отношение к людям:", "lp_attitude"),
            ("Значимый предмет:", "lp_item"),
            ("Мечта:", "lp_dream"),
            ("Фобии/страхи:", "lp_phobias")
        ]
        
        for i, (label, name) in enumerate(fields3):
            layout3.addWidget(QLabel(label), i, 0)
            entry = QLineEdit()
            entry.setStyleSheet(self.get_line_edit_style())
            layout3.addWidget(entry, i, 1)
            setattr(self, name, entry)
        
        lifepath_tabs.addTab(tab3, "3. Мотивы")
        
        # Подраздел 4: История персонажа
        tab4 = QWidget()
        layout4 = QVBoxLayout(tab4)
        
        layout4.addWidget(QLabel("История персонажа:"))
        self.lp_history = QTextEdit()
        self.lp_history.setStyleSheet("""
            QTextEdit {
                background-color: #333333;
                color: #00ff00;
                border: 1px solid #7fffd4;
                font-family: 'Courier New';
                font-size: 10pt;
            }
        """)
        layout4.addWidget(self.lp_history)
        
        lifepath_tabs.addTab(tab4, "4. История персонажа")
        
        # Подраздел 5: События в жизни
        tab5 = QWidget()
        layout5 = QVBoxLayout(tab5)
        
        # Таблица событий с сортировкой
        self.events_table = QTableWidget(0, 2)
        self.events_table.setHorizontalHeaderLabels(["Год", "Событие"])
        self.events_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.events_table.verticalHeader().setVisible(False)
        self.events_table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.events_table.setSortingEnabled(True)  # Включаем сортировку
        self.events_table.sortByColumn(0, Qt.AscendingOrder)  # Сортировка по возрастанию
        self.events_table.setStyleSheet(self.get_table_style())
        layout5.addWidget(self.events_table)
        
        # Кнопка для генерации событий
        gen_btn = QPushButton("Сгенерировать событие")
        gen_btn.setStyleSheet(self.get_button_style())
        gen_btn.clicked.connect(self.generate_life_event)
        layout5.addWidget(gen_btn)
        
        # Поля для ввода событий
        add_frame = QFrame()
        add_frame.setStyleSheet("background-color: #1a1a1a; padding: 10px;")
        add_layout = QHBoxLayout(add_frame)
        
        add_layout.addWidget(QLabel("Год:"))
        self.event_year = QLineEdit()
        self.event_year.setValidator(QIntValidator(0, 2100))
        self.event_year.setStyleSheet(self.get_line_edit_style())
        self.event_year.setMaximumWidth(80)
        add_layout.addWidget(self.event_year)
        
        add_layout.addWidget(QLabel("Событие:"))
        self.event_desc = QLineEdit()
        self.event_desc.setStyleSheet(self.get_line_edit_style())
        add_layout.addWidget(self.event_desc)
        
        btn_add = QPushButton("Добавить")
        btn_add.setStyleSheet(self.get_button_style())
        btn_add.clicked.connect(self.add_life_event)
        
        btn_delete = QPushButton("Удалить")
        btn_delete.setStyleSheet(self.get_button_style())
        btn_delete.clicked.connect(lambda: self.delete_selected(self.events_table))
        
        add_layout.addWidget(btn_add)
        add_layout.addWidget(btn_delete)
        
        layout5.addWidget(add_frame)
        lifepath_tabs.addTab(tab5, "5. События в жизни")
        
        # Подраздел 6: Семья
        tab6 = QWidget()
        layout6 = QVBoxLayout(tab6)
        layout6.setSpacing(15)
        
        # Семейная информация
        family_group = QGroupBox("Семейная информация")
        family_group.setStyleSheet(self.get_group_box_style())
        family_layout = QGridLayout(family_group)
        
        # Рейтинг семьи
        family_layout.addWidget(QLabel("Рейтинг семьи:"), 0, 0)
        self.family_rating = IconComboBox()
        self.family_rating.setStyleSheet(self.get_combo_box_style())
        self.family_rating.addItems([
            "Корпоративные руководители", "Корпоративные менеджеры", "Корпоративные техники", 
            "Стая номадов", "Пиратский флот", "Семейная банда", "Криминальные лорды", 
            "Беднота Боевой зоны", "Городские бездомные", "Семья из аркологии", "Вести свой вариант"
        ])
        family_layout.addWidget(self.family_rating, 0, 1)
        
        # Что-то произошло с твоими родителями
        family_layout.addWidget(QLabel("Что-то произошло с твоими родителями:"), 1, 0)
        self.parent_status = IconComboBox()
        self.parent_status.setStyleSheet(self.get_combo_box_style())
        self.parent_status.addItems([
            "С ними все хорошо", "Твои родители погибли во время войны.", 
            "Твои родители погибли в результате несчастного случая.", 
            "Твои родители были убиты.", 
            "Твои родители получили амнезию и не помнят тебя.", 
            "Ты никогда не знал своих родителей.", 
            "Твои родители скрываются, чтобы защитить тебя.", 
            "Ты был оставлен на попечение родственникам.", 
            "Ты вырос на улице и у тебя никогда не было родителей.", 
            "Твои родители отказались от тебя.", 
            "Твои родители продали тебя за деньги", 
            "Вести свой вариант"
        ])
        family_layout.addWidget(self.parent_status, 1, 1)
        
        # Семейная трагедия
        family_layout.addWidget(QLabel("Семейная трагедия:"), 2, 0)
        self.family_tragedy = IconComboBox()
        self.family_tragedy.setStyleSheet(self.get_combo_box_style())
        self.family_tragedy.addItems([
            "Семья потеряла всё из-за предательства.", 
            "Семья потеряла всё из-за плохого менеджмента.", 
            "Семья в изгнании или иным образом изгнана из своего первоначального дома / нации / корпорации.", 
            "Семья в тюрьме, и сбежал только ты.", 
            "Семья исчезла,Ты остался один.", 
            "Семья был убит по заказу, и ты единственный выживший.", 
            "Семья вовлечена в давний заговор,организацию или ассоциации, такую как преступная или революционная группа.", 
            "Твоя семья была рассеяна по ветру из-за несчастья.", 
            "Твоя семья проклята наследственной враждой, которая длится в течение нескольких поколений.", 
            "Ты являешься наследником семейного долга. Ты должен выплатить этот долг, прежде чем идти дальше по своей жизни.", 
            "Вести свой вариант."
        ])
        family_layout.addWidget(self.family_tragedy, 2, 1)
        
        # Место проведенного детства
        family_layout.addWidget(QLabel("Место проведенного детства:"), 3, 0)
        self.childhood_place = IconComboBox()
        self.childhood_place.setStyleSheet(self.get_combo_box_style())
        self.childhood_place.addItems([
            "Прошло на улице, без присмотра взрослых.", 
            "Прошло в безопасном корпоративном пригороде.", 
            "В стае номадов, переезжающих из города в город.", 
            "В разрушающемся, некогда высококлассном районе.", 
            "В защищенной корпоративной зоне в центре города.", 
            "В центре Боевой зоны.", 
            "В маленькой деревне или населёном пункте, в отдалении от города.", 
            "В большой аркологии.", 
            "В морской пиратской банде.", 
            "На корпоративной ферме или в исследовательском центере.", 
            "Вести свой вариант"
        ])
        family_layout.addWidget(self.childhood_place, 3, 1)
        
        layout6.addWidget(family_group)
        
        # Братья/сестры
        siblings_group = QGroupBox("Братья/сестры")
        siblings_group.setStyleSheet(self.get_group_box_style())
        siblings_layout = QVBoxLayout(siblings_group)
        
        # Таблица братьев/сестер
        self.siblings_table = QTableWidget(0, 4)
        self.siblings_table.setHorizontalHeaderLabels(["Имя", "Пол", "Возраст", "Отношение"])
        self.siblings_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.siblings_table.verticalHeader().setVisible(False)
        self.siblings_table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.siblings_table.setStyleSheet(self.get_table_style())
        siblings_layout.addWidget(self.siblings_table)
        
        # Поля для добавления брата/сестры
        add_frame = QFrame()
        add_frame.setStyleSheet("background-color: #1a1a1a; padding: 10px;")
        add_layout = QHBoxLayout(add_frame)
        
        add_layout.addWidget(QLabel("Имя:"))
        self.sibling_name = QLineEdit()
        self.sibling_name.setStyleSheet(self.get_line_edit_style())
        add_layout.addWidget(self.sibling_name)
        
        add_layout.addWidget(QLabel("Пол:"))
        self.sibling_gender = IconComboBox()
        self.sibling_gender.setStyleSheet(self.get_combo_box_style())
        self.sibling_gender.addItems(['М', 'Ж'])
        add_layout.addWidget(self.sibling_gender)
        
        add_layout.addWidget(QLabel("Возраст:"))
        self.sibling_age = IconComboBox()
        self.sibling_age.setStyleSheet(self.get_combo_box_style())
        self.sibling_age.addItems(['Старший', 'Младший', 'Близнец'])
        add_layout.addWidget(self.sibling_age)
        
        add_layout.addWidget(QLabel("Отношение:"))
        self.sibling_attitude = IconComboBox()
        self.sibling_attitude.setStyleSheet(self.get_combo_box_style())
        self.sibling_attitude.addItems([
            'Ненавидит', 'Не любит', 'Нейтрально', 'Любит', 'Поклоняется'
        ])
        add_layout.addWidget(self.sibling_attitude)
        
        # Кнопки
        btn_add = QPushButton("Добавить")
        btn_add.setStyleSheet(self.get_button_style())
        btn_add.clicked.connect(self.add_sibling)
        
        btn_delete = QPushButton("Удалить")
        btn_delete.setStyleSheet(self.get_button_style())
        btn_delete.clicked.connect(lambda: self.delete_selected(self.siblings_table))
        
        add_layout.addWidget(btn_add)
        add_layout.addWidget(btn_delete)
        
        siblings_layout.addWidget(add_frame)
        layout6.addWidget(siblings_group)
        lifepath_tabs.addTab(tab6, "6. Семья")
        
        self.tabs.addTab(lifepath_tabs, "Жизненный путь")
    
    def generate_life_event(self):
        # Определяем год (16 или последний год + 1)
        year = 16
        max_year = 0
        
        # Ищем максимальный год в событиях
        for row in range(self.events_table.rowCount()):
            try:
                year_val = int(self.events_table.item(row, 0).text())
                if year_val > max_year:
                    max_year = year_val
            except:
                pass
        
        if max_year > 0:
            year = max_year + 1
        
        # Генерируем событие
        roll = random.randint(1, 10)
        
        if roll <= 3:
            # Большие проблемы/победы
            sub_roll = random.randint(1, 10)
            if sub_roll % 2 == 0:
                # Победа
                event_type = "ТЕБЕ ПОВЕЗЛО"
                event_desc = self.generate_lucky_event()
            else:
                # Проблема
                event_type = "БЕДСТВИЯ!"
                event_desc = self.generate_disaster_event()
        elif roll <= 6:
            event_type = "Друзья и враги"
            event_desc = "Появились новые друзья или враги"
        elif roll <= 8:
            event_type = "Романтическое увлечение"
            event_desc = "Начались романтические отношения"
        else:
            event_type = "Ничего не случилось"
            event_desc = "В этом году не произошло значимых событий"
        
        # Добавляем событие
        row = self.events_table.rowCount()
        self.events_table.insertRow(row)
        self.events_table.setItem(row, 0, QTableWidgetItem(str(year)))
        self.events_table.setItem(row, 1, QTableWidgetItem(f"{event_type}: {event_desc}"))
        
        # Сортируем события по годам
        self.events_table.sortByColumn(0, Qt.AscendingOrder)
    
    def generate_lucky_event(self):
        roll = random.randint(1, 10)
        events = {
            1: "Завел Влиятельный контакт в городской администрации",
            2: "Финансовая неожиданность",
            3: "Сверхприбыль на работе или сделке!",
            4: "Находишь Сэнсэя (учителя)",
            5: "Находишь Учителя",
            6: "Влиятельный Корпоративный Руководитель должен тебе одну услугу",
            7: "Местная стая номадов подружилась с тобой",
            8: "Завёл друга в полицейских силас",
            9: "Ты нравишься местной банде бустеров",
            10: "Находишь Боевого Наставника"
        }
        return events.get(roll, "Неизвестное событие")
    
    def generate_disaster_event(self):
        roll = random.randint(1, 10)
        events = {
            1: "Финансовые потери или долги",
            "2": "Лишение свободы",
            3: "Болезнь или зависимость",
            4: "Предательство",
            5: "Авария",
            6: "Возлюбленный, друг или родственник был убит",
            7: "Ложное обвинение",
            8: "За тобой охотится Закон",
            9: "За тобой охотится Корпорация",
            10: "Психологическая или физиологическая недееспособность"
        }
        return events.get(roll, "Неизвестное бедствие")
    
    def add_life_event(self):
        year = self.event_year.text()
        desc = self.event_desc.text()
        
        if year and desc:
            row = self.events_table.rowCount()
            self.events_table.insertRow(row)
            self.events_table.setItem(row, 0, QTableWidgetItem(year))
            self.events_table.setItem(row, 1, QTableWidgetItem(desc))
            
            # Сортируем события по годам
            self.events_table.sortByColumn(0, Qt.AscendingOrder)
            
            self.event_year.clear()
            self.event_desc.clear()
        else:
            QMessageBox.warning(self, "Внимание", "Оба поля должны быть заполнены!")
    
    def add_sibling(self):
        name = self.sibling_name.text()
        gender = self.sibling_gender.currentText()
        age = self.sibling_age.currentText()
        attitude = self.sibling_attitude.currentText()
        
        if name and gender and age and attitude:
            row = self.siblings_table.rowCount()
            self.siblings_table.insertRow(row)
            self.siblings_table.setItem(row, 0, QTableWidgetItem(name))
            self.siblings_table.setItem(row, 1, QTableWidgetItem(gender))
            self.siblings_table.setItem(row, 2, QTableWidgetItem(age))
            self.siblings_table.setItem(row, 3, QTableWidgetItem(attitude))
            
            self.sibling_name.clear()
            self.sibling_gender.setCurrentIndex(0)
            self.sibling_age.setCurrentIndex(0)
            self.sibling_attitude.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Внимание", "Все поля должны быть заполнены!")
    
    def delete_selected(self, table):
        selected_rows = set()
        for index in table.selectedIndexes():
            selected_rows.add(index.row())
        
        for row in sorted(selected_rows, reverse=True):
            table.removeRow(row)
        
        # Если это таблица кибернетики, обновляем производные характеристики
        if table == self.cyber_table:
            total_cost = 0
            total_hc = 0
            for i in range(self.cyber_table.rowCount()):
                try:
                    total_cost += int(self.cyber_table.item(i, 3).text())
                    total_hc += int(self.cyber_table.item(i, 2).text())
                except:
                    pass
            
            self.total_hc_label.setText(str(total_hc))
            self.total_cost_label.setText(f"{total_cost} eb")
            self.update_derived_stats()
    
    def load_image(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Выберите изображение персонажа", "", 
                "Images (*.png *.jpg *.jpeg *.gif)"
            )
            if file_path:
                self.current_image_path = file_path
                self.load_image_from_path(file_path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить изображение: {e}")
            logging.error(f"Image load error: {e}")
    
    def load_image_from_path(self, file_path):
        try:
            # Ограничение размера изображения
            max_size = QSize(800, 800)
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                # Очищаем предыдущее изображение
                self.char_image.clear()
                
                # Масштабирование с сохранением пропорций
                scaled = pixmap.scaled(
                    max_size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.char_image.setPixmap(scaled)
            else:
                self.char_image.clear()
                QMessageBox.warning(self, "Ошибка", "Неверный формат изображения")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить изображение: {e}")
            logging.error(f"Image processing error: {e}")
    
    # Стилизация
    def get_main_style(self):
        return f"""
            QMainWindow {{
                background-color: {self.bg_color.name()};
                color: {self.fg_color.name()};
                font-family: 'Courier New';
            }}
            
            QLabel {{
                color: {self.fg_color.name()};
            }}
        """
    
    def get_tab_style(self):
        return f"""
            QTabWidget::pane {{
                border: 1px solid {self.accent_color.name()};
                background: {self.section_bg.name()};
            }}
            
            QTabBar::tab {{
                background: {self.bg_color.name()};
                color: {self.fg_color.name()};
                border: 1px solid {self.accent_color.name()};
                padding: 8px;
                font-weight: bold;
            }}
            
            QTabBar::tab:selected {{
                background: {self.section_bg.name()};
                border-bottom: 3px solid #00ff00;
                color: #00ff00;
                font-weight: bold;
            }}
        """
    
    def get_group_box_style(self):
        return f"""
            QGroupBox {{
                background-color: {self.section_bg.name()};
                color: {self.accent_color.name()};
                border: 1px solid {self.accent_color.name()};
                border-radius: 5px;
                margin-top: 1ex;
                font-weight: bold;
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                background-color: {self.section_bg.name()};
                color: {self.accent_color.name()};
            }}
        """
    
    def get_line_edit_style(self):
        return f"""
            QLineEdit {{
                background-color: #333333;
                color: {self.fg_color.name()};
                border: 1px solid #555555;
                padding: 2px;
                font-family: 'Courier New';
            }}
        """
    
    def get_combo_box_style(self):
        return f"""
            QComboBox {{
                background-color: #333333;
                color: {self.fg_color.name()};
                border: 1px solid #555555;
                padding: 2px;
                font-family: 'Courier New';
            }}
            
            QComboBox::drop-down {{
                border: none;
            }}
        """
    
    def get_button_style(self):
        return f"""
            QPushButton {{
                background-color: {self.bg_color.name()};
                color: {self.fg_color.name()};
                border: 1px solid {self.accent_color.name()};
                padding: 5px;
                font-weight: bold;
                font-family: 'Courier New';
            }}
            
            QPushButton:hover {{
                background-color: #333333;
            }}
            
            QPushButton:pressed {{
                background-color: #555555;
            }}
        """
    
    def get_table_style(self):
        return f"""
            QTableWidget {{
                background-color: {self.table_bg_color.name()};
                color: {self.fg_color.name()};
                gridline-color: {self.table_border_color.name()};
                font-family: 'Courier New';
                font-size: 10pt;
                border: 1px solid {self.table_border_color.name()};
            }}
            
            QHeaderView::section {{
                background-color: {self.table_header_bg.name()};
                color: {self.table_header_fg.name()};
                padding: 4px;
                border: 1px solid {self.table_border_color.name()};
                font-weight: bold;
            }}
            
            QTableWidget::item {{
                padding: 4px;
            }}
            
            QTableWidget::item:selected {{
                background-color: #444444;
                color: {self.fg_color.name()};
            }}
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Установка иконки приложения
    icon_path = "icon.ico"  # Укажите путь к вашей иконке
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Установка стиля приложения
    app.setStyle("Fusion")
    
    # Инициализация палитры стандартной темой
    themes = ThemeManager.get_themes()
    standard_theme = themes["Стандарт"]
    
    palette = QPalette()
    palette.setColor(QPalette.Window, standard_theme["bg_color"])
    palette.setColor(QPalette.WindowText, standard_theme["fg_color"])
    palette.setColor(QPalette.Base, standard_theme["section_bg"])
    palette.setColor(QPalette.AlternateBase, standard_theme["table_bg_color"])
    palette.setColor(QPalette.ToolTipBase, standard_theme["fg_color"])
    palette.setColor(QPalette.ToolTipText, standard_theme["bg_color"])
    palette.setColor(QPalette.Text, standard_theme["fg_color"])
    palette.setColor(QPalette.Button, standard_theme["bg_color"])
    palette.setColor(QPalette.ButtonText, standard_theme["fg_color"])
    palette.setColor(QPalette.BrightText, standard_theme["accent_color"])
    palette.setColor(QPalette.Highlight, standard_theme["accent_color"])
    palette.setColor(QPalette.HighlightedText, standard_theme["table_header_fg"])
    app.setPalette(palette)
    
    # Установка шрифта
    font = QFont("Courier New", 10)
    app.setFont(font)
    
    window = CyberpunkCharacterSheet()
    window.show()
    sys.exit(app.exec_())