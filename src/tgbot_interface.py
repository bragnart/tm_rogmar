from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import os
import asyncio
from game_process import handle_user_action, update_game_state

TGBOT_TOKEN = os.environ.get("TGBOT_TOKEN")

users = {}  # Словарь для хранения объектов пользователей

class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.state = 'новый игрок'
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

async def send_message(update: Update, message: str, reply_markup=None):
    if update.message:
        chat_id = update.message.chat_id
    else:
        chat_id = update.callback_query.message.chat_id

    if chat_id not in users:
        users[chat_id] = User(chat_id)
    users[chat_id].add_message(message)
    await update.effective_message.reply_text(message, reply_markup=reply_markup)

async def start(update: Update, context):
    chat_id = update.message.chat_id
    await send_message(update, f"Your chat ID is {chat_id}")

async def help_command(update: Update, context):
    await send_message(update, "Команды: /start, /help")

async def handle_message(update: Update, context):
    chat_id = update.message.chat_id
    user_input = update.message.text
    response, reply_markup = handle_user_action(chat_id, user_input, users)
    await send_message(update, response, reply_markup)

async def button_click(update: Update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    action = query.data
    response, reply_markup = handle_user_action(chat_id, action, users)
    await query.answer()
    await send_message(update, response, reply_markup)

def main():
    application = Application.builder().token(TGBOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_click))

    loop = asyncio.get_event_loop()
    loop.create_task(update_game_state(users))
    application.run_polling()
    loop.run_forever()

if __name__ == "__main__":
    main()
