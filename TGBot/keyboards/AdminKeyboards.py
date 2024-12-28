from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_admin_panel = KeyboardButton(text='Работа с базой данных')

btn_all_users = KeyboardButton(text='Все пользователи')

main_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [btn_admin_panel]
    ],
    resize_keyboard=True
)

Work_witch_BD = ReplyKeyboardMarkup(
    keyboard=[
        [btn_all_users]
    ],
    resize_keyboard= True
)