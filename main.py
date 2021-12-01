import json
import logging
import os

from telegram import Update, ParseMode, message
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters
from telegram.ext import CommandHandler
from translate import Translator


from_lang = 'en'
to_lang = 'fa'



def validate_language(lang):
	file = open('language_codes.json', 'r')
	data = json.load(file)
	for i in data['languages']:
		if lang == i:
			return True
	return False
	


def start(update: Update, context: CallbackContext):
	user = update.effective_user['username']
	text = f'Hello @{user}!\n\n'
	description = 'This bot helps you to translate different words and sentences into the languages you want.\n\n'
	help = '/help\tto know how to use bot\n/list\tto see supported languages list\n/creator\tto know about me'
	start_message = text + description + help
	context.bot.send_message(chat_id=update.effective_chat.id, text=start_message)



def change_from_lang(update: Update, context: CallbackContext):
	global from_lang
	lang = ' '.join(context.args)
	if validate_language(lang):
		from_lang = lang
		context.bot.send_message(chat_id=update.effective_chat.id, text="Language Changed Successfully!")
	else:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Language Change Failed!")



def change_to_lang(update: Update, context: CallbackContext):
	global to_lang
	lang = ' '.join(context.args)
	if validate_language(lang):
		to_lang = lang
		context.bot.send_message(chat_id=update.effective_chat.id, text="Language Changed Successfully!")
	else:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Language Change Failed!")
	


def list_langs(update: Update, context: CallbackContext):
	file = open('language_codes.json', 'r')
	data = json.load(file)
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
	message = 'To translate your text, just type it for the bot and get the translation in a short time.\n\nYou can use the /from and /to commands to change the input or output language.\nThe default is English to Persian. To change the input or output language, enter the appropriate command and type the ISO 639-1 code of your choice in front of it. This bot supports many languages, list of those languages and their ISO 639-1 code is available in /list.\n\nExamples of input and output language change:\n\n\t/from fa\n\t/to en'
	context.bot.send_message(chat_id=update.effective_chat.id, text=message)



def translate(update: Update, context: CallbackContext):
	text = update.message.text
	translated_text = Translator(to_lang=to_lang, from_lang=from_lang).translate(text)
	update.message.reply_text(reply_to_message_id=update.message.message_id, text=translated_text)



def contact(update: Update, context: CallbackContext):
	message = 'My Telegram Id: @amirsarebani81\nMy Gmail: amirsarebani1381@gmail.com'
	context.bot.send_message(chat_id=update.effective_chat.id, text=message)



def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")



if __name__ == "__main__":

	TOKEN = ""
	NAME = ""

	PORT = os.environ.get('PORT')

	updater = Updater(token=TOKEN, use_context=True)
	dispatcher = updater.dispatcher

	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

	start_handler = CommandHandler('start', start)
	change_from_lang_handler = CommandHandler('from', change_from_lang)
	change_to_lang_handler = CommandHandler('to', change_to_lang)
	list_handler = CommandHandler('list', list_langs)
	creator_handler = CommandHandler('creator', creator)
	help_handler = CommandHandler('help', help)
	contact_handler = CommandHandler('contact', contact)
	translate_handler = MessageHandler(Filters.text & (~Filters.command), translate)
	unknown_handler = MessageHandler(Filters.command, unknown)

	dispatcher.add_handler(start_handler)
	dispatcher.add_handler(change_from_lang_handler)
	dispatcher.add_handler(change_to_lang_handler)
	dispatcher.add_handler(list_handler)
	dispatcher.add_handler(creator_handler)
	dispatcher.add_handler(help_handler)
	dispatcher.add_handler(contact_handler)
	dispatcher.add_handler(translate_handler)
	dispatcher.add_handler(unknown_handler)

	updater.start_webhook(listen="0.0.0.0",
							port=int(PORT),
							url_path=TOKEN,
							webhook_url=f"https://{NAME}.herokuapp.com/{TOKEN}")
	updater.idle()