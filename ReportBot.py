import asyncio
import logging

from aiogram import Bot, Dispatcher

from core.settings import settings
from handlers import main_handlers, pivot_data_menu, settings_report

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(settings.bots.bot_token)
    dp = Dispatcher()
    dp.include_routers(main_handlers.router)
    dp.include_routers(pivot_data_menu.router)
    dp.include_routers(settings_report.router)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except KeyboardInterrupt as mess:
        print(str(mess))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print(str(e))
