from aiogram.filters import CommandStart,Command
from aiogram.fsm.context import FSMContext
from aiogram import Router,F
from aiogram.types import Message, CallbackQuery,FSInputFile
from aiogram import types
from aiogram.enums.parse_mode import ParseMode
import States as STS 
from keyboards.AdminKeyboards import Work_witch_BD
import Config as CFG

from database.database import get_all_users


router = Router()
@router.message(Command('AdminMenu'))
@router.message(F.text == 'Работа с базой данных')
async def work_with_bd(message:Message):
    if int(message.chat.id) == int(CFG.admin_id):
        await message.answer('Доступ разрешён.',reply_markup=Work_witch_BD)
    else:
        await message.answer('Ошибка: доступ к админ панели запрещен.')
        await message.answer(f'Ваш ID: {message.chat.id} | нужный: {CFG.admin_id}')

@router.message(F.text == 'Все пользователи')
async def get_all_users_handler(message: Message):
    users = get_all_users() 
    msg = []
    for user in users:
        msg.append(f'{user[0]}\n') 
    response_message = ''.join(msg)
    await message.answer(response_message)