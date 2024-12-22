from aiogram.filters import CommandStart,Command
from aiogram.fsm.context import FSMContext
import os
import States as STS 
from aiogram import Router
from aiogram.types import Message, CallbackQuery,FSInputFile
import aiohttp
import time
from database.database import get_answer_gpt
router = Router()
models = ['Got4-o','flux', 'gpt-3.5-turbo']

@router.message(CommandStart())
async def cmd_start(msg:Message):
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
@router.message(STS.ChatGPT.Prompt)
async def generateAnswerGPT(message: Message, state: FSMContext):
    prompt = message.text

    # Отправляем запрос к FastAPI
    url = f"http://localhost:8000/GPT/{message.chat.id}/{prompt}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                answer = get_answer_gpt(message.chat.id)
                await message.answer(f'ChatGPT-4o: {answer}')
            else:
                await message.answer("Произошла ошибка. Пожалуйста, попробуйте снова.")
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
                print(answer)
                script_dir = os.path.dirname(__file__)
                photos_directory = os.path.join(script_dir, '../../generated_images')

                file_path = f"{photos_directory}/{answer}"

                if os.path.isfile(file_path):
                    await message.answer_photo(photo=FSInputFile(file_path, filename='Фотография'), caption='Вот ваше фото!')
                else:
                    await message.answer("Ошибка: файл изображения не найден.")
            else:
                await message.answer("Произошла ошибка при получении изображения от FastAPI.")
               


    







