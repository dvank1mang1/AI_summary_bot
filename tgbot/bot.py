import asyncio
import os
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher,types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("👋 Hello! I'm your AI news bot.")

async def main():
    # You’ll register handlers here later
    print("Bot is working.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
