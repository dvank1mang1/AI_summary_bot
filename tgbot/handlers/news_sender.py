from __future__ import annotations

import json
from pathlib import Path

from aiogram import Router, types, F, Bot
from aiogram.filters import Command

from storage.user_preferences import get_user_language
from i18n import t
from ai.translate import translation
from ai.format import format_article

from ai_summary_bot.parsing import collect_articles
from ai_summary_bot.moderation import publish_articles
from ai_summary_bot.search import serpapi_search

router = Router()

@router.message(Command("daily"))
async def cmd_daily(msg: types.Message):
    await msg.answer("⏳ Готовлю свежую новость…")
    json_path = await collect_articles()
    articles = json.loads(Path(json_path).read_text("utf-8"))
    if not articles:
        await msg.answer("🙈 Сегодня подходящих новостей нет.")
        return
    article = articles[0]
    await send_news_to_user(msg.bot, msg.from_user.id, article)   # 🔸
    await msg.answer("✅ Опубликовано!")



@router.callback_query(F.data.startswith("more:"))
async def cb_more(cq: types.CallbackQuery):
    idx = int(cq.data.split(":", 1)[1])
    arts = json.loads(Path("articles.json").read_text("utf-8"))
    art = arts[idx]
    query = art.get("title") or art["text"][:120]

    try:
        serp = await serpapi_search(query, limit=3)
    except Exception as e:
        await cq.message.answer(f"⚠️ {e}")
        await cq.answer(); return

    if not serp:
        await cq.message.answer("🙈 Ничего не нашлось."); await cq.answer(); return

    text = f"<b>{query}</b>\n\n"
    for title, link, snip in serp:
        text += f"🔗 <a href=\"{link}\">{title}</a>\n{snip}\n\n"

    await cq.message.answer(text, parse_mode="HTML", disable_web_page_preview=False)
    await cq.answer()


async def send_news_to_user(bot: Bot, user_id: int, article: dict):
    lang = get_user_language(user_id)
    title_src = article.get("title", "")
    title = translation(title_src, target_lang=lang)
    raw_body = article.get("summary") or article.get("text") or ""
    body = translation(raw_body, target_lang=lang)
    formatted = format_article(
        title=title,
        summary=body,
        source=article.get("url", ""),
        time=article.get("date", ""),
    )

    await bot.send_message(chat_id=user_id,
                           text=formatted,
                           parse_mode="HTML")
