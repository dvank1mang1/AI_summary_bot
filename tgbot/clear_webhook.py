import asyncio
from aiogram import Bot
from config import BOT_TOKEN

async def clear_webhook():
    bot = Bot(token=BOT_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()

asyncio.run(clear_webhook())
