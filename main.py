import json
import time
from display import display_hangman
from config import bot
from words import word_list

dict_of_players = {}
'''
dict_of_players: {chat.id : [name, word itself, word's complection, length, tries (default 6), guessed_letters, guessed_words, guessed (default FALSE)]}

'''

with open('dict_of_players.txt', 'r') as dict_from_file:
    if isinstance(dict_from_file, type):
        json.dump(dict_of_players_old)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == 'Привет':
        bot.send_message(message.from_user.id, 'Ура, мы нашли общий язык!\
\nНу привет, сейчас мы попробуем поиграть в виселицу!')
        message = bot.send_message(message.chat.id, 'Представься, пожалуйста:)')
        bot.register_next_step_handler(message, name)
    elif message.text == '\help':
        bot.send_message(message.from_user.id, 'Ну давай же,\
напиши слово "Привет"')
    else:
        bot.send_message(message.from_user.id, 'Я ничего не понимаю:(\
\nЯ пока еще очень глупый бот, но dorochka учится. \
Поэтому давай начнем с малого - напиши просто "Привет" \n(Исходя из экспериментов это была самая сложная часть игры. Подсказка, Привет с большой буквы :))!')


def name(message):
    name = message.text
    if message.chat.id not in dict_of_players_old:
        dict_of_players[message.chat.id] = [name]
    bot.send_message(message.chat.id, f'Здарова, {dict_of_players[message.chat.id][0]}!')
    bot.send_message(message.chat.id, 'Так-так-так, пока ты восклицаешь, неужели dorochka сделала это сама, я в это время задумаю слово. Погоди немного. \
\n\n\n(И, да, она сделала это сама и примерно за один день)')
    time.sleep(1)
    bot.send_message(message.chat.id, f'{dict_of_players[message.chat.id][0]}, пока я загадываю слово, напомню тебе правила:\
  \nЯ загадываю слово на русском языке! \
  \nБуквы заменены на символы "_". Буквы "ё" нет. Цифр тоже нет.\
  \nКажется, что все супер легко, не так ли? У тебя будет возможность сделать 6 ошибок.')
    message = bot.send_message(message.chat.id, 'Начнем?')
    bot.register_next_step_handler(message, start)


def new_word():
    word = random.choice(word_list).upper()
    return word


def start(message):
    word = new_word()
    word_complection = '_' * len(word)
    length = len(word)
    del dict_of_players[message.chat.id][1:]
    dict_of_players[message.chat.id].append(word)
    dict_of_players[message.chat.id].append(word_complection)
    dict_of_players[message.chat.id].append(length)
    dict_of_players[message.chat.id].append(6)
    dict_of_players[message.chat.id].append([])
    dict_of_players[message.chat.id].append([])
    dict_of_players[message.chat.id].append(False)
    bot.send_message(message.chat.id, display_hangman(dict_of_players[message.chat.id][4]))
    time.sleep(0.5)
    bot.send_message(message.chat.id, f'Слово состоит из {dict_of_players[message.chat.id][3]} букв')
    time.sleep(0.5)
    bot.send_message(message.chat.id, f'Само слово {dict_of_players[message.chat.id][2]}\
\nПожалуйста, введи букву, которая, по твоему мнению, может быть в загаданном слове')
    time.sleep(0.5)
    bot.register_next_step_handler(message, game)


def game(message):
    print(dict_of_players)
    if message.text.upper() in 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' and message.text.upper() in \
            dict_of_players[message.chat.id][1] and len(message.text) == 1:
        message.text = message.text.upper()
        dict_of_players[message.chat.id][5].append(message.text)
        for i in range(dict_of_players[message.chat.id][3]):
            if dict_of_players[message.chat.id][1][i] == message.text:
                dict_of_players[message.chat.id][2] = dict_of_players[message.chat.id][2][:i] + message.text + \
                                                      dict_of_players[message.chat.id][2][i + 1:]
        bot.send_message(message.chat.id, dict_of_players[message.chat.id][2])
        bot.send_message(message.chat.id, f'Предположенные буквы: {dict_of_players[message.chat.id][5]}')
        message = bot.send_message(message.chat.id, 'Удачное предположение. Продолжим?...')
        bot.register_next_step_handler(message, game)
        if dict_of_players[message.chat.id][2] == dict_of_players[message.chat.id][1]:
            dict_of_players[message.chat.id][7] = True
            bot.send_message(message.chat.id,
                             f'... но в следюущей игре! Поздравляю, {dict_of_players[message.chat.id][0]}! Всё получилось!')
            message = bot.send_message(message.chat.id,
                                       'Ну что, сыграем ещё раз...?? Ответь, пожалуйста, "да" или "нет" :)')
            bot.register_next_step_handler(message, good_bye_or_not)

    elif message.text.upper() == dict_of_players[message.chat.id][1]:
        dict_of_players[message.chat.id][7] = True
        bot.send_message(message.chat.id,
                         f'... но в следующей игре! Поздравляю, {dict_of_players[message.chat.id][0]}! Всё получилось!')
        message = bot.send_message(message.chat.id,
                                   'Ну что, сыграем ещё раз...?? Ответь, пожалуйста, "да" или "нет" :)')
        bot.register_next_step_handler(message, good_bye_or_not)

    elif message.text.upper() != dict_of_players[message.chat.id][1] and len(message.text) == \
            dict_of_players[message.chat.id][3] and dict_of_players[message.chat.id][4] != 0:
        dict_of_players[message.chat.id][4] -= 1
        bot.send_message(message.chat.id, display_hangman(dict_of_players[message.chat.id][4]))
        dict_of_players[message.chat.id][6].append(message.text)
        bot.send_message(message.chat.id, f'Предположенные слова: {dict_of_players[message.chat.id][6]}')
        message = bot.send_message(message.chat.id, 'Стой-стой-стой, а если подумать?')
        bot.register_next_step_handler(message, game)

    elif message.text.upper() not in dict_of_players[message.chat.id][1] and len(message.text) == 1 and \
            dict_of_players[message.chat.id][4] != 0:
        dict_of_players[message.chat.id][5].append(message.text)
        dict_of_players[message.chat.id][4] -= 1
        bot.send_message(message.chat.id, display_hangman(dict_of_players[message.chat.id][4]))
        bot.send_message(message.chat.id, f'Предположенные слова: {dict_of_players[message.chat.id][6]}')
        bot.send_message(message.chat.id, f'Предположенные буквы: {dict_of_players[message.chat.id][5]}')
        bot.send_message(message.chat.id, f'Осталось попыток: {dict_of_players[message.chat.id][4]}')
        message = bot.send_message(message.chat.id, 'Ничего, попробуем ещё раз...')
        bot.register_next_step_handler(message, game)

    elif dict_of_players[message.chat.id][4] == 0:
        bot.send_message(message.chat.id,
                         f'... но, походу, в следующий раз. Загаданное слово было {dict_of_players[message.chat.id][1]}')
        message = bot.send_message(message.chat.id,
                                   'Ну что, сыграем ещё раз...?? Ответь, пожалуйста, "да" или "нет" :)')
        bot.register_next_step_handler(message, good_bye_or_not)

    else:
        if dict_of_players[message.chat.id][4] != 0:
            message = bot.send_message(message.chat.id, 'Введи, пожалуйста, букву, камон, ты хочешь играть ваще?')
            bot.register_next_step_handler(message, game)


def good_bye_or_not(message):
    if message.text == 'да':
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.from_user.id,
                         'Лови огромный плюс в твою карму ➕ :)) ')
        with open('dict_of_players.txt', 'w') as f:
            json.dump(dict_of_players, f)
        bot.stop_bot()