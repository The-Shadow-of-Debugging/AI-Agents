# from tasks.task_1 import ask_agent, get_weather
import asyncio
from telegram import Bot, Update

from dotenv import load_dotenv
load_dotenv()

import os

TG_TOKEN = os.environ['TELEGRAM_BOT_API_KEY']

# def handle_message(update, context):
#     if 'погода' in context.lower():
#         answer = get_weather()
#     else:
#         answer = ask_agent(update.message.text)


async def main():
    bot = Bot(TG_TOKEN)
    async with bot:
        print(await bot.get_me())


if __name__ == '__main__':
    asyncio.run(main())