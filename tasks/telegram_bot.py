from tools import ask_agent, get_weather
import logging
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from dotenv import load_dotenv
load_dotenv()

import os


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TG_TOKEN = os.environ['TELEGRAM_BOT_API_KEY']

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    history = context.user_data.get("history", [])
    history_str = '\n'.join(history)

    history.append(f"Пользователь: {user_msg}")

    if 'погода' in user_msg.lower():
        answer = get_weather()
    else:
        answer = await ask_agent(user_msg, history_str)

    history.append(f"Агент: {answer}")
    context.user_data["history"] = history

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=answer
    )


if __name__ == '__main__':
    application = ApplicationBuilder().token(TG_TOKEN).build()

    start_handler = CommandHandler('start', handle_message)
    message_handler = MessageHandler(filters.ALL, handle_message)

    application.add_handler(start_handler)
    application.add_handler(message_handler)

    application.run_polling()
