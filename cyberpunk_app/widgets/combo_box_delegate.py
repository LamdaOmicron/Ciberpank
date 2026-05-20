"""
Делегат ComboBox для таблиц
"""

from PyQt5.QtWidgets import QStyledItemDelegate, QComboBox


class CustomComboBoxDelegate(QStyledItemDelegate):
    """
    Делегат для создания ComboBox в ячейках таблицы
    
    Предоставляет предустановленные списки значений для разных колонок
    """
    
    # Предустановленные значения для колонок
    WEAPON_TYPES = [
        "Пистолеты-Пулемёты (ПП)",
        "Дробовики (ДРБ)",
        "Винтовки (ВИН)",
        "Тяжелое вооружение (ТЯЖ)",
        "Оружие Ближнего Боя (ОББ)",
        "Экзотическое Оружие (ЭКЗ)",
        "Вести свой вариант"
    ]
    
    CONCEALMENT_OPTIONS = [
        "Карманы (Карманы, штанины брюк или рукава)(Kар)",
        "Куртка (Куртка, пальто, оперативная кобура)(Кур)",
        "Длинный (Длинный плащ)(Д)",
        "Нет (Не может быть спрятано)(H)",
        "Вести свой вариант"
    ]
    
    AVAILABILITY_OPTIONS = [
        "Отличная (O)",
        "Доступная (Д)",
        "Малая (M)",
        "Редкая (P)",
        "Вести свой вариант"
    ]
    
    RELIABILITY_OPTIONS = [
        "Очень надёжное (OH)",
        "Обычное (ОБ)",
        "Ненадёжный (HH)",
        "Вести свой вариант"
    ]
    
    def __init__(self, parent=None, column_configs: dict = None):
        """
        Инициализация делегата
        
        Args:
            parent: Родительский виджет
            column_configs: Словарь конфигураций для колонок
                           {column_index: [list of options]}
        """
        super().__init__(parent)
        self._column_configs = column_configs or {}
    
    def createEditor(self, parent, option, index):
        """
        Создает редактор для ячейки таблицы
        
        Args:
            parent: Родительский виджет
            option: Опции стиля
            index: Индекс модели
            
        Returns:
            QComboBox: Редактор для ячейки
        """
        editor = QComboBox(parent)
        
        # Проверяем конфигурацию для данной колонки
        if index.column() in self._column_configs:
            editor.addItems(self._column_configs[index.column()])
        else:
            # Используем значения по умолчанию для известных колонок
            if index.column() == 1:  # Тип оружия
                editor.addItems(self.WEAPON_TYPES)
            elif index.column() == 3:  # Скрытность
                editor.addItems(self.CONCEALMENT_OPTIONS)
            elif index.column() == 4:  # Доступность
                editor.addItems(self.AVAILABILITY_OPTIONS)
            elif index.column() == 7:  # Надежность
                editor.addItems(self.RELIABILITY_OPTIONS)
        
        editor.setEditable(True)
        return editor
    
    def setColumnConfig(self, column: int, options: list):
        """
        Устанавливает конфигурацию для колонки
        
        Args:
            column: Индекс колонки
            options: Список опций для ComboBox
        """
        self._column_configs[column] = options
