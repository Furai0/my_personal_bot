import subprocess
import time

import config
import FarraHella_main
import app.hm


async def on_startup():
    for admin in config.admins:
        time.sleep(5)
        await FarraHella_main.bot.send_message(text='Bot started', chat_id=admin)


