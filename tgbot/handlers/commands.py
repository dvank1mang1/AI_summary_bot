from aiogram import Router, F
from aiogram.types import Message,BotCommand, BotCommandScopeChat
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.settings import Settings
from keyboards.language import get_language_keyboard
from keyboards.frequency import get_frequency_keyboard
from keyboards.size import get_size_keyboard
from storage.user_preferences import get_user_language, set_user_language, set_user_frequency, set_user_size
from i18n import t

router = Router()


@router.message(Command("language"))
async def choose_language(message: Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    await message.answer(
        t(lang, "language_prompt"),
        reply_markup=get_language_keyboard(lang)
    )
    await state.set_state(Settings.choosing_language)

@router.message(Settings.choosing_language)
async def save_language(message: Message, state: FSMContext):
    text = message.text.lower()
    lang_map = {
        t("ru", "language_ru").lower(): "ru",
        t("en", "language_en").lower(): "en",
    }

    lang = lang_map.get(text)
    if not lang:
        fallback_lang = get_user_language(message.from_user.id)
        await message.answer(t(fallback_lang, "language_invalid"))
        return

    set_user_language(message.from_user.id, lang)
    await state.clear()

    await message.bot.set_my_commands([
        BotCommand(command="start", description=t(lang, "cmd_start")),
        BotCommand(command="language", description=t(lang, "cmd_language")),
        BotCommand(command="frequency", description=t(lang, "cmd_frequency")),
        BotCommand(command="size", description=t(lang, "cmd_size")),
    ], scope=BotCommandScopeChat(chat_id=message.chat.id))


    await message.answer(t(lang, "language_set", value=text), reply_markup=None)




@router.message(Command("frequency"))
async def choose_frequency(message: Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    await message.answer(
        t(lang, "frequency_prompt"),
        reply_markup=get_frequency_keyboard(lang)
    )
    await state.set_state(Settings.choosing_frequency)



@router.message(Settings.choosing_frequency)
async def save_frequency(message: Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)

    freq_map = {
        t(lang, "daily").lower(): "daily",
        t(lang, "semiweekly").lower(): "semiweekly",
        t(lang, "weekly").lower(): "weekly"
    }

    user_input = message.text.lower()
    freq = freq_map.get(user_input)

    if not freq:
        await message.answer(t(lang, "frequency_invalid"))
        return

    
    set_user_frequency(message.from_user.id, freq)
    await state.clear()
    await message.answer(t(lang, "frequency_set", value=user_input), reply_markup=None)


@router.message(Command("size"))
async def choose_size(message: Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    await message.answer(
        t(lang, "size_prompt"),
        reply_markup=get_size_keyboard(lang)
    )
    await state.set_state(Settings.choosing_size)

@router.message(Settings.choosing_size)
async def save_size(message: Message, state: FSMContext):
    lang = get_user_language(message.from_user.id)
    
    size_map = {
        t(lang, "size_normal").lower(): "normal",
        t(lang, "size_extended").lower(): "extended"
    }

    user_input = message.text.lower()
    size = size_map.get(user_input)

    if not size:
        await message.answer(t(lang, "size_invalid"))
        return

    set_user_size(message.from_user.id, size)
    await state.clear()
    await message.answer(t(lang, "size_set", value = user_input), reply_markup=None)
