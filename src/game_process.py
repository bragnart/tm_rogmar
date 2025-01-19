import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.state = 'новый игрок'
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

def handle_user_action(chat_id, user_input, users):
    if chat_id not in users:
        users[chat_id] = User(chat_id)

    user = users[chat_id]
    reply_markup = None

    if user_input.lower() == "начать игру":
        user.state = 'игра началась'
        return "Игра началась!", main_menu_keyboard()
    elif user_input.lower() == "завершить игру":
        user.state = 'игра завершена'
        return "Игра завершена!", main_menu_keyboard()
    else:
        return f"Вы сказали: {user_input}", None

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Начать игру", callback_data='начать игру')],
        [InlineKeyboardButton("Завершить игру", callback_data='завершить игру')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def update_game_state(users):
    while True:
        for chat_id in users:
            user = users[chat_id]
            current_state = user.state
            # Логика для обновления состояния игры
            # Например, отправка уведомлений игрокам
        await asyncio.sleep(5)
