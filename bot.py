import asyncio
from telegram.ext import Application, CommandHandler
import discord

# Tokens
TELEGRAM_TOKEN = ""
DISCORD_TOKEN = ""

# TELEGRAM
async def tg_start(update, context):
    await update.message.reply_text("Hello from Telegram!")

def run_telegram():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", tg_start))
    return app

# DISCORD
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

discord_client = discord.Client(intents=intents)

@discord_client.event
async def on_ready():
    print(f"Discord has entered {discord_client.user}")

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return
    if message.content == "!ping":
        await message.channel.send("Hello from Discord!")

# Start for all platforms
async def start():
    tg_app = run_telegram()

    await asyncio.gather(
        tg_app.run_polling(),
        discord_client.start(DISCORD_TOKEN)
    )

