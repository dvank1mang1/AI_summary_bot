from aiogram import Bot
from storage.user_preferences import get_user_language
from i18n import t
from ai.translate import translation
from ai.format import format_article 

async def send_news_to_user(bot: Bot, user_id: int, article: dict):
    lang = get_user_language(user_id)


    translated_summary = translation(article["summary"], target_lang=lang)

    formatted = format_article(
        title=article.get("title", ""),
        summary=translated_summary,
        source=article.get("url", ""),
        time=article.get("date", "")
    )

    await bot.send_message(chat_id=user_id, text=formatted, parse_mode="HTML")
