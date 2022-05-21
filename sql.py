import sqlite3
import random


db = sqlite3.connect('english.db')
sql = db.cursor()


def delete_word(value):
    sql.execute(f"DELETE FROM words WHERE eng = '{value.lower()}'")
    db.commit()


def add_words(value, value2):
    sql.execute(f"SELECT eng FROM words WHERE eng = '{value}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO words VALUES (?, ?)", (value.lower(), value2.lower()))
        db.commit()
    else:
        return 1


def show_words():
    words = {}
    for i in sql.execute("SELECT eng, rus FROM words"):
        words[i[0]] = i[1]
    return words


def show_words_ru():
    words = {}
    for i in sql.execute("SELECT eng, rus FROM words"):
        words[i[1]] = i[0]
    return words

# d = show_words()
# print(d[random.choice(list(d.keys()))])