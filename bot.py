import os
import json
from dotenv import load_dotenv

# Telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, BotCommandScopeChat, BotCommandScopeChatMember
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

LOCALES = {}
LOCALES_DIR = "langs"
LANGUAGES = {
    "en": "English",
    "ru": "Русский",
    "uk": "Українська"
}
user_languages = {}

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
    user = getattr(update, "effective_user", None)
    uid = user.id if user else None
    lang = user_languages.get(uid) if uid else None
    if lang not in LOCALES:
        lang = "en"
    return lang

async def set_user_commands(bot, chat_id, user_id, lang_code, for_whole_chat=False):
    lang_dict = LOCALES.get(lang_code, LOCALES["en"])
    commands = [
        BotCommand("start", lang_dict["start_command"]),
        BotCommand("language", lang_dict["language_command"]),
        BotCommand("everyone", lang_dict["everyone_command"])
    ]

    if for_whole_chat:
        scope = BotCommandScopeChat(chat_id=chat_id)
    else:
        scope = BotCommandScopeChatMember(chat_id=chat_id, user_id=user_id)

    try:
        await bot.set_my_commands(commands, scope=scope)
        print(f"[i] set commands for user {user_id} (chat {chat_id}) lang={lang_code}")
    except Exception as e:
        print(f"[!] failed set_my_commands for user {user_id}: {e}")

# Beginning (/start)
async def tg_start(update, context):
    lang = get_user_lang(update)
    await update.message.reply_text(LOCALES[lang]["start"])

    try:
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        await set_user_commands(context.bot, chat_id=chat_id, user_id=user_id, lang_code=lang, for_whole_chat=False)
    except Exception as e:
        print("set_user_commands (on start) error:", e)


# Teg everyone (/everyone)
async def everyone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(update)
    chat = update.effective_chat

    try:
        admins = await context.bot.get_chat_administrators(chat.id)

        members = []
        for admin in admins:
            user = admin.user
            if user.is_bot or user.id == context.bot.id:
                continue
            if user.username:
                members.append(f"@{user.username}")
            else:
                members.append(user.first_name or str(user.id))

        if members:
            text = " ".join(members)
            await update.message.reply_text(text)
        else:
            await update.message.reply_text(LOCALES[lang]["no_members"])
    except Exception as e:
        text = LOCALES[lang].get("error", "Error: {error}").format(error=e)
        await update.message.reply_text(text)

# ===== Change language ===== (/language)
async def choose_language(update, context):
    lang = get_user_lang(update)

    keyboard = [
        [InlineKeyboardButton(name, callback_data=code)] 
        for code, name in LANGUAGES.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(LOCALES[lang]["choose_language"], reply_markup=reply_markup)

async def language_button(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    selected_lang = query.data
    user_id = query.from_user.id
    chat_id = query.message.chat.id

    user_languages[user_id] = selected_lang

    message = LOCALES[selected_lang]["language_set"].format(lang_name=LANGUAGES[selected_lang])
    await query.edit_message_text(text=message)

    try:
        await set_user_commands(context.bot, chat_id=chat_id, user_id=user_id, lang_code=selected_lang, for_whole_chat=False)
    except Exception as e:
        print("set_user_commands error:", e)
# =========================

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", tg_start))
    app.add_handler(CommandHandler("everyone", everyone))
    app.add_handler(CommandHandler("language", choose_language))
    app.add_handler(CallbackQueryHandler(language_button))

    app.run_polling()
    
