from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from i18n import t

def get_language_keyboard(lang: str):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "language_ru"))],
            [KeyboardButton(text=t(lang, "language_en"))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=t(lang, "language_prompt")
    )
