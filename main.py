import telebot
from config import TOKEN, keys
from extensions import APIException, CryptoConverter


bot = telebot.TeleBot(Token)

@bot.message_handler(commands=["start", "help", "command1"])
def help(message: telebot.types.Message):
         text = "Чтобы начать работу введите комманду боту в следующем формате:\n<имя валюты>\
    <в какую валюту перевести>\
    <количество переводимой валюты>\nУвидеть список всех доступных валют: /values"
         bot.reply_to(message, text)

@bot.message_handler(commands=["values", "command2"])
def values(message: telebot.types.Message):
         text = "Доступные валюты:"
         for key in keys.keys():
             text = "\n".join((text, key, ))
         bot.reply_to(message, text)


@bot.message_handler(commands=['start'])
def function_name(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Добрый день,\t {message.chat.first_name}!')
    bot.send_message(message.chat.id, 'Воспользуйтесь подсказками бота /help')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', 1])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')
        if len(values) > 3:
            raise APIException('Некорректное количество введенных значений.\n')
        amount, quote, base = values
        total_base = CryptoConverter.convert(amount, quote, base)

    except APIException as e:
        bot.reply_to(message, f'Ошибка\n{e} /help')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e} \n /help')
    else:
        text = f'{amount} ед. <{quote}> это {round(total_base, 2)} ед. <{base}>'
        bot.send_message(message.chat.id, text)

bot.polling()
