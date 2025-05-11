from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="English")],
        [KeyboardButton(text="Russian")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Choose your language"
)
