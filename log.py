import logging
class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Базовый формат сообщения
        base_format = '{asctime} {levelname} {message}'
        # Добавление пути к источнику для WARNING и выше
        if record.levelno >= logging.WARNING:
            base_format += ' {pathname}:{lineno}'
        # Добавление стека ошибки для ERROR и CRITICAL
        if record.levelno >= logging.ERROR:
            base_format += '\n{exc_info}'
        self._style._fmt = base_format
        return super().format(record)

class ErrorOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.ERROR

# Настройка обработчика для консоли
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(CustomFormatter())

# Добавление обработчика к логгеру по умолчанию
root_logger = logging.getLogger()
root_logger.addHandler(console_handler)
