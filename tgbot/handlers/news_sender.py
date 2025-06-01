import asyncio
import json
from pathlib import Path
from i18n import t

from aiogram import Bot, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from storage.user_preferences import get_user_language, get_user_size
from ai_summary_bot.translate import translation
from ai_summary_bot.format import format_article
from ai_summary_bot.summarizer import summarize_with_gpt
from ai_summary_bot.search import serpapi_search, format_snippets


ARTICLES_PATH = Path("articles.json")

async def send_news_to_user(bot: Bot, user_id: int, article: dict):
   
    lang = get_user_language(user_id)

    raw_body = article.get("summary") or article.get("text") or ""

    additional_context = article.get("external_context")

    summary = await summarize_with_gpt(
        base_text=raw_body,
        size = "normal",
        additional_context=additional_context
    )

    translated_summary = await translation(summary, target_lang=lang)

    raw_title = article.get("title", "")
    translated_title = await translation(raw_title, target_lang=lang)
   
    formatted_message = format_article(
        title=translated_title,
        summary=translated_summary,
        source=article.get("url", ""),
        time=article.get("date", "")
    )

    url = article.get("url", "")

    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text = t(lang, "more"), callback_data = f"more:{url}")
    markup = kb_builder.as_markup()


    await bot.send_message(
        chat_id=user_id,
        text=formatted_message,
        reply_markup=markup,
        parse_mode="HTML"
    )

async def handle_more_callback(bot: Bot, callback: types.CallbackQuery):
    data = callback.data
    if not data.startswith("more:"):
        await callback.answer()
        return
    url = data[len("more:"):]

    all_articles = json.loads(ARTICLES_PATH.read_text("utf-8"))
    target_article = None
    for art in all_articles:
        if art.get("url") == url:
            target_article = art
            break
    

    raw_title = target_article.get("title", "")
    raw_text = target_article.get("text", "")
    date = target_article.get("date", "")

    user_id = callback.from_user.id
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
        time = data
    )

    await callback.message.answer(formatted_extend, parse_mode = "HTML")
    await callback.answer()

