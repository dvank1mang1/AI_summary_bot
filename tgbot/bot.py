import asyncio
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import BotCommand

from dotenv import load_dotenv
from config import BOT_TOKEN
from i18n import t
from storage.user_preferences import get_user_language, get_all_user_ids
from scheduler import start_scheduler
from handlers.commands import router as commands_router
from handlers.news_sender import handle_more_callback


load_dotenv()

bot = Bot(token=BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    lang = get_user_language(message.from_user.id) or "ru"
    await message.answer(t(lang, "start_message"))


async def main():
    await bot.delete_webhook()

    await bot.set_my_description(t("ru", "bot_description"), "ru")
    await bot.set_my_description(t("en", "bot_description"), "en")
    await bot.set_my_short_description(t("ru", "bot_short"), "ru")
    await bot.set_my_short_description(t("en", "bot_short"), "en")
    dp.include_router(commands_router)

    dp.callback_query.register(handle_more_callback, lambda c: c.data and c.data.startswith("more:"))

    start_scheduler(bot)

    print("Bot is working.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
