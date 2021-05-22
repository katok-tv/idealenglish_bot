import telebot
from settings import TG_TOKEN
import trans_alg
import buttons
import help_information
import bd
import chek_of_knowledge

## создаем экземпляр бота
bot = telebot.TeleBot(TG_TOKEN)

message_text = 'Hello'
message_id = 0
button_status = ''


## Демонстрация главного меню.
#
#  После запуска бота, функция отправляет главное меню
@bot.message_handler(commands=['start'])
def show_main_menu(message):
    buttons.main_menu(message)


@bot.message_handler(commands=['help'])
def launch_help(message):
    help_information.help(message)


@bot.message_handler(content_types='text')
def get_words(message):
    help_information.help_commands(message)
    global message_text, message_id, button_status
    message_text = message.text
    message_id = int(message.from_user.id)
    if button_status == 'add':
        buttons.LocalButtons(message).creating_keyboard(message)
    if button_status == 'trans':
        inform = 'Введи слово, которое хочешь перевести:'
        trans_alg.translation_function(message_text, message_id)
        bot.send_message(message.from_user.id, inform)


## Обработка нажатия на кнопку "Добавить слова"
#
#  Функция отправляет уведомление о переходе в режим "Добавить слова".
@bot.callback_query_handler(func=lambda call: call.data == buttons.add_word)
def add_word_function(call):
    global button_status, message_text, message_id
    bot.answer_callback_query(callback_query_id=call.id, text='')
    inform = 'Добавь слова в формате: Английское слово.Русский перевод'
    bot.send_message(call.from_user.id, inform)
    button_status = 'add'



## Обработка нажатия на кнопку "Учить слова"
#
#  Функция отправляет уведомление о переходе в режим "Учить слова".
#  Отправляет пользователю клавиатуру, для работы в режиме "Учить слова"
@bot.callback_query_handler(func=lambda call: call.data == buttons.learn_words)
def learn_word_function(call):
    inform = 'Давай поучим новые слова! (в разработке)'
    bot.send_message(call.from_user.id, inform)
    buttons.LocalButtonsLearning(call).creating_keyboard(call)
    bot.answer_callback_query(callback_query_id=call.id, text='')


## Обработка нажатия на кнопку "Проверить знания"
#
#  Функция отправляет уведомление о переходе в режим "Проверить знания".
#  Отправляет пользователю клавиатуру, для работы в режиме "Проверить знания"
@bot.callback_query_handler(
    func=lambda call: call.data == buttons.check_knowledge)
def check_knowledge_function(call):
    inform = 'Пора проверить твои знания (в разработке)'
    bot.send_message(call.from_user.id, inform)
    buttons.LocalButtonsChecking(call).creating_keyboard(call)
    bot.answer_callback_query(callback_query_id=call.id, text='')


## Обработка нажатия на кнопку "Переводчик"
#
#  Функция отправляет уведомление о переходе в режим "Переводчик".
#  Запускает функцию Перевода в реальном времени
@bot.callback_query_handler(func=lambda call: call.data == buttons.translate)
def translator_function(call):
    global message_text, button_status
    message_text = 'Hello'
    button_status = 'trans'
    bot.answer_callback_query(callback_query_id=call.id, text='')
    inform = 'Введи слово, которое хочешь перевести:'
    bot.send_message(call.from_user.id, inform)


## Обработка нажатия на кнопку "Выход в главное меню"
#
#  Запускает функцию Демонстрация главного меню
@bot.callback_query_handler(
    func=lambda call: call.data == buttons.exit_to_main_menu)
def back_to_main_menu_function(call):
    bot.send_message(call.from_user.id, 'Чуи, мы дома')
    show_main_menu(call)
    bot.answer_callback_query(callback_query_id=call.id, text='')


@bot.callback_query_handler(func=lambda call: call.data == buttons.approve)
def approve_button_func(call):
    bd.add_to_db(message_text, message_id)
    info = 'Ваше слово/предложение добавлено в словарь'
    bot.send_message(call.from_user.id, info)
    bot.answer_callback_query(callback_query_id=call.id, text='')
    buttons.LocalButtons(call).creating_keyboard(call)


@bot.callback_query_handler(func=lambda call: call.data == buttons.quiz)
def quiz_button_func(call):
    buttons.QuizGameButtons(call).creating_keyboard(call)
    bot.answer_callback_query(callback_query_id=call.id, text='')


@bot.callback_query_handler(func=lambda call: call.data == buttons.eng_rus)
def eng_rus_button_func(call):
    chek_of_knowledge.eng_rus_quiz(bd.take_user_words(
        call.from_user.id),
        bd.take_other_words(), call)
    bot.answer_callback_query(callback_query_id=call.id, text='')


@bot.callback_query_handler(func=lambda call: call.data == buttons.rus_eng)
def rus_eng_button_func(call):
    chek_of_knowledge.rus_eng_quiz(bd.take_user_words(
        call.from_user.id),
        bd.take_other_words(), call)
    bot.answer_callback_query(callback_query_id=call.id, text='')


@bot.callback_query_handler(
    func=lambda call: call.data == buttons.easy_translate)
def easy_translate_button_func(call):
    buttons.LettersGameButtons(call).creating_keyboard(call)
    bot.answer_callback_query(callback_query_id=call.id, text='')


@bot.callback_query_handler(
    func=lambda call: call.data == buttons.letters_rus_eng)
def letters_rus_eng_button_func(call):
    chek_of_knowledge.rus_eng_letters(
        bd.take_user_words(call.from_user.id), call)
    bot.answer_callback_query(callback_query_id=call.id, text='')


@bot.callback_query_handler(
    func=lambda call: call.data == buttons.letters_eng_rus)
def letters_eng_rus_button_func(call):
    chek_of_knowledge.eng_rus_letters(
        bd.take_user_words(call.from_user.id), call)
    bot.answer_callback_query(callback_query_id=call.id, text='')


@bot.callback_query_handler(
    func=lambda call: call.data == buttons.eng_next_word)
def eng_next_word_button_func(call):
    chek_of_knowledge.eng_rus_quiz(chek_of_knowledge.take_user_words(
        call.from_user.id),
        chek_of_knowledge.take_other_words(), call)
    bot.answer_callback_query(callback_query_id=call.id, text='')


@bot.callback_query_handler(
    func=lambda call: call.data == buttons.back_to_games)
def back_to_games_button_func(call):
    buttons.LocalButtonsChecking(call).creating_keyboard(call)
    bot.answer_callback_query(callback_query_id=call.id, text='')


@bot.callback_query_handler(
    func=lambda call: call.data == buttons.rus_next_word)
def rus_next_word_button_func(call):
    chek_of_knowledge.rus_eng_quiz(chek_of_knowledge.take_user_words(
        call.from_user.id),
        chek_of_knowledge.take_other_words(), call)
    bot.answer_callback_query(callback_query_id=call.id, text='')


@bot.callback_query_handler(func=lambda call: True)
def checking_answer(call):
    if call.data == chek_of_knowledge.eng_user_word:
        bot.send_message(call.from_user.id, chek_of_knowledge.eng_inform1)
        buttons.InEngQuizButtons(call).creating_keyboard(call)
    if call.data == chek_of_knowledge.eng_random_word:
        bot.send_message(call.from_user.id, chek_of_knowledge.eng_inform2)
        buttons.InEngQuizButtons(call).creating_keyboard(call)
    if call.data == chek_of_knowledge.rus_user_word:
        bot.send_message(call.from_user.id, chek_of_knowledge.rus_inform1)
        buttons.InRusQuizButtons(call).creating_keyboard(call)
    if call.data == chek_of_knowledge.rus_random_word:
        bot.send_message(call.from_user.id, chek_of_knowledge.rus_inform2)
        buttons.InRusQuizButtons(call).creating_keyboard(call)
    bot.answer_callback_query(callback_query_id=call.id, text='')


bot.polling(none_stop=True, interval=0)
