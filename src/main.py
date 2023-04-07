import asyncio
import os

import aiohttp
from aiogram import Bot, Dispatcher, types

from services.salary_aggregator import handle_message


async def main():
    async with aiohttp.ClientSession() as session:
        bot_token = os.getenv('BOT_TOKEN')
        bot = Bot(token=bot_token)
        dp = Dispatcher(bot)

        dp.register_message_handler(handle_message, content_types=types.ContentType.TEXT)

        await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())