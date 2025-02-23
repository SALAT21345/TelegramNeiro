from aiogram.filters import CommandStart,Command
from aiogram.fsm.context import FSMContext
from aiogram import Router,F
from aiogram.types import Message, CallbackQuery,FSInputFile,LabeledPrice, PreCheckoutQuery
from aiogram import types 
from aiogram.enums.parse_mode import ParseMode
import States as STS 
from keyboards.MainKeyboards import MainReplyKeyboard,btn_for_answer_gpt,Btn_for_Photo,btn_BayChatGPT_StartMenu,Btn_BayTokensOrChatGPT_Menu,Btn_My_Account,btnSelectSub
import Config as CFG
import aiohttp
from database.database import add_answer_gpt,get_answer_gpt,clear_context,add_last_promt_generate_photo,get_last_promt_generate_photo,BayGPT,Have_subscription,Reduce_Tokens,inicialize_sub,GetInfoForAccunt
import g4f
from g4f.client import Client
import time

from translate import Translator
import asyncio
from asyncio import WindowsSelectorEventLoopPolicy

asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
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
    inicialize_sub(msg.chat.id)
    await msg.answer("""Я - Салат бот.
Что я умею на данный момент? 
✅ChatGPT-4o : /GPT
✅Генерация фото : /GenerateImage
✅Информация о подписках: /Shop

""",reply_markup=Btn_My_Account)
    
############################################
#           Handlers message/Command       #
############################################
@router.message(F.text == 'Shop')
@router.message(Command('Shop'))
async def Shop(message:Message):
    await message.answer('......',reply_markup=btnSelectSub)

@router.message(Command('Stop'))
async def cmd_stop(message: Message, state:FSMContext):
    await state.clear()

@router.callback_query(F.data == 'Bay_ChatGPT_start_menu')
async def Bay_ChatGptStart_Menu(callback:CallbackQuery):
    await callback.message.answer("""Выберите подходящую вам услугу:
<b><i>
ХИТЫ ПРОДАЖ : 
— ChatGPT + 300 Токенов | Всего 350 р.
— 1000 токенов | Всего 500 р.
</i></b>
Все услуги: 

• ChatGPT | 185 р.
• ChatGPT + 100 Токенов | 200 р.

• 10 токенов | 25 р. 
• 25 токенов | 50 p. 
• 50 токенов | 75 p.
• 100 токенов  | 100 p.""",reply_markup=Btn_BayTokensOrChatGPT_Menu, parse_mode="html")
    
@router.message(Command('GPT'))
@router.message(F.text == "GPT")
async def greet_user(message: Message,state: FSMContext):
    inicialize_sub(message.chat.id)
    IsHaveSubGpt = Have_subscription(message.chat.id, 'GPT')
    await message.answer(f'ID: {message.chat.id}')
    if IsHaveSubGpt != None or str(message.chat.id) == CFG.admin_id:
        if IsHaveSubGpt == True or str(message.chat.id) == CFG.admin_id:
            await message.answer('ChatGPT ожидает вашего вопроса')
            await state.set_state(STS.ChatGPT.Prompt)
        else:
            await message.answer('У-пс.. Кажется, что у вас нет подписки на ChatGPT😢.\nЖелаете приобрести её?',reply_markup=btn_BayChatGPT_StartMenu)


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
        await callback.message.answer("Code: Успешно! \nКонтекст сброшен.")
    else:
        await callback.message.answer("Ошибка: Возможно, контекста не существовало пока что или вы недавно его отчищали..")

@router.callback_query(F.data == 'AgainPrompt')
async def AgainPrompt(callback: CallbackQuery):
    Content = get_last_promt_generate_photo(callback.message.chat.id)
    await callback.message.answer('Ваш запрос был принят в очередь. ожидайте.')
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
                    await CFG.bot.send_photo(chat_id=callback.message.chat.id, photo=image_url,caption='Повторить последний запрос',reply_markup=Btn_for_Photo)

@router.callback_query(F.data == 'MyAccount')
async def MyAccount(callback: CallbackQuery):
    account_info = GetInfoForAccunt(callback.message.chat.id)
    
    if account_info is not None:
        Tokens, Gpt, Photo = account_info
        
        msg = f"""
Доступные токены💎  |   {Tokens}

Подписка на ChatGPT |   {'✅' if Gpt == 1 else "❌"}

Подписка на Генерацию фото | {'✅' if Photo == 1 else "❌"}
"""
        await callback.message.answer(msg, reply_markup=Btn_BayTokensOrChatGPT_Menu)
    else:
        await callback.message.answer("Информация о вашем аккаунте не найдена.")



@router.callback_query(F.data == 'Bay_Photo_start_menu')
async def BayPhoto(callback:CallbackQuery):
    await callback.message.answer('Покупк Photo')
############################################
#                  States                  #
############################################


@router.message(STS.ChatGPT.Prompt)
async def generateAnswerGPT(message: Message, state: FSMContext):
    Tokens = Reduce_Tokens(message.chat.id)
    time.sleep(1.5)
    if Tokens != None or str(message.chat.id) == CFG.admin_id:
        if Tokens[0] !=False or str(message.chat.id) == CFG.admin_id:
            prompt = message.text
            # if prompt.startswith('!'):
            Description = await message.answer('ChatGPT-4o генерирует ответ...')
            Context = get_answer_gpt(message.chat.id)
            if Context != None:
                promptForGPT = f'Ознакомься с нашим диалогом и отвечай изходя из его контекста: {Context}. И мой последний вопрос был: {prompt}'
                response = g4f.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": promptForGPT}],)
            else:
                response = g4f.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                ) 
            if response:
                try: 
                    await CFG.bot.delete_message(chat_id=message.chat.id, message_id=Description.message_id)
                    await message.reply(response,reply_markup=btn_for_answer_gpt)
                    add_answer_gpt(message.chat.id, response, prompt)
                except:
                    await CFG.bot.delete_message(chat_id=message.chat.id, message_id=Description.message_id)
                    await message.reply('Упс.. Возникла ошибка, попробуйте снова или перефразируйте ваш запрос.',reply_markup=btn_for_answer_gpt)
        else:
            if Tokens[1] == 'Not enough tokens':
                await message.answer('Кажется, у вас закончились токены...  Проверьте ваш аккаунт',reply_markup=Btn_My_Account)
            elif Tokens[1] == 'Not Have GPT':
                await message.answer('Возникла ошибка: У вас нет доступа к ChatGPT')

@router.message(STS.Image.SendImage)
async def generate_image(message: Message, state: FSMContext):
    Content = str(message.text)
    await message.answer('Ваш запрос был принят в очередь. ожидайте.')
    Content = Translete_Prompt(Content)
    add_last_promt_generate_photo(message.chat.id, Content)
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
                    await CFG.bot.send_photo(chat_id=message.chat.id, photo=image_url,caption='Повторить последний запрос',reply_markup=Btn_for_Photo)


############################################
#                   functions              #
############################################


def Translete_Prompt(prompt):
        translator = Translator(from_lang='ru', to_lang='en')
        translated_text = translator.translate(prompt)
        return translated_text

@router.callback_query(F.data == 'BayChatGPT')
async def order(callback:CallbackQuery, bot:CFG.Bot):
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title='Подписка на ChatGPT',
        description='Доступ к ChatGPT',
        payload='BayChatGPT',
        provider_token='381764678:TEST:109578',
        currency='rub',
        prices=[
            LabeledPrice(
                label = 'Подписка на ChatGPT',
                amount=100*100
            )
        ]
    )

@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery) -> None:
    await pre_checkout_q.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: types.Message) -> None:
    Answer = BayGPT(message.chat.id)
    print('Вызвался BayGPT')
    if Answer != None:
        if Answer == True:
            print('Вызвался BayGPT При успешной оплате, который вернул True')
            await message.answer('Готово! Оплата прошла успешно!')