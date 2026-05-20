"""
Декораторы и функции валидации
"""

from functools import wraps
from PyQt5.QtWidgets import QMessageBox


def validate_int_field(func):
    """
    Декоратор для валидации числовых полей
    
    Перехватывает ValueError и показывает предупреждение пользователю
    
    Args:
        func: Функция, которую нужно обернуть
        
    Returns:
        Обернутая функция с обработкой ошибок
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except ValueError:
            QMessageBox.warning(
                self, 
                "Ошибка", 
                "Некорректное числовое значение"
            )
            return 0
    
    return wrapper


def validate_non_empty(func):
    """
    Декоратор для проверки непустых значений
    
    Args:
        func: Функция, которую нужно обернуть
        
    Returns:
        Обернутая функция с проверкой на пустоту
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if not result or (isinstance(result, str) and not result.strip()):
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Поле не должно быть пустым"
            )
        return result
    
    return wrapper


def confirm_action(message: str = "Вы уверены?"):
    """
    Декоратор для подтверждения действий
    
    Args:
        message: Текст сообщения подтверждения
        
    Returns:
        Декоратор для функций
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            reply = QMessageBox.question(
                self,
                'Подтверждение',
                message,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                return func(self, *args, **kwargs)
            return None
        
        return wrapper
    return decorator
