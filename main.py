from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.fsm import State, StatesGroup, FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import sqlite3
import logging
from config import TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    course = State()
    gender = State()

def init_db():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        course TEXT NOT NULL)
        ''')
    conn.commit()
    conn.close()

init_db()

# Инициализация бота и маршрутизатора
bot = Bot(token=TOKEN)
storage = MemoryStorage()
router = Router()

@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await message.answer('Привет. Как тебя зовут?')
    await state.set_state(Form.name)

@router.message(Form.name)
async def name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Сколько тебе лет?')
    await state.set_state(Form.age)

@router.message(Form.age)
async def age_handler(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer('На каком курсе ты учишься?')
    await state.set_state(Form.course)

@router.message(Form.course)
async def course_handler(message: types.Message, state: FSMContext):
    await state.update_data(course=message.text)
    await message.answer('Укажите пол? (м/ж)')
    await state.set_state(Form.gender)

@router.message(Form.gender)
async def gender_handler(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    user_data = await state.get_data()

    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO users (name, age, course, gender) VALUES (?, ?, ?, ?)''',
    (user_data['name'], user_data['age'], user_data['course'], user_data['gender']))
    conn.commit()
    conn.close()

    await message.answer('Данные сохранены!')

@router.message(Command('stats'))
async def stats(message: types.Message):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    # Запрос статистики по возрасту и курсу
    cur.execute('''
    SELECT age, course, COUNT(*) FROM users GROUP BY age, course
    ''')
    age_course_stats = cur.fetchall()

    # Запрос статистики по полу на курсе
    cur.execute('''
    SELECT course, gender, COUNT(*) FROM users GROUP BY course, gender
    ''')
    gender_stats = cur.fetchall()

    conn.close()

    # Формирование ответа
    response = "Статистика:\n"

    response += "Количество студентов по возрасту и курсу:\n"
    for age, course, count in age_course_stats:
        response += f"Возраст: {age}, Курс: {course}, Количество: {count}\n"

    response += "\nКоличество мальчиков и девочек на курсах:\n"
    for course, gender, count in gender_stats:
        response += f"Курс: {course}, Пол: {gender}, Количество: {count}\n"

    await message.answer(response)

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(bot, router)
