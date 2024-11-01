from keyboards import kb_start

from aiogram import types, Dispatcher
from create_bot import dp, bot, database, langs, users_langs
from jmespath import search
from config import config
from AI import gpt
from loguru import logger as lg
import datetime
import openai
import asyncio
from random import randint

from jmespath import search
from random import randint


async def get_text(code, id):
    if users_langs.get(id) == None:
        users_langs[id] = database.read(id, "users", "lang")

    return search(code, langs[users_langs[id]])


# Очистить строку для записи в файл ChatGPT
async def clean(string):
    return string.replace("'", "").replace('"', "").replace("\n", "").replace("/", "//")


# Изменить текст
async def edit(chat_id, message_id, text, reply_markup=None, parse_mode=None):
    msg = await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode,
        disable_web_page_preview=True,
    )
    database.update(chat_id, "users", "last_msg_id", msg.message_id)
