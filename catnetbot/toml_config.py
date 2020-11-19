"""
Небольшой модуль для управления конфигурацией.
Написан давно (2 года назад) и все время мной использовался.
Является говнокодом, но работает
- Merded
"""

import os
import sys
from shutil import copyfile

import tomlkit
from loguru import logger


FILE_NAME = "config.toml"
CONFIG_PATH = f"{FILE_NAME}"


def copy_template():
    """
    Копирует файл-шаблон
    """

    try:
        copyfile("config_template.toml", CONFIG_PATH)
    except:
        logger.exception("Не удалось скопировать файл-шаблон.")
        sys.exit(1)


def config_find():
    """
    Если конфиг не создан, создает
    """

    if not os.path.exists(CONFIG_PATH):

        copy_template()
        config_find()

        logger.warning("Конфигурация была создана.")
        sys.exit(0)
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, encoding = "utf-8") as file:
            return file


def load_config():
    """
    Возвращает конфиг
    config.toml
    [test]
    abc = 123

    # >>> import toml_config
    # >>> conf = toml_config.load_config()
    # >>> conf["test"]["abc"]
    123
    """

    config_find()

    with open(CONFIG_PATH, encoding = "utf-8") as file:
        config = tomlkit.parse(file.read())
        return config
