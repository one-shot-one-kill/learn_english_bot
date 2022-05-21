from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

add_btn = KeyboardButton(text='Add word')
learn_eng_btn = KeyboardButton(text='ENG-RU')
learn_ru_btn = KeyboardButton(text='RU-ENG')
delete_btn = KeyboardButton(text='Delete word')
show_list_btn = KeyboardButton(text='Show words')
start_key_mark = ReplyKeyboardMarkup(resize_keyboard=True).row(learn_eng_btn, learn_ru_btn)\
    .add(show_list_btn).add(add_btn, delete_btn)