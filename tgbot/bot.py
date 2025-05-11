import asyncio
import os
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher,types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from dotenv import load_dotenv
from handlers import commands
from aiogram.types import BotCommand
from handlers.commands import router

load_dotenv()

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("👋 Hello! I'm your AI news bot.")

async def main():
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="language", description="Change language"),
        BotCommand(command="frequency", description="Change frequency of news"),
    ]
    await bot.set_my_commands(commands)


    dp.include_router(router)
    print("Bot is working.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
