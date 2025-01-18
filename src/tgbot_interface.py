from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import os

TGBOT_TOKEN = os.environ.get("TGBOT_TOKEN")

async def start(update: Update, context):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Your chat ID is {chat_id}")

def main():
    application = Application.builder().token(TGBOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    
    application.run_polling()

if __name__ == "__main__":
    main()



