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
    cur.execute("""CREATE TABLE IF NOT EXISTS GeneratePhoto(
                user_id TEXT,
                last_prompt TEXT
                )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS TokensAndAccess(
                user_id TEXT,
                Tokens INTEGER,
                GPT BOOL,
                GeneratePhoto BOOL
                )""")
    bd.commit()
    cur.close()
    
def inicialize_sub(user_id):
    create_table()  # Убедитесь, что таблица существует
    bd = sqlite3.connect('Neiro.bd')
    cur = bd.cursor()
    cur.execute("SELECT * FROM TokensAndAccess WHERE user_id =?",(user_id,))
    result = cur.fetchone()
    if result !=None:
        print(f'функиця inicialize_sub 31 Строка::: {result}')
        cur.close()
        bd.close()
    else:
        cur.execute(f"INSERT INTO TokensAndAccess (user_id,Tokens,GPT,GeneratePhoto) VALUES ({user_id},0,{False},{False})")
        print('функиця inicialize_sub 36 Строка')
        bd.commit()
        bd.close()





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
        bd.commit()
        cur.close()
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
        bd.commit()
        return True
    else:
        return False
    
def get_all_users():
    bd = sqlite3.connect('Neiro.bd')
    cur = bd.cursor()
    cur.execute("SELECT user_id FROM ContextGPT")
    users = cur.fetchall()
    return users

def add_last_promt_generate_photo(user_id, prompt):
    create_table()
    print('Запрос добавился')
    bd = sqlite3.connect("Neiro.bd")
    cur = bd.cursor()
    cur.execute(f'SELECT * FROM GeneratePhoto WHERE user_id = {user_id}')
    result = cur.fetchone()
    if result:
        cur.execute("UPDATE GeneratePhoto SET last_prompt = ? WHERE user_id = ? ", (prompt, user_id))
    else:
        cur.execute("INSERT INTO GeneratePhoto (user_id,last_prompt) VALUES(?,?)", (user_id, prompt))
    bd.commit()
    cur.close()
    bd.close()

def get_last_promt_generate_photo(user_id):
    create_table()
    bd = sqlite3.connect("Neiro.bd")
    cur = bd.cursor()
    cur.execute(f'SELECT * FROM GeneratePhoto WHERE user_id = {user_id}')
    result = cur.fetchone()
    print(f'{result} в 91 строке')
    print(result[0])
    print(result[0][0])
    cur.execute("SELECT last_prompt FROM GeneratePhoto WHERE user_id = ? ", (user_id))
    result = cur.fetchone()

    return result[0]

def BayGPT(user_id):
    create_table()
    bd = sqlite3.connect("Neiro.bd")
    cur = bd.cursor()
    HaveSubGPT = Have_subscription(user_id,'GPT')
    if HaveSubGPT == True:
        print(f"BD 131 строка: уже имеет аккаунт.")
        return 'Ошибка: Пользователь уже имеет подписку на ChatGPT'
    elif HaveSubGPT == False:
        cur.execute(f"SELECT user_id FROM TokensAndAccess WHERE user_id = {user_id}")
        result = cur.fetchone()
        if result != None:
            print(f"Функция BayGPT. добавился user_id: {user_id}")
            cur.execute(f"UPDATE TokensAndAccess SET GPT = True, Tokens = 3 WHERE user_id = {user_id}")
            bd.commit()
            return True
    else:
        print(HaveSubGPT)
        print(f"Функция BayGPT. добавился user_id: {user_id}")
        cur.execute(f"INSERT INTO TokensAndAccess (user_id,GPT,GeneratePhoto,Tokens) VALUES ({user_id}, True,False, 100)")
        bd.commit()
        BayGPT(user_id)
    cur.close()
    bd.commit()
    bd.close()
    

def Have_subscription(user_id,TypeSub): # Принимает два значения: "GPT", "Photo";
    create_table()
    bd = sqlite3.connect("Neiro.bd")
    cur = bd.cursor()
    if TypeSub == 'GPT':
        cur.execute(f"SELECT GPT FROM TokensAndAccess WHERE user_id = {user_id}")
        result = cur.fetchone()
        if result != None:
            if result[0] == True:
                print(f'Строка №157 .Вернулось {result[0]}. True')
                return True
            elif result[0] == False:
                print(f'Строка №159 .Вернулось {result[0]}. False')
                return False
                
        else:
            print(f'Строка №164 .Вернулось {result}. "Возникла ошибка: Пользователь не найден"')
            return 'Возникла ошибка: Пользователь не найден.'
    elif TypeSub == "Photo":
        cur.execute(f"SELECT GeneratePhoto FROM TokensAndAccess WHERE user_id = {user_id}")

def add_Tokens():
    pass

def GetCountTokens(user_id):
    pass


def Reduce_Tokens(user_id):
    bd = sqlite3.connect("Neiro.bd")
    cur = bd.cursor()
    cur.execute(f"SELECT GPT FROM TokensAndAccess WHERE user_id = {user_id}")
    gpt = cur.fetchone()
    if gpt != None:
        if gpt[0] == 1:
            cur.execute(f"SELECT Tokens FROM TokensAndAccess WHERE user_id = {user_id}")
            NewBanalce = cur.fetchone()
            print(NewBanalce[0])
            if NewBanalce[0] >=1:
                NewBanalce = NewBanalce[0] - 1
                cur.execute(f"UPDATE TokensAndAccess SET Tokens = {NewBanalce} WHERE user_id = {user_id}")
                bd.commit()
                return True,NewBanalce
            else:
                return False, 'Not enough tokens'
        else:
            return False, 'Not Have GPT'


def GetInfoForAccunt(user_id):
    bd = sqlite3.connect("Neiro.bd")
    cur = bd.cursor()
    cur.execute(f"SELECT Tokens, GPT, GeneratePhoto FROM TokensAndAccess WHERE user_id = {user_id}")
    result = cur.fetchone()
    cur.execute(f"SELECT * FROM TokensAndAccess")
    result_1 = cur.fetchall()
    print(user_id)
    print(result_1)
    print(result, '202 line')
    if result is not None:
            print(result)
            return result[0], result[1], result[2]
    else:
       return None 