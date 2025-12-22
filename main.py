import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config import BOT_TOKEN
from app.handlers import router
from app.services.payments import init_db
from app.services.crm import init_crm_db


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    init_db()
    init_crm_db()

    bot=Bot(token=BOT_TOKEN)
    dp=Dispatcher()
    dp.include_router(router)

    logging.info("Bot is running. Press Ctrl+C to stop.")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())