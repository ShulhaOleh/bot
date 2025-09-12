import os
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

# Tokens
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Alert if incorrect tokens
if not TELEGRAM_TOKEN:
    raise SystemExit("Error: TELEGRAM_TOKEN was not found. Add TELEGRAM_TOKEN in .env file.")

async def tg_start(update, context):
    await update.message.reply_text("Hello from Telegram!")

def start():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", tg_start))
    app.run_polling()
    
