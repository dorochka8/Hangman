import json
import random
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
    if message.text == 'Hello':
        bot.send_message(message.from_user.id, "Hooray, we have found a common language! \
        \nWell hello, now let's try to play hangman")
        message = bot.send_message(message.chat.id, "Please introduce yourself :)")
        bot.register_next_step_handler(message, name)
    elif message.text == '/help':
        bot.send_message(message.from_user.id, "Come on, go ahead and write the word 'Hello'.")
    else:
        bot.send_message(message.from_user.id, "I don't understand anything :(\
        \nSo, let's start with something small - just write 'Hello' \
        \n(Hint, Hello with a capital H :))!")

def name(message):
    name = message.text
    if message.chat.id not in dict_of_players_old:
        dict_of_players[message.chat.id] = [name]
    bot.send_message(message.chat.id, f'Hello, {dict_of_players[message.chat.id][0]}!')
    bot.send_message(message.chat.id, "Well-well-well, while you're exclaiming in disbelief, I'll take this time to think of a word. Just hold on a moment.")
    time.sleep(1)
    bot.send_message(message.chat.id, f"{dict_of_players[message.chat.id][0]}, while I'm thinking of a word, let me remind you of the rules: \
    \nI will think of a word in English! \
    \nThe letters are replaced with '_' symbols. No numbers. \
    \nSeems super easy, right? You'll have the opportunity to make 6 mistakes. \
    \nPlease writ after my answers, do NOT write more than a letter at once. ")
    message = bot.send_message(message.chat.id, 'We are ready to start! Wait for the word ...')
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
    bot.send_message(message.chat.id, f'The word contains {dict_of_players[message.chat.id][3]} letters')
    time.sleep(0.5)
    bot.send_message(message.chat.id, f'The word itself: {dict_of_players[message.chat.id][2]}\
\nPlease enter a letter that, in your opinion, might be in the guessed word')
    time.sleep(0.5)
    bot.register_next_step_handler(message, game)


def game(message):
    print(dict_of_players)
    if message.text.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and message.text.upper() in \
            dict_of_players[message.chat.id][1] and len(message.text) == 1:
        message.text = message.text.upper()
        dict_of_players[message.chat.id][5].append(message.text)
        for i in range(dict_of_players[message.chat.id][3]):
            if dict_of_players[message.chat.id][1][i] == message.text:
                dict_of_players[message.chat.id][2] = dict_of_players[message.chat.id][2][:i] + message.text + \
                                                      dict_of_players[message.chat.id][2][i + 1:]
        bot.send_message(message.chat.id, dict_of_players[message.chat.id][2])
        bot.send_message(message.chat.id, f'Guessed letters: {dict_of_players[message.chat.id][5]}')
        message = bot.send_message(message.chat.id, 'Great suggestion. Go on. Next letter will be ...')
        bot.register_next_step_handler(message, game)
        if dict_of_players[message.chat.id][2] == dict_of_players[message.chat.id][1]:
            dict_of_players[message.chat.id][7] = True
            bot.send_message(message.chat.id,
                             f'... but in the net game! Congratulations, {dict_of_players[message.chat.id][0]}! You did it!')
            message = bot.send_message(message.chat.id,
                                       'Would you like to play once again...?? Please answer "y" or "n" :)')
            bot.register_next_step_handler(message, good_bye_or_not)

    elif message.text.upper() == dict_of_players[message.chat.id][1]:
        dict_of_players[message.chat.id][7] = True
        bot.send_message(message.chat.id,
                         f'... but in the net game! Congratulations, {dict_of_players[message.chat.id][0]}!  You did it!')
        message = bot.send_message(message.chat.id,
                                   'Would you like to play once again...?? Please answer "y" or "n" :)')
        bot.register_next_step_handler(message, good_bye_or_not)

    elif message.text.upper() != dict_of_players[message.chat.id][1] and len(message.text) == \
            dict_of_players[message.chat.id][3] and dict_of_players[message.chat.id][4] != 0:
        dict_of_players[message.chat.id][4] -= 1
        bot.send_message(message.chat.id, display_hangman(dict_of_players[message.chat.id][4]))
        dict_of_players[message.chat.id][6].append(message.text)
        bot.send_message(message.chat.id, f'Guessed words: {dict_of_players[message.chat.id][6]}')
        message = bot.send_message(message.chat.id, 'Wrong, think a bit!')
        bot.register_next_step_handler(message, game)

    elif message.text.upper() not in dict_of_players[message.chat.id][1] and len(message.text) == 1 and \
            dict_of_players[message.chat.id][4] != 0:
        dict_of_players[message.chat.id][5].append(message.text)
        dict_of_players[message.chat.id][4] -= 1
        bot.send_message(message.chat.id, display_hangman(dict_of_players[message.chat.id][4]))
        bot.send_message(message.chat.id, f'Guessed words: {dict_of_players[message.chat.id][6]}')
        bot.send_message(message.chat.id, f'Guessed letters: {dict_of_players[message.chat.id][5]}')
        bot.send_message(message.chat.id, f'Remaining attempts: {dict_of_players[message.chat.id][4]}')
        message = bot.send_message(message.chat.id, "No worries, let's try again ...")
        bot.register_next_step_handler(message, game)

    elif dict_of_players[message.chat.id][4] == 0:
        bot.send_message(message.chat.id,
                         f'... but it seems, next time. The guessed word was {dict_of_players[message.chat.id][1]}')
        message = bot.send_message(message.chat.id,
                                   'Would you like to play once again...?? Please answer "y" or "n" :)')
        bot.register_next_step_handler(message, good_bye_or_not)

    else:
        if dict_of_players[message.chat.id][4] != 0:
            message = bot.send_message(message.chat.id, 'Please enter a letter, come on, do you even want to play?')
            bot.register_next_step_handler(message, game)


def good_bye_or_not(message):
    if message.text == 'y':
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.from_user.id,
                         'Catch a huge plus for your karma ➕ :)) ')
        with open('dict_of_players.txt', 'w') as f:
            json.dump(dict_of_players, f)
        bot.stop_bot()
