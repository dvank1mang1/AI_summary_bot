import asyncio
import json
from pathlib import Path
from i18n import t
import re
from html import escape

from aiogram import Bot, types, Router, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from storage.user_preferences import get_user_language, get_user_size
from ai_summary_bot.translate import translation
from ai_summary_bot.format import format_article
from ai_summary_bot.summarizer import summarize_with_gpt
from ai_summary_bot.search import serpapi_search, format_snippets

router = Router()


def sanitize_html(text: str) -> str:

    escaped = escape(text)

    escaped = re.sub(r"&lt;b&gt;(.*?)&lt;/b&gt;", r"<b>\1</b>", escaped, flags=re.IGNORECASE | re.DOTALL)
    escaped = re.sub(r"&lt;a href=&quot;(.*?)&quot;&gt;(.*?)&lt;/a&gt;", r"<a href=\"\1\">\2</a>", escaped,flags=re.IGNORECASE | re.DOTALL,)
    return escaped

async def send_news_to_user(bot: Bot, user_id: int, article: dict):
   
    lang = get_user_language(user_id)

    raw_body = article.get("summary") or article.get("text") or ""

    summary = await summarize_with_gpt(
        base_text=raw_body,
        size = "normal",
        additional_context=None
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

    formatted_message = sanitize_html(formatted_message)

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



