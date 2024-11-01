from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from config import config
from loguru import logger as lg
from PostgreSQL import Database
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import json, asyncio

# Инициализация
bot = Bot(token=config["BotToken"])  # Бот
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)  # Диспатчер
database = Database()  # База Данных
lg.add("logs.log", format="{time} {level} {message}", level="INFO")  # Логи

users_langs = {}
# Подключение языков
with open(config["LangsDir"] + "rus.json", "r", encoding="utf-8") as f:
    js_rus = json.load(f)
with open(config["LangsDir"] + "eng.json", "r", encoding="utf-8") as f:
    js_eng = json.load(f)
with open(config["LangsDir"] + "ger.json", "r", encoding="utf-8") as f:
    js_ger = json.load(f)
with open(config["LangsDir"] + "pol.json", "r", encoding="utf-8") as f:
    js_pol = json.load(f)

# Создание словаря с языковыми файлами
langs = {"rus": js_rus, "eng": js_eng, "ger": js_ger, "pol": js_pol}
