"""
Настройка логирования для приложения
"""

import logging
from pathlib import Path


def setup_logger(
    log_file: str = 'cyberpunk_sheet.log',
    level: int = logging.ERROR,
    format_string: str = None
) -> logging.Logger:
    """
    Настраивает и возвращает логгер для приложения
    
    Args:
        log_file: Имя файла логов
        level: Уровень логирования
        format_string: Формат сообщений лога
        
    Returns:
        Настроенный логгер
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Создаем logger для приложения
    logger = logging.getLogger('cyberpunk_app')
    logger.setLevel(level)
    
    # Проверяем, есть ли уже обработчики
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(format_string))
        logger.addHandler(file_handler)
        
        # Console handler (для отладки)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(logging.Formatter(format_string))
        logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = 'cyberpunk_app') -> logging.Logger:
    """
    Возвращает существующий логгер или создает новый
    
    Args:
        name: Имя логгера
        
    Returns:
        Логгер с указанным именем
    """
    return logging.getLogger(name)


class LoggerMixin:
    """
    Миксин для добавления логгера в классы
    
    Пример использования:
        class MyClass(LoggerMixin):
            def my_method(self):
                self.logger.info("Message")
    """
    
    @property
    def logger(self) -> logging.Logger:
        """Возвращает логгер для класса"""
        if not hasattr(self, '_logger'):
            self._logger = get_logger(self.__class__.__name__)
        return self._logger
