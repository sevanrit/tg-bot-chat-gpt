from aiogram.utils import executor
from create_bot import dp, bot
from loguru import logger as lg
from handlers import chatgpt_get_text, commands, audio, choose_lang
from config import config
import asyncio
import datetime
import aioschedule


async def today_updates() -> None:
    database.update_requests_today(0)
    database.update_tokens_today(0)
    lg.info("SYSTEM - Today UPDATES")


async def everyday_tasks() -> None:
    aioschedule.every().day.at(config["UpdateTime"]).do(today_updates)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_) -> None:
    lg.info(f"Bot start polling")
    asyncio.create_task(everyday_tasks())


async def on_shutdown(_) -> None:
    lg.info(f"Bot stop polling")


commands.register_handlers(dp)
chatgpt_get_text.register_handlers(dp)
audio.register_handlers(dp)
choose_lang.register_handlers(dp)


if __name__ == "__main__":
    lg.info(f"SYSTEM - Try to start Bot")
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
