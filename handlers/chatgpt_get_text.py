from keyboards import kb_start, kb_no_name, kb_main_menu, kb_services

from aiogram import types, Dispatcher
from create_bot import dp, bot, database, langs
from jmespath import search
from AI import gpt
from loguru import logger as lg
from datetime import datetime
import openai
import asyncio
from random import randint

from state_machine_modul import BotStatesGroup
from dependencies.support_funcs import get_text, clean, edit

# Модуль с функциями для статистики
"""from dependencies.statistic import update_requests_count
from dependencies.support_funcs import inProgress, get_text, \
    editclean"""


# Прием сообщений
@lg.catch()
async def get_message_trash(message: types.Message):
    chat_id = message.chat.id
    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)


@lg.catch()
async def gpt_(chat_id, prompt):
    try:
        await BotStatesGroup.in_progress.set()
        msg = await bot.send_message(
            chat_id, await get_text("text.waitAnswer", chat_id)
        )
        database.update(chat_id, "users", "last_msg_id", msg.message_id)
        request = await clean(prompt)
        await gpt.update_user_file(chat_id, request)
        answer = await gpt.get_response_gpt_3_5(chat_id)
        await edit(
            chat_id,
            database.read(chat_id, "users", "last_msg_id"),
            answer,
        )

    except Exception as e:
        lg.error(f"{e} from id: {chat_id}")
        await edit(
            chat_id,
            database.read(chat_id, "users", "last_msg_id"),
            await get_text("text.largeContext", chat_id),
        )

    await BotStatesGroup.free.set()


# Прием сообщений
@lg.catch()
async def get_message_buts(message: types.Message):
    chat_id = message.chat.id

    if message.text == await get_text("buts.noName", chat_id):
        await bot.send_message(
            chat_id,
            await get_text("text.noName", chat_id),
            reply_markup=kb_no_name(chat_id),
        )

    elif message.text == await get_text("buts.tellAboutService", chat_id):
        await bot.send_message(
            chat_id,
            await get_text("text.tellAboutService", chat_id),
            reply_markup=kb_services(chat_id),
        )
    elif message.text == await get_text("buts.writeProblem", chat_id):
        await bot.send_message(
            chat_id,
            await get_text("text.freeAdvice", chat_id),
            reply_markup=kb_main_menu(chat_id),
        )
        await BotStatesGroup.gpt.set()
    elif message.text == await get_text("buts.freeAdvice", chat_id):
        await gpt_(message.chat.id, "Пришли мне любой полезный совет")
        await BotStatesGroup.gpt.set()
    elif message.text == await get_text("buts.writeMe", chat_id):
        await bot.send_message(chat_id, await get_text("text.getName", chat_id))
        await BotStatesGroup.get_name.set()

    elif message.text == await get_text("buts.mainMenu", chat_id):
        await gpt.create_file(chat_id)
        await bot.send_message(
            chat_id,
            await get_text("text.start_msg", chat_id),
            reply_markup=kb_start(chat_id),
        )
        await BotStatesGroup.free.set()

    # СЕРВИСЫ

    elif message.text == await get_text("buts.idk", chat_id):
        await message.reply_sticker(
            "CAACAgIAAxkBAAEZMwNldMHRtsPx3XlkS_zshLjI3yhZRQAC7igAAie7iUqSfGgisu9nWjME"
        )
        await BotStatesGroup.gpt.set()

    elif message.text == await get_text("buts.digitalMarketing", chat_id):
        await gpt_(
            message.chat.id,
            f"Расскажи про {await get_text('buts.digitalMarketing', chat_id)}",
        )
        await BotStatesGroup.gpt.set()
    elif message.text == await get_text("buts.contentMarketing", chat_id):
        await gpt_(
            message.chat.id,
            f"Расскажи про {await get_text('buts.contentMarketing', chat_id)}",
        )
        await BotStatesGroup.gpt.set()
    elif message.text == await get_text("buts.webAndMobile", chat_id):
        await gpt_(
            message.chat.id,
            f"Расскажи про {await get_text('buts.webAndMobile', chat_id)}",
        )
        await BotStatesGroup.gpt.set()
    elif message.text == await get_text("buts.resAndStrats", chat_id):
        await gpt_(
            message.chat.id,
            f"Расскажи про {await get_text('buts.resAndStrats', chat_id)}",
        )
        await BotStatesGroup.gpt.set()
    elif message.text == await get_text("buts.otherServices", chat_id):
        await bot.send_message(
            chat_id,
            await get_text("text.getServices", chat_id),
            reply_markup=kb_main_menu(chat_id),
        )
        await BotStatesGroup.get_services.set()

    else:
        await gpt_(message.chat.id, message.text)


@lg.catch()
async def get_services(message: types.Message):
    chat_id = message.chat.id
    if message.text == await get_text("buts.mainMenu", chat_id):
        await gpt.create_file(chat_id)
        await bot.send_message(
            chat_id,
            await get_text("text.start_msg", chat_id),
            reply_markup=kb_start(chat_id),
        )
        await BotStatesGroup.free.set()
    else:
        await gpt_(message.chat.id, f"Расскажи про сервисы - {message.text}")
        await BotStatesGroup.gpt.set()


@lg.catch()
async def get_name(message: types.Message):
    chat_id = message.chat.id
    if message.text == await get_text("buts.mainMenu", chat_id):
        await gpt.create_file(chat_id)
        await bot.send_message(
            chat_id,
            await get_text("text.start_msg", chat_id),
            reply_markup=kb_start(chat_id),
        )
        await BotStatesGroup.free.set()
    else:
        text = await get_text("text.writeMe", chat_id)
        await bot.send_message(
            chat_id, text.format(message.text), reply_markup=kb_no_name(chat_id)
        )
        database.update(chat_id, "users", "name", message.text)
        await BotStatesGroup.free.set()


# Handlers register
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(
        get_message_trash,
        state=[BotStatesGroup.in_progress, BotStatesGroup.choose_lang],
    )  # Receiving messages handler
    dp.register_message_handler(
        get_message_buts, state=[None, BotStatesGroup.free, BotStatesGroup.gpt]
    )
    dp.register_message_handler(get_services, state=BotStatesGroup.get_services)
    dp.register_message_handler(get_name, state=BotStatesGroup.get_name)
