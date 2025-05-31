import asyncio
from aiogram import Bot
from storage.user_preferences import get_user_language, get_user_size
from ai.translate import translation
from ai.format import format_article
from ai.summarizer import summarize_with_gpt

async def send_news_to_user(bot: Bot, user_id: int, article: dict):
   
    lang = get_user_language(user_id)
    size = get_user_size(user_id)

    raw_body = article.get("summary") or article.get("text") or ""

    additional_context = article.get("external_context")

    summary = await summarize_with_gpt(
        base_text=raw_body,
        size=size,
        additional_context=additional_context
    )

    translated_summary = translation(summary, target_lang=lang)

    title_src = article.get("title", "")
    translated_title = translation(title_src, target_lang=lang)
   
    formatted_message = format_article(
        title=translated_title,
        summary=translated_summary,
        source=article.get("url", ""),
        time=article.get("date", "")
    )

    await bot.send_message(
        chat_id=user_id,
        text=formatted_message,
        parse_mode="HTML"
    )
