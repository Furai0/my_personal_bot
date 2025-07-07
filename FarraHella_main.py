import asyncio
import logging
import time
import app.keyboards as kb
from aiogram import Bot, Dispatcher
import config

from app.handlers import Router, user_router
from app import notifications

bot = Bot(token=config.TOKEN)
dp = Dispatcher()
#
# bot pool
async def main():
    dp.include_router(user_router)

    await asyncio.gather(
        notifications.on_startup(),
        dp.start_polling(bot)

                         )

if __name__ == '__main__':
    # loggirovanie!!
    # LOGGINGLOGGINGLOGGINGLOGGINGLOGGINGLOGGINGLOGGINGLOGGINGLOGGINGLOGGING
    logging.basicConfig(level=logging.INFO
)
    # LOGGINGLOGGINGLOGGINGLOGGINGLOGGINGLOGGINGLOGGINGLOGGINGLOGGINGLOGGING
    asyncio.run(main())