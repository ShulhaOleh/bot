import os
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from telegram import Update

# Tokens
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Alert if incorrect tokens
if not TELEGRAM_TOKEN:
    raise SystemExit("Error: TELEGRAM_TOKEN was not found. Add TELEGRAM_TOKEN in .env file.")

# Beginning (/start)
async def tg_start(update, context):
    await update.message.reply_text("Hello, I'm Chattiye!")

# Teg everyone (/everyone)
async def everyone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    try:
        admins = await context.bot.get_chat_administrators(chat.id)
        members = [f"@{admin.user.username}" for admin in admins if admin.user.username]
        if members:
            text = " ".join(members)
            await update.message.reply_text(text)
        else:
            await update.message.reply_text("Can't get members")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def start():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", tg_start))
    app.add_handler(CommandHandler("everyone", everyone))

    app.run_polling()
    
