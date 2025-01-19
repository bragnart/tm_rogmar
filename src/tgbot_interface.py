from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import os
import asyncio

TGBOT_TOKEN = os.environ.get("TGBOT_TOKEN")

class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.state = 'новый игрок'
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

users = {}  # Словарь для хранения объектов пользователей

async def send_message(update: Update, message: str, reply_markup=None):
    chat_id = update.message.chat_id
    if chat_id not in users:
        users[chat_id] = User(chat_id)
    users[chat_id].add_message(message)
    await update.message.reply_text(message, reply_markup=reply_markup)

async def start(update: Update, context):
    chat_id = update.message.chat_id
    await send_message(update, f"Your chat ID is {chat_id}")

async def handle_message(update: Update, context):
    chat_id = update.message.chat_id
    user_input = update.message.text
    response, reply_markup = handle_user_action(chat_id, user_input)
    await send_message(update, response, reply_markup)

async def button_click(update: Update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    action = query.data
    response, reply_markup = handle_user_action(chat_id, action)
    await query.answer()
    await send_message(update, response, reply_markup)

def handle_user_action(chat_id, user_input):
    if chat_id not in users:
        users[chat_id] = User(chat_id)

    user = users[chat_id]
    reply_markup = None

    if user_input == "/start":
        return "Добро пожаловать! Выберите действие:", main_menu_keyboard()
    elif user_input == "начать игру":
        user.state = 'игра началась'
        return "Игра началась!", main_menu_keyboard()
    elif user_input == "завершить игру":
        user.state = 'игра завершена'
        return "Игра завершена!", main_menu_keyboard()
    elif user_input == "/help":
        return "Команды: /start, /help", None
    else:
        return f"Вы сказали: {user_input}", None

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Начать игру", callback_data='начать игру')],
        [InlineKeyboardButton("Завершить игру", callback_data='завершить игру')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def update_game_state():
    while True:
        for chat_id in users:
            user = users[chat_id]
            current_state = user.state
            # Логика для обновления состояния игры
            # Например, отправка уведомлений игрокам
        await asyncio.sleep(5)

def main():
    application = Application.builder().token(TGBOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_click))
    
    asyncio.create_task(update_game_state())
    application.run_polling()

if __name__ == "__main__":
    main()
