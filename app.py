import telebot
from extentions import APIException, CryptoConverter
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def help(message: telebot.types.Message):
    text = 'Firstly enter command in next format(with whitespaces): ' \
           ' \n- <Currency name, you want convert to >  \n- <Currency name you want to convert from' \
           '> \n- <Amount to exchange>\n For example: euro dollar 220\n \
 Available currencies list: /values'

    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Available currencies:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

# base, quote, amount = message.text.split(' ')
@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('You entered more (or less) than 3 parameters')
        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Wrong user\'s input. \n{e}')

    except Exception as e:
        bot.reply_to(message, f'can not process this command\n{e}')
    else:
        text = f'Price {amount} {quote} in {base}: {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
