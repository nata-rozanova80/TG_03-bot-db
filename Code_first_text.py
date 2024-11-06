# @TG01wetherbot or tg01bot функционал БД про студентов

import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StateGroup
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
import sqlite3
import aiohttp
import logging

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(Level=logging.INFO)

class Form(StateGroup):
    name = State()
    age = State()
    course = State()

def init_db():
    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        course INTEGER NOT NULL)
        ''')
    conn.commit()
    conn.close()

init_db()
















@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /help')

@dp.message(Form.name)  #???????
async def start(message: Message, state: FSMContext):
        await message.answer(f'Привет. Как тебя зовут?')
        await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f'Сколько тебе лет?')
    await state.set_state(Form.age)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f'Сколько тебе лет?')
    await state.set_state(Form.age)

@dp.message(Form.course)
async def course(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
    user_data = await state.get_data()

    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INFO (name, age, course) VALUES (?, ?, ?)''', (user_data['name'], (user_data['age'], (user_data['course']))
    conn.commit()
    conn.close()

    async with aiohttp.ClientSession() as session:
        async with session.get

@dp.message()
async def startall(message: Message):
    await message.answer("Я тебе ответил")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())