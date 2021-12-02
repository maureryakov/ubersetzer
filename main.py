import json
import logging
import os

from telegram import Update, ParseMode
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters
from telegram.ext import CommandHandler
from translate import Translator


file = open('language_codes.json', 'r')
data = json.load(file)


def check_bot_data_for_user(update: Update, context: CallbackContext):
	if not update.effective_user['id'] in context.bot_data.keys():
		context.bot_data[update.effective_user['id']] = ['en', 'fa']



def validate_language(lang):
	for i in data['languages']:
		if lang == i:
			return True
	return False



def start(update: Update, context: CallbackContext):
	check_bot_data_for_user(update, context)
	username = update.effective_user['username']
	text = f'Hello @{username}!\n\n'
	description = 'This bot helps you to translate different words and sentences into the languages you want.\n\n'
	help = '/help\tto know how to use bot\n/list\tto see supported languages list\n/creator\tto know about me'
	start_message = text + description + help
	context.bot.send_message(chat_id=update.effective_chat.id, text=start_message)



def change_from_lang(update: Update, context: CallbackContext):
	check_bot_data_for_user(update, context)
	lang = ' '.join(context.args)
	user = update.effective_user['id']
	if validate_language(lang):
		context.bot_data[user][0] = lang
		context.bot.send_message(chat_id=update.effective_chat.id, text="Input Language Changed Successfully!")
	else:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Input Language Change Failed!")



def change_to_lang(update: Update, context: CallbackContext):
	check_bot_data_for_user(update, context)
	lang = ' '.join(context.args)
	user = update.effective_user['id']
	if validate_language(lang):
		context.bot_data[user][1] = lang
		context.bot.send_message(chat_id=update.effective_chat.id, text="Output Language Changed Successfully!")
	else:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Output Language Change Failed!")
	


def current(update: Update, context: CallbackContext):
	check_bot_data_for_user(update, context)
	user = update.effective_user['id']
	message = f'Input Language: <b>{context.bot_data[user][0]}</b>\nOutput Language: <b>{context.bot_data[user][1]}</b>'
	context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)



def swap(update: Update, context: CallbackContext):
	check_bot_data_for_user(update, context)
	user = update.effective_user['id']
	from_lang = context.bot_data[user][0]
	to_lang = context.bot_data[user][1]
	context.bot_data[user][0] = to_lang
	context.bot_data[user][1] = from_lang
	context.bot.send_message(chat_id=update.effective_chat.id, text="Languages Swapped Successfully!")



def list_langs(update: Update, context: CallbackContext):
	replied_text = '<b>List of languages and their ISO 639-1 codes:</b>\n\n'

	counter = 1
	for i in data['languages']:
		lang = data['languages'][i]
		replied_text += f'{i:10}:\t<i>{lang}</i>\n'
		counter += 1

		if counter % 73 == 0:
			context.bot.send_message(chat_id=update.effective_chat.id, text=replied_text, parse_mode=ParseMode.HTML)
			replied_text = str()

	context.bot.send_message(chat_id=update.effective_chat.id, text=replied_text, parse_mode=ParseMode.HTML)



def creator(update: Update, context: CallbackContext):
	message = 'Hi. I am Amir hossein Sarebani, the creator of this bot.\n\nI am very happy that you are using this bot and I hope the bot will help you in the best way.\nIf you see a problem or have an idea on how to improve the bot, you can contact me using the following communication channels:\n\nTelegram Id: @amirsarebani81\nGmail: amirsarebani1381@gmail.com\n\n\nIf this bot is useful for you, please introduce it to your other friends.'
	context.bot.send_message(chat_id=update.effective_chat.id, text=message)



def help(update: Update, context: CallbackContext):
	message = 'To translate your text, just type it for the bot and get the translation in a short time.\n\nTo see current input and output languages use /current command.\nYou can use the /from and /to commands to change the input or output language.You can also use /swap command to easily swap input output languages.\nThe default is English to Persian. To change the input or output language, enter the appropriate command and type the ISO 639-1 code of your choice in front of it. This bot supports many languages, list of those languages and their ISO 639-1 code is available in /list.\n\nExamples of input and output language change:\n\nChange input language: \t/from fa\nChange output language: \t/to en'
	context.bot.send_message(chat_id=update.effective_chat.id, text=message)



def translate(update: Update, context: CallbackContext):
	check_bot_data_for_user(update, context)
	text = update.message.text
	user = update.effective_user['id']
	from_lang = context.bot_data[user][0]
	to_lang = context.bot_data[user][1]
	translated_text = Translator(provider='mymemory', to_lang=to_lang, from_lang=from_lang, email='amirsarebani1381@gmail.com').translate(text)
	update.message.reply_text(reply_to_message_id=update.message.message_id, text=translated_text)



def contact(update: Update, context: CallbackContext):
	message = 'My Telegram Id: @amirsarebani81\nMy Gmail: amirsarebani1381@gmail.com'
	context.bot.send_message(chat_id=update.effective_chat.id, text=message)



def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")



if __name__ == "__main__":

	# Set these variable to the appropriate values
	TOKEN = ""
	# Name just should set if you want to deploy your bot on Heroku (it's your app name)
	NAME = ""

	# Port is given by Heroku
	PORT = os.environ.get('PORT')

	updater = Updater(token=TOKEN, use_context=True)
	dispatcher = updater.dispatcher

	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

	start_handler = CommandHandler('start', start)
	change_from_lang_handler = CommandHandler('from', change_from_lang)
	change_to_lang_handler = CommandHandler('to', change_to_lang)
	current_handler = CommandHandler('current', current)
	swap_handler = CommandHandler('swap', swap)
	list_handler = CommandHandler('list', list_langs)
	creator_handler = CommandHandler('creator', creator)
	help_handler = CommandHandler('help', help)
	contact_handler = CommandHandler('contact', contact)
	translate_handler = MessageHandler(Filters.text & (~Filters.command), translate)
	unknown_handler = MessageHandler(Filters.command, unknown)

	dispatcher.add_handler(start_handler)
	dispatcher.add_handler(change_from_lang_handler)
	dispatcher.add_handler(change_to_lang_handler)
	dispatcher.add_handler(current_handler)
	dispatcher.add_handler(swap_handler)
	dispatcher.add_handler(list_handler)
	dispatcher.add_handler(creator_handler)
	dispatcher.add_handler(help_handler)
	dispatcher.add_handler(contact_handler)
	dispatcher.add_handler(translate_handler)
	dispatcher.add_handler(unknown_handler)

	# Comment this if you want to run your bot from your system
	# updater.start_webhook(listen="0.0.0.0",
	# 						port=int(PORT),
	# 						url_path=TOKEN,
	# 						webhook_url=f"https://{NAME}.herokuapp.com/{TOKEN}")

	# comment this if you want to deploy your bot on Heroku
	updater.start_polling()
	updater.idle()