import sqlite3
import os
def create_table():
    bd = sqlite3.connect('Neiro.bd')
    cur = bd.cursor()
    # Создаём таблицу, если она ещё не существует
    cur.execute("""CREATE TABLE IF NOT EXISTS ContextGPT(
                user_id TEXT,
                context TEXT
                )""")
    bd.commit()
    cur.close()

def add_answer_gpt(user_id, answer, prompt):
    create_table()  # Убедитесь, что таблица существует
    bd = sqlite3.connect('Neiro.bd')
    cur = bd.cursor()
    cur.execute(f"SELECT context,user_id FROM ContextGPT WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    if result:
        cur.execute("UPDATE ContextGPT SET context = ? WHERE user_id = ?",
                    (None, user_id))
        cur.execute("UPDATE ContextGPT SET context = ? WHERE user_id = ?",
                    (result[0] + "Я:" + prompt + "Ты:" + answer, user_id))
    else:
        cur.execute("INSERT INTO ContextGPT (user_id,context) VALUES(?,?)",
                    (user_id, "Я:" + prompt + "Ты:" + answer))

    bd.commit()
    cur.close()

def get_answer_gpt(user_id):
    create_table()
    bd = sqlite3.connect('Neiro.bd')
    cur = bd.cursor()
    cur.execute(f"SELECT context FROM ContextGPT WHERE user_id = {user_id}")
    try:
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return False
    except:
        return False
    
def clear_context(user_id):
    bd = sqlite3.connect('Neiro.bd')
    cur = bd.cursor()
    cur.execute(f"SELECT context,user_id FROM ContextGPT WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    if result:
        cur.execute("UPDATE ContextGPT SET context = ? WHERE user_id = ?",
                    (None, user_id))
        return True
    else:
        return False
    
def get_all_users():
    bd = sqlite3.connect('Neiro.bd')
    cur = bd.cursor()
    cur.execute("SELECT user_id FROM ContextGPT")
    users = cur.fetchall()
    return users