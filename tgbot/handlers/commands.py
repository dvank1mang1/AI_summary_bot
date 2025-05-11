from keyboards.language import language_keyboard
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.settings import Settings
from handlers import commands
from keyboards.frequency import frequency_keyboard

router = Router()

@router.message(Command("language"))
async def choose_language(message: Message, state: FSMContext):
    await message.answer(
        "🌍 Choose your preferred language:",
        reply_markup=language_keyboard
    )
    await state.set_state(Settings.choosing_language)


@router.message(Settings.choosing_language)
async def save_language(message: Message, state: FSMContext):
    lang_map = {
        "english": "English",
        "russian": "Russian",
    }

    user_input = message.text.lower()
    lang = lang_map.get(user_input)

    if not lang:
        await message.answer("❌ Please use the buttons to choose a valid language.")
        return
    await state.clear()
    await message.answer(f"✅ Language set to <b>{lang}</b>.", reply_markup=None)




@router.message(Command("frequency"))
async def choose_frequency(message: Message, state: FSMContext):
    await message.answer(
        "⏱ How often should I send you news?",
        reply_markup=frequency_keyboard
    )
    await state.set_state(Settings.choosing_frequency)

@router.message(Settings.choosing_frequency)
async def save_frequency(message: Message, state: FSMContext):
    freq_map = {
        "as soon as possible": "ASAP",
        "daily": "Daily",
        "semiweekly": "Semiweekly",
        "weekly": "Weekly"
    }

    user_input = message.text.lower()
    freq = freq_map.get(user_input)

    if not freq:
        await message.answer("❌ Please use the buttons to choose a valid option.")
        return

    
    await state.clear()
    await message.answer(f"✅ Frequency set to <b>{freq}</b>.", reply_markup=None)