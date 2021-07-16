#Бот версия 1.4
import telebot
import random
import requests
from bs4 import BeautifulSoup as BS
import config

bot = telebot.TeleBot(config.TOKEN)

#Списки с вопросами(q) пользователя и ответами(a) бота
greetings_q = ['привет', 'здорова', 'хай']
greetings_a = ['Привет', 'Здорова', 'Бомжур']
howdies_q = ['как дела?', 'как поживаешь?', 'как ты?']
howdies_a = ['Шикарно', 'Великолепно', 'Замечательно', 'Хорошо']

HELP_MESSAGE = """
Я могу ответить на ваше приветствие. Или можете спросить как у меня дела.
\nТакже я умею рассказывать анекдоты и смогу посчитать факториал от введенного числа.
\nПопробуйте что-нибудь ввести прямо сейчас!
"""

@bot.message_handler(commands=['start', 'help', 'anek'])
def start_commands(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')
    if message.text == '/help':
        bot.send_message(message.chat.id, HELP_MESSAGE)
    if message.text == '/anek':
        bot.send_message(message.chat.id, anek())

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text.lower() in greetings_q:
        bot.send_message(message.chat.id, random.choice(greetings_a)) 
    elif message.text.lower() in howdies_q:
        bot.send_message(message.chat.id, random.choice(howdies_a)) 
    elif message.text.lower() == 'где ты находишься?':
        bot.send_message(message.chat.id, 'Я нахожусь в Амстердаме.') 
    elif message.text.isdigit():
        bot.send_message(message.chat.id, f'{factorial(message.text)} — факториал числа {message.text}')
    else:
        bot.send_message(message.chat.id, 'Пока что я не знаю, что вам ответить на это.\nВведите "/help" чтобы узнать чему я научился на данный момент.')

def factorial(n):
    n = int(n)
    fact = 1
    while n > 1:
        fact *= n
        n -= 1
    return fact

def anek():
    url = 'https://baneks.ru/random'
    r = requests.get(url) #отправляем ссылку в библиотеку requests
    r.encoding = 'utf-8' # принудительный выбор кодировки, без него не работало
    soup = BS(r.text, "html.parser") #отправляем в bs, второй параметр - выбранный парсер
    anek = soup.find('article').text #вывести текст полученного сектора в переменную
    return anek

bot.polling(none_stop=True)
