import sqlite3
from ConfigChatGPT import Description_Prompt_gpt_text
allNeiro = {
    "GPT_text": False,
    "GPT_image": False
}

def initialize_all_database(user_id):
    bd = sqlite3.connect('Neiro.bd')
    cur = bd.cursor()
    
    cur.execute(f"""CREATE TABLE IF NOT EXISTS Prompts_Gpt_text(
                user_id TEXT PRIMARY KEY,
                last_prompt TEXT DEFAULT None,
                last_answer_gpt TEXT DEFAULT None,
                context TEXT  DEFAULT None,
                Count_Prompt INTEGER DEFAULT 0
               )""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS Prompts_Gpt_image(
                user_id TEXT PRIMARY KEY,
                last_prompt TEXT DEFAULT None
               )""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS ActiveNeiro(
                user_id PRIMARY KEY,
                GPT_text BOOL,
                GPT_image BOOL
                )""")
    cur.execute("INSERT INTO Prompts_Gpt_text (user_id, context) VALUES (?,?)", (user_id,Description_Prompt_gpt_text))
    bd.commit()
    cur.close()

def add_prompt_GPT_text(user_id, prompt, last_answer ):
    bd = sqlite3.connect('Neiro.bd')
    cur = bd.cursor()
    
    cur.execute("SELECT * FROM Prompts_Gpt_text WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    
    if result:
        cur.execute("UPDATE Prompts_Gpt_text SET last_prompt = ?,context = ?, Count_Prompt = ? ",(None,None,None))
        cur.execute("UPDATE Prompts_Gpt_text SET last_prompt = ? = ?, context = ?, Count_Prompt = ? ", (prompt, prompt, result[4]+1 ))
        print(result)
    else:
        cur.execute("INSERT INTO Prompts_Gpt_text (user_id, last_prompt) VALUES(?, ?)", (user_id, prompt))
    if last_answer != None:
        cur.execute("UPDATE Prompts_Gpt_text SET last_answer_gpt = last_answer WHERE Count_Prompt = ? AND user_id = ?", (result[4], user_id))
    
    bd.commit()
    cur.close()

def check_last_prompt(user_id):
    bd = sqlite3.connect('Neiro.bd')
    cur = bd.cursor()
    cur.execute("SELECT Count_Prompt, context, last_answer_gpt FROM Prompts_Gpt_text WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    if result != None: 
        cur.close()
        bd.commit()
        print(f"{result} 71 строка")
        return result
    else:
        cur.close()
        bd.commit()
        print(f"{result} 75 строка")
        return None
    
    
# Остальные функции базы данных...



# def add_prompt_GPT_image(user_id,prompt):
#     bd = sqlite3.connect('Neiro.bd')
#     cur = bd.cursor()
#     cur.execute("SELECT * FROM Prompts_Gpt_image WHERE user_id = ?", (user_id,))
#     result = cur.fetchall()
#     if result:
#         cur.execute("UPDATE Prompts_Gpt_image last_prompt =  ?",(prompt))
#     else:
#         cur.execute("INSERT INTO Prompts_Gpt_image (user_id, last_prompt) VALUES()", (user_id,prompt))



# def Active_neiro(user_id, name_neiro):
#     bd = sqlite3.connect('Neiro.bd')
#     cur = bd.cursor()
#     cur.execute("SELECT user_id form ActiveNeiro")
