import sqlite3

def create_table():
    bd = sqlite3.connect('Neiro.bd')
    cur = bd.cursor()
    # Создаём таблицу, если она ещё не существует
    cur.execute("""CREATE TABLE IF NOT EXISTS Answer_gpt(
                user_id TEXT, 
                answer TEXT
                )""")
    bd.commit()
    cur.close()

def add_answer_gpt(user_id, answer):
    # create_table()  # Убедитесь, что таблица существует
    bd = sqlite3.connect('Neiro.bd')
    cur = bd.cursor()
    cur.execute("SELECT user_id FROM Answer_gpt WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    if result:
        # Если данные уже были, заменяем их.
        cur.execute("UPDATE Answer_gpt SET answer = ? WHERE user_id = ?", (answer, user_id))
    else:
        # если данных нет, добавляем новые.
        cur.execute("INSERT INTO Answer_gpt (user_id, answer) VALUES (?, ?)", (user_id, answer))


    cur.execute("SELECT * FROM Answer_gpt")
    result = cur.fetchall()                         # ЗДЕСЬ В ТАБЛИЦЕ ДАННЫЕ ЕСТЬ
    print(f'Вся таблица: {result}')


    bd.commit()
    cur.close()


def get_answer_gpt(user_id):
    # create_table()  # Убедитесь, что таблица существует
    bd = sqlite3.connect('Neiro.bd')
    cur = bd.cursor()


    cur.execute("SELECT * FROM Answer_gpt")
    result = cur.fetchall()             # ЗДЕСЬ МЫ ПОНИМАЕМ, ЧТО ТАБЛИЦА ПУСТАЯ
    print(f'Вся таблица: {result}')


    cur.execute("SELECT user_id, answer FROM Answer_gpt WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    if result:
        return result[1]
    else:
        return False
    
