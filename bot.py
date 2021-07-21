#Бот версия 1.4
import telebot
from telebot import types # необходимо для клавиатуры
import random
import requests
from bs4 import BeautifulSoup as BS
import config

bot = telebot.TeleBot(config.TOKEN)

# Списки с вопросами(q) пользователя и ответами(a) бота
greetings_q = ['привет', 'здорова', 'хай']
greetings_a = ['Привет', 'Здорова', 'Бомжур']
howdies_q = ['как дела?', 'как поживаешь?', 'как ты?']
howdies_a = ['Шикарно', 'Великолепно', 'Замечательно', 'Хорошо']

HELP_MESSAGE = """
Я могу ответить на ваше приветствие. Или можете спросить как у меня дела.
\nТакже я умею рассказывать анекдоты и смогу посчитать факториал от введенного числа.
"""

UNKNOWN_MESSAGE = """
Пока что я не знаю, что вам ответить на это.
\nВведите "/help" чтобы узнать чему я научился на данный момент
"""

@bot.message_handler(commands=['start', 'help', 'anek', 'anek2'])
def start_commands(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')
    if message.text == '/help':
        bot.send_message(message.chat.id, HELP_MESSAGE)
    if message.text == '/anek':
        bot.send_message(message.chat.id, anek())
    if message.text == '/anek2':
        bot.send_message(message.chat.id, anek2())

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text.lower() in greetings_q:
        bot.send_message(message.chat.id, random.choice(greetings_a)) 
    elif message.text.lower() in howdies_q:
        bot.send_message(message.chat.id, random.choice(howdies_a))
    elif message.text.lower() == 'покажи попуга':
        stic = open('sticker.webp', 'rb')
        bot.send_sticker(message.chat.id,stic)
    elif message.text.isdigit():
        bot.send_message(message.chat.id, factorial(message.text))
    else:
        bot.send_message(message.chat.id, UNKNOWN_MESSAGE)

def factorial(n):
    num = int(n)
    fact = 1
    for i in range(1, num + 1):
        fact = fact * i
    return f'{fact} — факториал числа {num}'

def anek():
    try:
        url = 'https://baneks.ru/random'
        r = requests.get(url)
        r.encoding = 'utf-8'
        soup = BS(r.text, "html.parser")
        anek = soup.find('article').text
        return anek
    except:
        return """
        Анекдота не будет. Сайт не работает. 
        \nВведите /anek2 чтобы получить анекдот с другого сайта."""

def anek2():
    url = 'https://nekdo.ru/random'
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BS(r.text, "html.parser")
    anek = soup.find('div', class_='text').text
    return anek

bot.polling(none_stop=True)
