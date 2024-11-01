from aiogram import types, Dispatcher
from keyboards import kb_start
from create_bot import dp, bot, database, langs, users_langs
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


@lg.catch()
async def choose_lang(call: types.CallbackQuery) -> None:
    chat_id = call.message.chat.id

    database.update(chat_id, "users", "lang", call.data)
    users_langs[chat_id] = call.data
    await edit(
        chat_id,
        database.read(chat_id, "users", "last_msg_id"),
        await get_text("text.choose_lang_ok", chat_id),
    )
    await bot.send_message(
        chat_id,
        await get_text("text.start_msg", chat_id),
        reply_markup=kb_start(chat_id),
    )
    await bot.answer_callback_query(callback_query_id=call.id)
    await BotStatesGroup.free.set()


# Handlers register
def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        choose_lang, text=["rus", "eng", "ger", "pol"], state=BotStatesGroup.choose_lang
    )
