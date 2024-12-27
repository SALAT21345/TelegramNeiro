from aiogram.filters import CommandStart,Command
from aiogram.fsm.context import FSMContext
from aiogram import Router,F
from aiogram.types import Message, CallbackQuery,FSInputFile
from aiogram import types
from aiogram.enums.parse_mode import ParseMode
import States as STS 
from keyboards.MainKeyboards import MainReplyKeyboard,btn_for_answer_gpt
import Config as CFG
import aiohttp
from database.database import add_answer_gpt,get_answer_gpt,clear_context
import g4f
from g4f.client import Client


from translate import Translator
router = Router()
client = Client()

Models_Image = [
    'flux-anime', # 18+ 10/10 ЕСТЬ ВОДЯНОЙ ЗНАК
    'flux-realism', # 18+ 10/10 ЕСТЬ ВОДЯНОЙ ЗНАК
    'flux-4o', # Нет знака. 8/10
]

############################################
#                   Let's Go!              #
############################################


@router.message(CommandStart())
async def cmd_start(msg:Message):
    await msg.answer("""Я - Салат бот.
Что я умею на данный момент? 
✅ChatGPT-4o : /GPT
✅Генерация фото : /GenerateImage

""",reply_markup=MainReplyKeyboard)
    
############################################
#           Handlers message/Command       #
############################################

@router.message(Command('Stop'))
async def cmd_stop(message: Message, state:FSMContext):
    await state.clear()

@router.message(F.text == "GPT")
async def greet_user(message: Message,state: FSMContext):
    await message.answer('ChatGPT ожидает вашего вопроса')
    await state.set_state(STS.ChatGPT.Prompt)

@router.message(Command('GPT'))
async def GPT(message:Message, state: FSMContext):
    await message.answer('ChatGPT ожидает вашего вопроса')
    await state.set_state(STS.ChatGPT.Prompt)

@router.message(F.text == 'Поменять режим')
async def ClearState(message: Message,state:FSMContext):
    await state.clear()
    await message.answer('Нейросеть приостановлена🌀')
    
@router.callback_query(F.data == 'StopNeiro')
async def ClearState(callback:CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('Нейросеть приостановлена🌀')

@router.message(F.text == '👤 Генерация фото')
@router.message(Command('GenerateImage'))
async def get_prompt_generate_image(message:Message,state:FSMContext):
    await message.answer('Введите ваш запрос.\nP.s: Запросы на английском лучше обрабатываются.')
    await state.set_state(STS.Image.SendImage)

@router.callback_query(F.data == 'ClearContext')
async def ClearContext(callback:CallbackQuery):
    answer = clear_context(callback.message.chat.id)
    if answer == True:
        callback.message.answer("Code: Успешно! \nКонтекст сброшен.")
    else:
        callback.message.answer("Ошибка: Возможно, контекста не существовало пока что или вы недавно его отчищали..")
    

############################################
#                  States                  #
############################################


@router.message(STS.ChatGPT.Prompt)
async def generateAnswerGPT(message: Message, state: FSMContext):
    prompt = message.text
    Description = await message.answer('ChatGPT-4o генерирует ответ...')
    Context = get_answer_gpt(message.chat.id)
    if Context != None:
        promptForGPT = f'Ознакомься с нашим диалогом и отвечай изходя из его контекста: {Context}. И мой последний вопрос был: {prompt}'
        response = g4f.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": promptForGPT}],)
    else:
        response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        ) 
    if response:
        await CFG.bot.delete_message(chat_id=message.chat.id, message_id=Description.message_id)
        await message.reply(response,reply_markup=btn_for_answer_gpt)
        add_answer_gpt(message.chat.id, response, prompt)

@router.message(STS.Image.SendImage)
async def generate_image(message: Message, state: FSMContext):
    Content = str(message.text)
    Content = Translete_Prompt(Content)
    response = await client.images.async_generate(
        model="flux",
        prompt=Content,
        response_format="url"
    )
    if response:
        image_url = response.data[0].url
        print(image_url)

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status == 200:
                    await CFG.bot.send_photo(chat_id=message.chat.id, photo=image_url)


############################################
#                   functions              #
############################################


def Translete_Prompt(prompt):
        translator = Translator(from_lang='ru', to_lang='en')
        translated_text = translator.translate(prompt)
        return translated_text


