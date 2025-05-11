from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

frequency_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="As soon as possible")],
        [KeyboardButton(text="Daily")],
        [KeyboardButton(text="Semiweekly")],
        [KeyboardButton(text="Weekly")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Choose update frequency"
)
