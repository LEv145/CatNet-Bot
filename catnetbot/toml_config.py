"""
Небольшой модуль для управления конфигурацией.
Нaписан давно (2 года назад) и все время мной использовался.
Является говнокодом, но работает
"""

import os
from shutil import copyfile
import sys
import tomlkit
from loguru import logger as l


FILE_NAME = "config.toml"
CONFIG_PATH = f"{FILE_NAME}"


def copy_template():
    """Копирует файл-шаблон"""
    try:
        copyfile("config_template.toml", CONFIG_PATH)
    except:
        l.exception("Не удалось скопировать файл-шаблон.")
        sys.exit(1)


def config_find():
    """Если конфиг не создан, создает"""
    if not os.path.exists(CONFIG_PATH):
        copy_template()
        config_find()
        l.warning("Конфигурация была создана.")
        sys.exit(0)
    if os.path.exists(CONFIG_PATH):
        f = open(CONFIG_PATH, "r")
    return f


def load_config():
    """Возвращает конфиг
    config.toml
    [test]
    abc = 123

    # >>> import toml_config
    # >>> conf = toml_config.load_config()
    # >>> conf["test"]["abc"]
    123
    """

    with open(CONFIG_PATH, encoding = "utf-8") as f:
        conf = tomlkit.parse(f.read())
        return conf
