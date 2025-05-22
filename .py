import os
import random
import telebot
from telebot import types

API_TOKEN = '123'  #Замените на токен вашего бота
bot = telebot.TeleBot(API_TOKEN)

MUSIC_DIR = os.path.join(os.path.expanduser('~'), 'Desktop', 'music')  #Путь до музыки (папка на рабочем столе с именим music)

played_tracks = []  # Список для хранения уже воспроизведенных треков

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_play = types.KeyboardButton('Слушать музыку')           #Создает кнопку "Слушать музыку" в ответ на команду /start
    keyboard.add(btn_play)
    bot.send_message(message.chat.id, 'Нажми на кнопку:', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Слушать музыку')
def play_random_music(message):
    music_files = os.listdir(MUSIC_DIR)     #обрабатывает нажатие кнопки "Слушать музыку" и получает список музыкальных файлов из указанной директории MUSIC_DIR

    if not music_files:
        bot.send_message(message.chat.id, 'Музыки ещё нет.')
        return               #Проверяет, есть ли музыкальные файлы в директории MUSIC_DIR. Если файлов нет, бот отправляет сообщение "Музыки ещё нет."

    # Убираем уже воспроизведенные треки из списка
    available_tracks = [track for track in music_files if track not in played_tracks]

    if not available_tracks:  #Если все треки были воспроизведены, сбрасываем
        played_tracks.clear()
        available_tracks = music_files

    random_music = random.choice(available_tracks)
    played_tracks.append(random_music)       #Выбирает случайный трек из списка доступных треков available_tracks и добавляет его в список played_tracks, чтобы отслеживать уже воспроизведенные треки.

    # Проверка на последующее воспроизведение одного и того же трека
    if len(played_tracks) > 1 and played_tracks[-1] == played_tracks[-2]:
        played_tracks.pop()  # Удаляем последний добавленный трек, если он повторяется

    with open(os.path.join(MUSIC_DIR, random_music), 'rb') as music:
        bot.send_audio(message.chat.id, music)

bot.polling()     #Открывает выбранный случайный музыкальный файл в двоичном режиме ('rb') и отправляет его в чат пользователя с помощью метода send_audio. Затем bot.polling() запускает бесконечный цикл, который позволяет боту принимать и обрабатывать входящие сообщения.

