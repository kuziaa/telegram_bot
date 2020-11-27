import telebot
import config
from ling import LinguaLeo
from state import State
import random


bot = telebot.TeleBot(config.token)
lingua = LinguaLeo()
state = State()

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


@bot.message_handler(commands=['auth'])
def start_message(message):
    state.state = 'auth'
    lingua.login = None
    lingua.password = None
    answer = 'Напиши свой Логин'
    send_text_message(message.chat.id, answer)


@bot.message_handler(commands=['stop'])
def stop_message(message):
    state.state = None
    answer = 'Все режимы остановлены'
    chat_id = message.chat.id
    send_text_message(chat_id, answer)


@bot.message_handler(commands=['to_en'])
def start_message(message):
    state.state = 'to_en'
    to_en(message)



@bot.message_handler(content_types=['text'])
def check_text(message):
    if state.state == 'auth':
        auth(message)
    elif state.state == 'to_en':
        to_en(message)


def auth(message):
    chat_id = message.chat.id
    if not lingua.login:
        lingua.login = message.text
        answer = 'It was login. Please send also password.'
        send_text_message(chat_id, answer)
        return
    elif not lingua.password:
        lingua.password = message.text
        answer = 'It was password. Now we are checking it ...'
        send_text_message(chat_id, answer)

    if lingua.logining():
        answer = 'Login and password are ok'
        state.state = None
    else:
        answer = 'Login and password are incorrect. Try again.'
    send_text_message(chat_id, answer)
    lingua.get_full_vocabulary()

def to_en(message):
    chat_id = message.chat.id
    if state.step == 0:
        send_random_word_in_en(message)
    else:
        if message.text == state.word['nwd']:
            send_text_message(chat_id, 'Правильно')
        else:
            send_text_message(chat_id, 'Неправильно')
            send_text_message(chat_id, f'Правильный ответ: {state.word["nwd"]}')
        state.word = ''
        state.step = 0
        send_random_word_in_en(message)


def send_random_word_in_en(message):
    chat_id = message.chat.id
    state.word = random.choice(lingua.full_vocabulary)
    send_text_message(chat_id, state.word['trc'])
    state.step += 1




def send_text_message(chat_id, text):
    bot.send_message(chat_id, text)



keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row("Привет", "Пока", "ааа", "ббб", "ввв", "ггг")


bot.polling()
