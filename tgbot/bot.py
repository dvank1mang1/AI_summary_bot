import asyncio
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher,types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from dotenv import load_dotenv
from handlers import commands
from aiogram.types import BotCommand
from handlers.commands import router
from storage.user_preferences import get_user_language
from i18n import t
from scheduler import start_scheduler
from storage.user_preferences import get_all_user_ids



load_dotenv()

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    lang =get_user_language(message.from_user.id)
    if lang not in ["ru", "en"]:
        lang = "ru"

    await message.answer(t(lang, "start_message"))

async def main():

    await bot.set_my_description(
        description=t("ru", "bot_description"),
        language_code="ru"
    )
    await bot.set_my_description(
        description=t("en", "bot_description"),
        language_code="en"
    )

    await bot.set_my_short_description(
        short_description=t("ru", "bot_short"),
        language_code="ru"
    )
    await bot.set_my_short_description(
        short_description=t("en", "bot_short"),
        language_code="en"
    )

    dp.include_router(router)
    print("Bot is working.")

    start_scheduler(bot) 

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
