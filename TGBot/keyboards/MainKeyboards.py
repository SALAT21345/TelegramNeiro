from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Start Menu кнопки
btn_gpt = KeyboardButton(text="GPT")
btn_photo = KeyboardButton(text="👤 Генерация фото")
btn_stop_state = KeyboardButton(text='Поменять режим')

#Выбор модели
Btn_Model_Flux = InlineKeyboardButton(text='Flux',callback_data='Flux')
Btn_Model_Anime = InlineKeyboardButton(text='Anime',callback_data='Flux-Anime')



# Создаем клавиатуру
MainReplyKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [btn_gpt],[btn_photo],[btn_stop_state]  # Второй ряд кнопок
    ],
    resize_keyboard=True
)

btn_for_answer_gpt = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Остановить нейросеть❌🤖', callback_data='StopNeiro')],
        [InlineKeyboardButton(text='Сбросить контекст🗑️',callback_data='ClearContext')]
    ]
)
# Select_Image_Model = InlineKeyboardMarkup(
#     inline_keyboard=[
#         Btn_Model_Flux,
#         Btn_Model_Anime
#     ]
# )
