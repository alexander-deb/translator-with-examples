import os
import shelve
import telebot

from assets.globals import Globals
from translate import translate_message


TG_TOKEN = os.getenv('TG_TOKEN')
bot = telebot.TeleBot(TG_TOKEN)

'''
list of commands:
help - help :)))
from_language - allows you to choose the language, you want to translate from
into_language - allows you to choose the language, you want to translate into
exchange - exchanges language from and language into
'''


@bot.message_handler(commands=['start', 'help'])
def start(message):
    '''
    Function that starts bot and adds user to database
    '''
    bot.send_message(chat_id=message.chat.id,
                     text='Choose languages. Press /from_language and then /into_language.')
    with shelve.open('assets/user_langs') as file:
        file[str(message.from_user.id)] = ['not chosen', 'not chosen']


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    '''
    Shows beautiful buttons
    '''
    with shelve.open('assets/user_langs') as file:
        if Globals.flag:
            bot.answer_callback_query(
                callback_query_id=call.id, text=f'You succesfully changed second language to {call.data}')
            second_language = call.data[Globals.TRASH:].lower()

            file[str(call.from_user.id)] = [
                file[str(call.from_user.id)][Globals.FIRST_LANG], second_language]
        else:
            bot.answer_callback_query(
                callback_query_id=call.id, text=f'You succesfully changed first language to {call.data}')
            first_language = call.data[Globals.TRASH:].lower()
            file[str(call.from_user.id)] = [
                first_language, file[str(call.from_user.id)][Globals.SECOND_LANG]]

    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)


@bot.message_handler(commands=['from_language'])
def change_first_lang(message):
    '''
    Changes first language in database
    '''
    markup = telebot.types.InlineKeyboardMarkup()

    with shelve.open('assets/user_langs') as file:
        for text in Globals.list_of_languages:
            if text[Globals.TRASH:] not in file[str(message.from_user.id)]:
                button = telebot.types.InlineKeyboardButton(
                    text=text, callback_data=text)
                markup.add(button)
    bot.send_message(chat_id=message.chat.id,
                     text='Choose language from this list:', reply_markup=markup)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    Globals.flag = False


@bot.message_handler(commands=['into_language'])
def change_second_lang(message):
    '''
    Changes second language in database
    '''
    markup = telebot.types.InlineKeyboardMarkup()
    with shelve.open('assets/user_langs') as file:
        for text in Globals.list_of_languages:
            if text[Globals.TRASH:] not in file[str(message.from_user.id)]:
                button = telebot.types.InlineKeyboardButton(
                    text=text, callback_data=text)
                markup.add(button)
    bot.send_message(chat_id=message.chat.id,
                     text='Choose language from this list:', reply_markup=markup)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    Globals.flag = True


@bot.message_handler(commands=['exchange'])
def exchange(message):
    '''
    Exchanges first and second langugages.
    '''
    with shelve.open('assets/user_langs') as file:
        file[str(message.from_user.id)] = [
            file[str(message.from_user.id)][Globals.SECOND_LANG], file[str(message.from_user.id)][Globals.FIRST_LANG]]
    bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id
    )
    bot.send_message(
        chat_id=message.from_user.id,
        text='Languages succesfully exchanged!'
    )
    with shelve.open('assets/user_langs') as file:
        bot.send_message(
            chat_id=message.from_user.id,
            text='Selected languages:\nFrom {}\nInto {}'.format(
                file[str(message.from_user.id)][Globals.FIRST_LANG], file[str(
                    message.from_user.id)][Globals.SECOND_LANG]
            )
        )


@bot.message_handler(content_types=["text"])
def send_message(message):
    '''
    Sends translations and examples to the user
    '''
    with shelve.open('assets/user_langs') as file:
        if 'not chosen' not in file[str(message.from_user.id)]:
            translation_text, example_text = translate_message(str(message.from_user.id), file, message.text)
            bot.send_message(
                chat_id=message.from_user.id,
                text=example_text,
                parse_mode="markdown"
            )
            bot.send_message(
                chat_id=message.from_user.id,
                text=translation_text,
                parse_mode="markdown"
            )
        else:
            if file[str(message.from_user.id)][Globals.FIRST_LANG] == 'not chosen':
                text = 'Please, choose language you want to translate FROM. Press /from_language'
                bot.send_message(
                    chat_id=message.from_user.id,
                    text=text
                )
            if file[str(message.from_user.id)][Globals.SECOND_LANG] == 'not chosen':
                text = 'Please, choose language you want to translate INTO. Press /into_language'
                bot.send_message(
                    chat_id=message.from_user.id,
                    text=text
                )


if __name__ == '__main__':
    bot.polling(none_stop=True)
