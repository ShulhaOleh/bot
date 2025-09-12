import os
import json
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from telegram import Update

LOCALES = {}
LOCALES_DIR = "langs"

# Tokens
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Alert if incorrect tokens
if not TELEGRAM_TOKEN:
    raise SystemExit("Error: TELEGRAM_TOKEN was not found. Add TELEGRAM_TOKEN in .env file.")

for filename in os.listdir(LOCALES_DIR):
    if filename.endswith(".json"):
        lang_code = filename.split(".")[0]

        with open(os.path.join(LOCALES_DIR, filename), encoding="utf-8") as f:
            LOCALES[lang_code] = json.load(f)

def get_user_lang(update):
    lang = update.effective_user.language_code
    if lang not in LOCALES:
        lang = "en"
    return lang

# Beginning (/start)
async def tg_start(update, context):
    lang = get_user_lang(update)
    await update.message.reply_text(LOCALES[lang]["start"])


# Teg everyone (/everyone)
async def everyone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(update)

    chat = update.effective_chat
    try:
        admins = await context.bot.get_chat_administrators(chat.id)
        members = [f"@{admin.user.username}" for admin in admins if admin.user.username]
        if members:
            text = " ".join(members)
            await update.message.reply_text(text)
        else:
            await update.message.reply_text(LOCALES[lang]["no_members"])
    except Exception as e:
        await update.message.reply_text(LOCALES[lang]["error"])

def start():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", tg_start))
    app.add_handler(CommandHandler("everyone", everyone))

    app.run_polling()
    
