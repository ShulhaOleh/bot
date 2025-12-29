[![ENG](https://img.shields.io/badge/lang-English-red)](readme.md)
[![UKR](https://img.shields.io/badge/lang-Ukrainian-green)](docs/readme.uk.md)
[![RUS](https://img.shields.io/badge/lang-Russian-blue)](docs/readme.ru.md)

# Chattiye Bot

A multilingual Telegram bot for managing groups with support for mentioning all participants and dynamic language switching.

## Features

* **Group Management**: Mention all group administrators with a single command
* **Multilingual Support**: Built-in support for English, Russian, and Ukrainian

## Commands

* `/start` - Initialize the bot and display a welcome message
* `/everyone` - Mention all group administrators (mentions @username or names)
* `/language` - Open the language selection menu

## Requirements

* Python 3.14
* Telegram bot token (obtain from [@BotFather](https://t.me/BotFather))

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/ShulhaOleh/bot.git
   cd bot
   ```

2. **Install dependencies**

   ```bash
   pip install python-telegram-bot python-dotenv
   ```

3. **Set up environment variables**

   Create a `.env` file in the project root:

   ```env
   TELEGRAM_TOKEN=your_bot_token_here
   ```

## Project Structure

```
bot/
├── bot.py              # Main bot logic and handlers
├── main.py             # Entry point
├── .env                # Environment variables (create this file)
├── langs/              # Localization files
│   ├── en.json
│   ├── ru.json
│   └── uk.json
├── LICENSE
└── README.md
```

## Usage

Run the bot:

```bash
python main.py
```

The bot will start polling updates. Add it to a Telegram group and use the commands above.

## How it works

### Language Selection

* Users can change the interface language anytime using `/language`
* Language preferences are stored in memory for each user
* Bot commands automatically update according to the selected language

### Everyone Command

* Mentions only group administrators (not all participants) due to Telegram limitations
* Skips bots in the mention list
* Works only in group chats with the necessary bot permissions

## Dependencies

* `python-telegram-bot` - A wrapper for the Telegram Bot API
* `python-dotenv` - Environment variable management

## Bot Permissions

* The bot requires admin rights to access the list of chat administrators

## Known Limitations

* User language preferences are stored in memory and reset on bot restart
* The `/everyone` command works only for group administrators, not all participants
* The bot needs proper permissions to access the list of chat administrators

## License

This project is licensed under the MIT [License](LICENSE) — see the LICENSE file for details.
