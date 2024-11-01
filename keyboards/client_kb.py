from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from create_bot import langs, database
from jmespath import search


# Get text
def get_text(code: str, id: int) -> str:
    return search(code, langs[database.read(id, "users", "lang")])


# Start Keyboard
def kb_start(id):
    kb_start = ReplyKeyboardMarkup()

    kb_start.row(get_text("buts.noName", id))
    kb_start.row(get_text("buts.tellAboutService", id))
    kb_start.row(get_text("buts.freeAdvice", id))
    kb_start.row(get_text("buts.writeMe", id))

    return kb_start


def kb_no_name(id):
    kb_no_name = ReplyKeyboardMarkup()

    kb_no_name.row(get_text("buts.tellAboutService", id))
    kb_no_name.row(get_text("buts.freeAdvice", id))
    kb_no_name.row(get_text("buts.writeProblem", id))
    return kb_no_name


def kb_services(id):
    kb_services = ReplyKeyboardMarkup()

    kb_services.row(get_text("buts.digitalMarketing", id))
    kb_services.row(get_text("buts.contentMarketing", id))
    kb_services.row(get_text("buts.webAndMobile", id))
    kb_services.row(get_text("buts.resAndStrats", id))
    kb_services.row(get_text("buts.otherServices", id))
    kb_services.row(get_text("buts.idk", id))
    kb_services.row(get_text("buts.mainMenu", id))
    return kb_services


# Start Keyboard
def kb_languages() -> InlineKeyboardMarkup:
    kb_languages_b1 = InlineKeyboardButton("Rus🇷🇺", callback_data="rus")
    kb_languages_b2 = InlineKeyboardButton("Eng🏴󠁧󠁢󠁥󠁮󠁧󠁿", callback_data="eng")
    kb_languages_b3 = InlineKeyboardButton("Ger🇩🇪", callback_data="ger")
    kb_languages_b4 = InlineKeyboardButton("Pol🇵🇱", callback_data="pol")

    kb_languages = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    kb_languages.row(kb_languages_b1).insert(kb_languages_b2).row(
        kb_languages_b3
    ).insert(kb_languages_b4)

    return kb_languages


def kb_main_menu(id):
    kb_main_menu = ReplyKeyboardMarkup()

    kb_main_menu.row(get_text("buts.mainMenu", id))

    return kb_main_menu
