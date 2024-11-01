from keyboards import kb_start, kb_languages

from aiogram import types, Dispatcher
from create_bot import dp, bot, database, langs
from jmespath import search
from config import config
from AI import gpt
from loguru import logger as lg
from datetime import datetime
import openai
import asyncio
from random import randint

from state_machine_modul import BotStatesGroup
from dependencies.support_funcs import get_text, clean, edit


# Команда /admin
@lg.catch()
async def command_admin(message: types.Message) -> None:
    chat_id = message.chat.id
    if chat_id in config["AdminList"]:
        text = (
            f"Всего пользователей: {database.get_users_count()}\n"
            f"Запросов сегодня: {database.read_admin('requests_today')}\n"
            f"Запросов за все время: {database.read_admin('requests_all')}\n"
            f"Потрачено токенов сегодня: {database.read_admin('tokens_today')}\n"
            f"Потрачено токенов за все время: {database.read_admin('tokens_all')}\n"
        )
        await bot.send_message(chat_id, text)
    else:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


# Команда /lang
@lg.catch()
async def command_lang(message: types.Message) -> None:
    chat_id = message.chat.id
    msg = await bot.send_message(
        chat_id,
        await get_text("text.choose_lang", chat_id),
        reply_markup=kb_languages(),
    )
    database.update(chat_id, "users", "last_msg_id", msg.message_id)
    await BotStatesGroup.choose_lang.set()


# Команда /start
@lg.catch()
async def command_start(message: types.Message) -> None:
    chat_id = message.chat.id
    await gpt.create_file(chat_id)
    if database.isReg(chat_id):
        await bot.send_message(
            chat_id,
            await get_text("text.start_msg", chat_id),
            reply_markup=kb_start(chat_id),
        )
        await BotStatesGroup.free.set()
    else:
        database.recording(id=chat_id, name=message.from_user.first_name)
        msg = await bot.send_message(
            chat_id,
            await get_text("text.choose_lang", chat_id),
            reply_markup=kb_languages(),
        )
        database.update(chat_id, "users", "last_msg_id", msg.message_id)
        await BotStatesGroup.choose_lang.set()


# Команда /restart
@lg.catch()
async def command_restart(message: types.Message) -> None:
    chat_id = message.chat.id
    await gpt.create_file(chat_id)  # Обновляем файл юзера

    await bot.send_message(chat_id, await get_text("text.restart", chat_id))
    await BotStatesGroup.free.set()


# Handlers register
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(
        command_start, commands=["start"], state=[None, BotStatesGroup.free]
    )  # Command /start
    dp.register_message_handler(
        command_restart, commands=["restart"], state=[None, BotStatesGroup.free]
    )  # Command /restart
    dp.register_message_handler(
        command_lang, commands=["lang"], state=[None, BotStatesGroup.free]
    )  # Command /lang
    dp.register_message_handler(
        command_admin, commands=["admin"], state=[None, BotStatesGroup.free]
    )  # Command /lang
