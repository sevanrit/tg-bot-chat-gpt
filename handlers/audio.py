from keyboards import kb_start
from aiogram import types, Dispatcher
from create_bot import dp, bot, database, langs
from config import config
from AI import gpt
from loguru import logger as lg
from openai import OpenAI
import os

from pydub import AudioSegment


from state_machine_modul import BotStatesGroup
from dependencies.support_funcs import get_text, clean, edit

client = OpenAI(api_key=config["APIToken"])


@lg.catch()
async def audio(message: types.Message) -> None:
    chat_id = message.chat.id
    await BotStatesGroup.in_progress.set()
    msg = await bot.send_message(chat_id, await get_text("text.waitAnswer", chat_id))
    database.update(chat_id, "users", "last_msg_id", msg.message_id)
    # FILE
    try:
        voice = message.voice
        voice_file_id = voice.file_id
        voice_file = await bot.get_file(voice_file_id)

        voice_path = os.path.join("voices", f"{chat_id}.oga")
        await voice_file.download(voice_path)

        response = client.audio.transcriptions.create(
            model="whisper-1", file=open(voice_path, "rb")
        )
        req_message = response.text

    except Exception as ex:
        lg.error(f"An error occurred, please try again:\n\n`{ex}`")
    finally:
        os.remove(voice_path)
    database.update(chat_id, "users", "last_msg_id", msg.message_id)
    try:
        request = await clean(req_message)
        await gpt.update_user_file(chat_id, request)
        answer = await gpt.get_response_gpt_3_5(chat_id)
        await edit(
            chat_id,
            database.read(chat_id, "users", "last_msg_id"),
            answer,
        )

    except Exception as e:
        if config.get("LogsON", False):
            lg.error(f"{e} from id: {chat_id}")
        await edit(
            chat_id,
            database.read(chat_id, "users", "last_msg_id"),
            await get_text("text.largeContext", chat_id),
        )
    await BotStatesGroup.free.set()


@lg.catch()
async def audio_trash(message: types.Message) -> None:
    chat_id = message.chat.id
    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(
        audio,
        content_types="voice",
        state=[BotStatesGroup.free, BotStatesGroup.gpt, None],
    )
    dp.register_message_handler(
        audio_trash,
        content_types="voice",
        state=[BotStatesGroup.in_progress, BotStatesGroup.choose_lang],
    )
