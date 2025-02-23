from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Start Menu кнопки
# ================== MainReplyKeyboard ===================== #
btn_gpt = KeyboardButton(text="GPT")
btn_photo = KeyboardButton(text="👤 Генерация фото")
btn_stop_state = KeyboardButton(text='Поменять режим')

MainReplyKeyboard = ReplyKeyboardMarkup(
    keyboard=[
        [btn_gpt],[btn_photo],[btn_stop_state]  
    ],
    resize_keyboard=True
)

#Выбор модели
Btn_Model_Flux = InlineKeyboardButton(text='Flux',callback_data='Flux')
Btn_Model_Anime = InlineKeyboardButton(text='Anime',callback_data='Flux-Anime')

#Подписки

# ================== btn_BayChatGPT_StartMenu ===================== #
_btn_BayChatGPT_StartMenu = InlineKeyboardButton(text='Приобрести подписку', callback_data='Bay_ChatGPT_start_menu')
_MyAccount = InlineKeyboardButton(text='Мой Аккаунт📱',callback_data='MyAccount')

btn_BayChatGPT_StartMenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [_btn_BayChatGPT_StartMenu]
    ],
)

_btn_BayChatGPT_300 = InlineKeyboardButton(text='ChatGPT + 300 Tokens',callback_data='BayChatGPT_300')
_btn_BayChatGPT_Tokens_ = InlineKeyboardButton(text='1000 Tokens',callback_data='BayTokens_1000')

_btn_BayChatGPT = InlineKeyboardButton(text='ChatGPT',callback_data='BayChatGPT')
_btn_BayChatGPT_100 = InlineKeyboardButton(text='ChatGPT + 100 Tokens',callback_data='BayChatGPT_100')

_btn_BayChatGPT_Tokens_10 = InlineKeyboardButton(text='10 Tokens',callback_data='BayChatGPT_Tokens_10')
_btn_BayChatGPT_Tokens_25 = InlineKeyboardButton(text='25 Tokens',callback_data='BayChatGPT_Tokens_25')
_btn_BayChatGPT_Tokens_50 = InlineKeyboardButton(text='50 Tokens',callback_data='BayChatGPT_Tokens_50')
_btn_BayChatGPT_Tokens_100 = InlineKeyboardButton(text='100 Tokens',callback_data='BayChatGPT_Tokens_100')

Btn_BayTokensOrChatGPT_Menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [_btn_BayChatGPT_300],
        [_btn_BayChatGPT_Tokens_],
        [_btn_BayChatGPT], 
        [_btn_BayChatGPT_100],
        [_btn_BayChatGPT_Tokens_10,_btn_BayChatGPT_Tokens_25],
        [_btn_BayChatGPT_Tokens_50,_btn_BayChatGPT_Tokens_100]

    ]
)

# ================== btn_BayPhoto_StartMenu ===================== #



Btn_BayTokensOrChatGPT_Menu = InlineKeyboardMarkup(
    inline_keyboard=[]
)
# ================== Btn_My_Account ===================== #
Btn_My_Account = InlineKeyboardMarkup(
    inline_keyboard=[
        [_MyAccount]
    ],
)

_btnSelectSub_GPT = InlineKeyboardButton(text='ChatGPT',callback_data='Bay_ChatGPT_start_menu')
_btnSelectSub_Photo = InlineKeyboardButton(text='Генерация Фото',callback_data='Bay_Photo_start_menu')

btnSelectSub = InlineKeyboardMarkup(inline_keyboard=[
    [_btnSelectSub_GPT],[_btnSelectSub_Photo]
],)




#работа с генерацией фото.
btn_Again_prompt = InlineKeyboardButton(text='Повторить запрос', callback_data='AgainPrompt')

Btn_for_Photo = InlineKeyboardMarkup(
    inline_keyboard=[
        [btn_Again_prompt]
    ]
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
