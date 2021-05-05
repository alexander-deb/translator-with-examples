import requests

from bs4 import BeautifulSoup


def translate_message(bot, message, file):
    '''
    Function that parses web-page for giving translations and examples.
    '''
    first_language = file[str(message.from_user.id)][0]
    second_language = file[str(message.from_user.id)][1]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    URL = f'https://context.reverso.net/translation/{first_language}-{second_language}/{message.text}'

    try:
        response = requests.get(URL, headers=headers)  # send request
        if response.status_code == 200:
            #  print(response.status_code, 'OK')
            pass
    except requests.exceptions.ConnectionError:
        bot.send_message(
            chat_id=message.from_user.id,
            text='Something is wrong with the server. Contact support.'
        )

    soup = BeautifulSoup(response.text, "html.parser")  # parse web page
    word_list = soup.find(id="translations-content").get_text().split("\n")
    word_list = [item.strip() for item in word_list if item != ""]
    example_list = soup.find(id="examples-content").get_text().split("\n")
    # ATTENTION! MAGICAL CONSTANT! Removes trash from the end of list
    example_list = [item.strip() for item in example_list if item != ""][:-7]

    translation_text = f'*\n{second_language} translations:*\n'.title()
    for translation in word_list:
        if len(translation) > 0:
            translation_text += f'`{translation}\n`'

    i = 0
    example_text = '*Examples:*\n\n'
    exlen = len(example_list)
    while i < exlen:
        if i % 2:
            example = '`{}`\n'.format(example_list[i])
        else:
            example = '*{}:*'.format(example_list[i])

        if len(example_text) < 4096 < len(example_text + example + '\n'):
            bot.send_message(
                chat_id=message.from_user.id,
                text=example_text,
                parse_mode="markdown"
            )
            example_text = ''
        example_text += example + '\n'

        i += 1
    bot.send_message(
        chat_id=message.from_user.id,
        text=example_text,
        parse_mode="markdown"
    )
    return translation_text
