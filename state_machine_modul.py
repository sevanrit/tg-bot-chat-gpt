from aiogram.dispatcher.filters.state import StatesGroup, State


class BotStatesGroup(StatesGroup):
    free = State()
    in_progress = State()
    choose_lang = State()
    gpt = State()
    get_name = State()
    get_services = State()
