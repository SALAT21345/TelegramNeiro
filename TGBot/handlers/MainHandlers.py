from aiogram.filters import CommandStart,Command
from aiogram.fsm.context import FSMContext
import os
import States as STS 
from aiogram import Router
from aiogram.types import Message, CallbackQuery,FSInputFile
import aiohttp
from database.database import add_prompt_GPT_text, initialize_all_database, check_last_prompt
from ConfigChatGPT import Description_Prompt_gpt_text
router = Router()
models = ['Got4-o','flux', 'gpt-3.5-turbo']

@router.message(CommandStart())
async def cmd_start(msg:Message):
    initialize_all_database(msg.chat.id) 
    await msg.answer("""Я - Салат бот.
                     
Что я умею на данный момент? 
✅ChatGPT-4o : /GPT
✅Генерация фото : /GenerateImage
""")

@router.message(Command('Stop'))
async def cmd_stop(message: Message, state:FSMContext):
    await state.clear()
@router.message(Command('GPT'))
async def GPT(message:Message, state: FSMContext):
    await message.answer('ChatGPT ожидает вашего вопроса')
    await state.set_state(STS.ChatGPT.Prompt)
    


# @router.message(STS.ChatGPT.Prompt)
# async def generateAnswerGPT(message: Message, state: FSMContext):

#     result = check_last_prompt(message.chat.id)
#     # await message.answer(f'DEBUG: Проверка "что возвращается в 35 строке" {result}')
#     # result[0] -- Номер промпта 
#     prompt = message.text
    
#     if result[0] != None:
#         await message.answer('выполнилась 40 строка')
#         prompt = f"Диалог№{result[0]}: я:{message.text}. Ты:"
#         # print(prompt)
#         # print(result[1])
#         prompt = f'{result[1]}' + " " + f'{prompt}'

#         await message.answer('выполнилась 47 строка')
#         add_prompt_GPT_text(message.chat.id, prompt)

@router.message(STS.ChatGPT.Prompt)
async def generateAnswerGPT(message: Message, state: FSMContext):

    result = check_last_prompt(message.chat.id)
    # await message.answer(f'DEBUG: Проверка "что возвращается в 35 строке" {result}')
    # result[0] -- Номер промпта 
    prompt = message.text
    
    if result[2] != None:
        prompt = f'{result[1]} Диалог №{result[0]}: \nЯ: {prompt}.\nТы:{result[2]}.'

    await message.answer(f'На сервер отправляется промпт: {prompt}')
    url = f"http://localhost:8000/GPT/{prompt}"
    async with aiohttp.ClientSession() as session:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    answer = await response.text()
                    answer = answer.strip('"') 
                    answer = answer.replace('/n', '\n')
                    await message.answer(f'{answer}')
                    add_prompt_GPT_text(message.chat.id, prompt, answer)
                else:
                    await message.answer("У-псс.. произошла ошибочка... попробуйте снова")
                    await state.clear()


@router.message(Command('GenerateImage'))
async def get_prompt_generate_image(message:Message,state:FSMContext):
    await message.answer('Введите ваш запрос.\nP.s: Запросы на английском лучше обрабатываются.')
    await state.set_state(STS.Image.SendImage)

@router.message(STS.Image.SendImage)
async def generate_image(message: Message, state: FSMContext):
    prompt = str(message.text)
    url = f"http://localhost:8000/GPT/Image/{prompt}"
    await message.answer("Мы получили ваш запрос, ожидайте!")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                answer = await response.text()
                answer = os.path.basename(answer)
                answer = answer.replace('"', '')
                script_dir = os.path.dirname(__file__)
                photos_directory = os.path.join(script_dir, '../../generated_images')

                file_path = f"{photos_directory}/{answer}"

                if os.path.isfile(file_path):
                    await message.answer_photo(photo=FSInputFile(file_path, filename='Фотография'), caption='Вот ваше фото!')
                else:
                    await message.answer("Ошибка: файл изображения не найден.")
            else:
                await message.answer("Произошла ошибка при получении изображения от FastAPI.")
               


    







