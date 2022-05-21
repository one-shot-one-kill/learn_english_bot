from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from random import choice

from config import *
import keyboards as kb
import sql


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

words = {}


class WordState(StatesGroup):
    word = State()
    translate = State()
    delete = State()


class LearningState(StatesGroup):
    learn = State()
    learn_ru = State()


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await bot.send_message(message.from_user.id, "Menu:", reply_markup=kb.start_key_mark)


@dp.message_handler(text_contains='Add word', state=None)
async def add_word(message: types.Message):
    await message.answer("Enter word: ")
    await WordState.word.set()


@dp.message_handler(state=WordState.word)
async def translate_word(message: types.Message, state: FSMContext):
    await state.update_data(word=message.text)
    await message.answer("Enter translate: ")
    await WordState.next()


@dp.message_handler(state=WordState.translate)
async def translate_word(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if sql.add_words(data['word'], message.text) == 1:
        await message.answer(sql.show_words())
    else:
        sql.add_words(data['word'], message.text)
        await message.answer("Word added")
    await state.finish()


@dp.message_handler(text_contains="ENG-RU", state=None)
async def learn_words(message: types.Message, state: FSMContext):
    global words
    words = sql.show_words()
    await LearningState.learn.set()
    await state.update_data(word=choice(list(words.keys())))
    data = await state.get_data()
    await message.answer(data['word'])


@dp.message_handler(state=LearningState.learn)
async def enter_translate(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == words[data['word']]:
        await state.finish()
        await learn_words(message, state)
    elif message.text == 'stop' or message.text == 'стоп':
        await state.finish()
        await message.answer("Learning stopped")
    else:
        await state.finish()
        await message.answer(f"Wrong! Correct answer {words[data['word']]}")
        await learn_words(message, state)


@dp.message_handler(text_contains="RU-ENG", state=None)
async def learn_words_ru(message: types.Message, state: FSMContext):
    global words
    words = sql.show_words_ru()
    await LearningState.learn_ru.set()
    await state.update_data(word=choice(list(words.keys())))
    data = await state.get_data()
    await message.answer(data['word'])


@dp.message_handler(state=LearningState.learn_ru)
async def enter_translate_ru(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == words[data['word']]:
        await state.finish()
        await learn_words_ru(message, state)
    elif message.text == 'stop' or message.text == 'стоп':
        await state.finish()
        await message.answer("Learning stopped")
    else:
        await state.finish()
        await message.answer(f"Wrong! Correct answer {words[data['word']]}")
        await learn_words_ru(message, state)


@dp.message_handler(text_contains='Delete word', state=None)
async def delete_word(message: types.Message):
    await message.answer("Enter delete word:")
    await WordState.delete.set()


@dp.message_handler(state=WordState.delete)
async def delete_word_second(message: types.Message, state: FSMContext):
    sql.delete_word(message.text)
    await message.answer("Word deleted")
    await state.finish()


@dp.message_handler(text_contains='Show words')
async def show_words(message: types.Message):
    words_list = sql.show_words()
    for key, word in words_list.items():
        await message.answer(f"{key} - {word}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)