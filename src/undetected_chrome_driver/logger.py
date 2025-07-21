"""Настройки и инициализация логера"""

import logging

LOGGER_NAME = 'Webdriver'
# LOGS_DIR = 'logs'
# LOG_FILE = f'{LOGGER_NAME}.log'
LOGGING_LEVEL = logging.DEBUG

logger: logging.Logger = logging.getLogger(name=LOGGER_NAME)
logger.setLevel(LOGGING_LEVEL)

# Создаем консольный обработчик и устанавливаем для него уровень логирования
console_handler = logging.StreamHandler()
console_handler.setLevel(LOGGING_LEVEL)

# Создаем форматер и добавляем его в обработчик
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Добавляем обработчик логеру
logger.addHandler(console_handler)

# Файловое логирование
# file_handler = logging.FileHandler(os.path.join(LOGS_DIR, f'{LOG_FILE}'))
# file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(formatter)
#
# logger.addHandler(file_handler)