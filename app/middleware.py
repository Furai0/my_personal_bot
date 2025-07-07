from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable

import os

import config
import subprocess
import time

import config

from FarraHella_main import bot
class MessagesLog(BaseMiddleware):
    async def __call__(self,
                       handler: Callable [[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:

        result = await handler(event, data)

        user_id = event.chat.id
        user_name = event.from_user.full_name
        user_text = event.text
        message_date = event.date

        if config.fast_logs and config.full_logs == False:
            None
        if config.fast_logs:
            # fast logs
            try:
                os.makedirs(f'logs/chat_logs/fast_logs/{user_name}')
            except FileExistsError:
                None

            if not os.path.exists(f'logs/chat_logs/fast_logs/{user_name}/{user_name}'):
                with open(f'logs/chat_logs/fast_logs/{user_name}/{user_name}', "w", encoding="utf-8") as file:
                    file.write(f" \n{message_date}, {user_name}, {user_id}, {user_text}\n")

            else:
                with open(f'logs/chat_logs/fast_logs/{user_name}/{user_name}', 'a', encoding='utf-8') as file:
                    file.write(f" \n{message_date}, {user_name}, {user_text}\n")

            print('user message fast_logged')


        # full logs
        if config.full_logs:
            if not os.path.exists(f'logs/chat_logs/full_logs/{user_id}'):
                time.sleep(5)
                for admin in config.admins:
                    await bot.send_message(text=f'new user {user_name} ', chat_id=admin)

            try:
                os.makedirs(f'logs/chat_logs/full_logs/{user_id}')
            except FileExistsError:
                None

            if not os.path.exists(f'logs/chat_logs/full_logs/{user_id}/{user_id}'):
                with open(f'logs/chat_logs/full_logs/{user_id}/{user_id}', "w", encoding="utf-8") as file:
                    file.write(f'{event}\n{data}')

            else:
                with open(f'logs/chat_logs/full_logs/{user_id}/{user_id}', 'a', encoding='utf-8') as file:
                    file.write(f'\n{event}\n{data}')
            print('user message full_logged')

