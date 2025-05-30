from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from i18n import t

def get_size_keyboard(lang: str):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "size_normal"))],
            [KeyboardButton(text=t(lang, "size_extended"))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=t(lang, "size_prompt")
    )
