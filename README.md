# Telegram Translator Bot

## Table of content

- [Introduction](README.md#introduction)
- [Bot commands](README.md#bot-commands)
- [Dependencies](README.md#dependencies)
- [Usage](README.md#usage)
- [Contributing](README.md#contributing)

## Introduction

This project is a simple Telegram translator bot that receives a text from the user and translates it into any language. The robot supports more than a hundred different languages ​​for input and output, some of which are:

- Chinese
- English
- French
- Persian
- German
- etc

## Bot Commands

| Command | Description |
| ------- | ----------- |
| /start | Start the bot |
| /help | Help |
| /list | List available languages and their ISO 639-1 code |
| /from | Change input language |
| /to | Change output language |
| /creator | Creator info |
| /contact | Communication channels |
| /current | See current input/output languages |
| /swap | Swap input output languages |

## Dependencies

- [python3](https://www.python.org/) >= 3.6.8
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) >= 13.4
- [translate](https://pypi.org/project/translate/) >= 3.6

## Usage

You can always see an active version of this robot [here](https://t.me/amir_translator_bot).
To your version of this robot follow the steps below:

1. get your personal API token from [@BotFather](https://t.me/botfather)
2. Clone the repository

   ```shell
   git clone https://github.com/amirsarebani81/telegram-translator-bot.git
   ```

3. Install the dependencies
4. Go to project directory and run main.py

    ```shell
    cd telegram-translator-bot
    python3 main.py
    ```

You can also deploy your bot on [Heroku](https://heroku.com). To do this

1. Comment and uncomment the necessary parts of the code
2. Install the Heroku CLI
3. If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.

    ```shell
    heroku login
    ```

4. Push your repository to Heroku

    ```shell
    git push heroku master
    ```

## Contributing

Contributions of all sizes are welcome. You can also help by reporting bugs or making suggestions.
