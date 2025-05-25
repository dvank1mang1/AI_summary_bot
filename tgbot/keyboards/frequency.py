from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from i18n import t

def get_frequency_keyboard(lang: str):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "daily"))],
            [KeyboardButton(text=t(lang, "semiweekly"))],
            [KeyboardButton(text=t(lang, "weekly"))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=t(lang, "frequency_prompt")
    )
