import telebot
from telebot import types
import sqlite3
import random
from config import TOKEN
from logik import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Регистрация")
    button2 = types.KeyboardButton("Войти")
    button3 = types.KeyboardButton("Я учитель")
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, "Привет! Выберите действие:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Регистрация")
def register(message):
    msg = bot.send_message(message.chat.id, "Введите ваше имя для регистрации:")
    bot.register_next_step_handler(msg, process_registration)

@bot.message_handler(func=lambda message: message.text == "Я учитель")
def register_teacher(message):
    msg = bot.send_message(message.chat.id, "Введите ваше имя (будет добавлено как учитель):")
    bot.register_next_step_handler(msg, process_teacher_registration)

def process_teacher_registration(message):
    name = message.text
    add_teacher(name)
    bot.send_message(message.chat.id, f"Учитель {name} успешно зарегистрирован! Используйте /teacher для входа.")

@bot.message_handler(func=lambda message: message.text == "Войти")
def login(message):
    msg = bot.send_message(message.chat.id, "Введите ваше имя для входа:")
    bot.register_next_step_handler(msg, process_login)

def process_registration(message):
    name = message.text
    add_student(name)
    bot.send_message(message.chat.id, f"Регистрация прошла успешно, {name}! Теперь выберите: /Войти для входа или /teacher для входа как учитель.")

def process_login(message):
    name = message.text
    student_info = get_student(name)
    if student_info:
        grades, homework = student_info
        bot.send_message(message.chat.id, f"Здравствуйте, {name}! Ваши оценки: {grades}, Ваши домашние задания: {homework}")
    else:
        bot.send_message(message.chat.id, f"Студент с именем {name} не найден. Попробуйте зарегистрироваться.")

@bot.message_handler(commands=['teacher'])
def teacher(message):
    msg = bot.send_message(message.chat.id, "Введите ваше имя (для входа как учитель):")
    bot.register_next_step_handler(msg, process_teacher_login)

def process_teacher_login(message):
    name = message.text
    if is_teacher(name):
        msg = bot.send_message(message.chat.id, "Введите имя ученика для выставления оценок:")
        bot.register_next_step_handler(msg, ask_grades_homework)
    else:
        bot.send_message(message.chat.id, "Вы не учитель! Попробуйте еще раз.")

def ask_grades_homework(message):
    student_name = message.text
    msg = bot.send_message(message.chat.id, "Введите оценки ученика:")
    bot.register_next_step_handler(msg, process_grades, student_name)

def process_grades(message, student_name):
    grades = message.text
    msg = bot.send_message(message.chat.id, "Введите домашнее задание ученика:")
    bot.register_next_step_handler(msg, process_homework, (student_name, grades))

def process_homework(message, data):
    student_name, grades = data
    homework = message.text
    update_student_grades(student_name, grades, homework)
    bot.send_message(message.chat.id, f"Оценки и домашнее задание для ученика {student_name} были обновлены!")

# Генерация расписания
subjects_list = [
    'Математика', 'Физика', 'Химия', 'Литература', 'Английский', 'История',
    'Биология', 'География', 'Информатика', 'Спорт', 'Русский язык', 'Музыка', 'Трудовое обучение'
]
days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']

for day in days_of_week:
    random_subjects = random.sample(subjects_list, 5)
    schedule = ', '.join(random_subjects)
    add_schedule(day, schedule)

@bot.callback_query_handler(func=lambda call: True)
def button_callback(call):
    day = call.data
    schedule = get_schedule(day)
    if schedule:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Ваше расписание на {day}:\n{schedule}")
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Расписание на {day} еще не добавлено.")

bot.polling(none_stop=True)