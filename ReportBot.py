import asyncio
import logging

from aiogram import Bot, Dispatcher

from core.settings import settings
from handlers import handlers_bot

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(settings.bots.bot_token)
    dp = Dispatcher()
    dp.include_routers(handlers_bot.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
