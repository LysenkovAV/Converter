import telebot # для работы с Телеграм-ботом

from config import * # настройки
from extensions import Converter, APIException # класс конвертации и класс ошибок

bot = telebot.TeleBot(TOKEN) # создание бота


# обработка команд start и help - вывод инструкции по работе с ботом
@bot.message_handler(commands=['start', 'help'])
def handle_help(message: telebot.types.Message):
    text = 'Формат ввода для конвертации валют:\n \
<из валюты 1> <в валюту 2> <количество валюты 1>\n\n \
Команды боту:\n \
/start, /help - инструкция по работе\n \
/values - список доступных валют'
    bot.reply_to(message, text) # ответ бота


# обработка команды values - вывод списка доступных валют
@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in keys.keys():
        text += '\n' + i + ' ' + '(' + keys[i] + ')'
    bot.reply_to(message, text) # ответ бота


# обработка запроса на конвертацию валют
@bot.message_handler(content_types=['text'])
def handle_convert(message: telebot.types.Message):
    try:
        base, quote, amount = message.text.split() # base - валюта 1, quote - валюта 2, amount - количетво валюты 1
        price_message = Converter.get_price(base, quote, amount) # высоз статического метода в классе конвертации
    except ValueError as v: # если количество параметров в запросе неверное
        bot.reply_to(message, "Неверное количество параметров!")
    except APIException as a: # если есть ошибки в параметрах запроса
        bot.reply_to(message, f"Ошибка в запросе:\n{a}")
    else:
        bot.reply_to(message, price_message) # если конвертация произошла без ошибок - ответ бота


bot.polling(none_stop=True) # бот работает пока не остановлена программа