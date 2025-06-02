from aiogram import Router, F, types
from aiogram.types import Message,BotCommand, BotCommandScopeChat
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import json
from pathlib import Path
from html import escape
import re


from states.settings import Settings
from keyboards.language import get_language_keyboard
from keyboards.frequency import get_frequency_keyboard
from storage.user_preferences import get_user_language, set_user_language, set_user_frequency, set_user_size
from handlers.news_sender import sanitize_html
from ai_summary_bot.translate import translation
from ai_summary_bot.search import serpapi_search
from ai_summary_bot.search import format_snippets
from ai_summary_bot.summarizer import summarize_with_gpt
from ai_summary_bot.format import format_article
from i18n import t

router = Router()

ARTICLES_PATH = Path("articles.json")

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




@router.callback_query(lambda c: c.data and c.data.startswith("more:"))
async def handle_more_callback(cq: types.CallbackQuery):
    await cq.answer() 
    bot = cq.bot
    data = cq.data
    if not data.startswith("more:"):
        await cq.answer()
        return

    url = data.split(":", 1)[1]
    all_articles = json.loads(ARTICLES_PATH.read_text("utf-8"))
    target_article = None
    for art in all_articles:
        if art.get("url") == url:
            target_article = art
            break
    

    raw_title = target_article.get("title", "")
    raw_text = target_article.get("text", "")
    date = target_article.get("date", "")

    user_id = cq.from_user.id
    lang = get_user_language(user_id) or "ru"

    title_translated = await translation(raw_title, target_lang = lang)
    query_for_search = raw_title if raw_title else raw_text[:100]
    serp = await serpapi_search(query_for_search, limit=3)
    snippets = format_snippets(serp)

    summary_extend = await summarize_with_gpt(
        base_text = raw_text,
        size = "extended",
        additional_context = snippets
    )

    body_translated = await translation(summary_extend, target_lang = lang)

    formatted_extend = format_article(
        title = title_translated,
        summary = body_translated,
        source = url,
        time = date
    )
    clean = sanitize_html(formatted_extend)

    await cq.message.answer(clean, parse_mode="HTML")