from aiogram import Bot, Dispatcher, types
import asyncio
from random import randint
import importlib
import os

from aiogram.types import InputMediaPhoto

Token = "7548762812:AAF1EwLTg7m4KF_5tUf9LS0RBzY95PgGZRw"
chenal_name = "@project_oneone"
bot = Bot(token = Token)
dp = Dispatcher()
user_data = {}
project_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(project_dir, "images")

basket_list = []
@dp.message()
async def message_handler(message: types.Message):
    user_id = message.from_user.id
    if message.text == "/start":
        await welcome(message)
    elif "language" not in user_data[user_id]:
        await check_lang(message)
    elif "phone" not in user_data[user_id]:
        await check_phone(message)
    elif "status" not in user_data[user_id]:
        await check_sms(message)
    elif 'state' not in user_data[user_id]:
        await choice_menu(message)
    elif "none" in user_data[user_id]['state']:
        await show_menu(message)
    elif 'categories' in user_data[user_id]['state']:
        await show_category(message)
    elif 'items' in user_data[user_id]['state']:
        await show_items(message)
    elif 'item' in user_data[user_id]['state']:
        await preview_items(message)
    elif 'basket' in user_data[user_id]:
        await basket_order(message)

async def welcome(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    button = [
        [types.KeyboardButton(text="Русский 🇷🇺"),
        types.KeyboardButton(text="English 🇺🇸"),
        types.KeyboardButton(text="Ўзбекча 🇺🇿")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(f"Здравствуйте! Добро пожаловать в наш бот! \n"
                         f"Давайте для начала выберем язык обслуживания!", reply_markup=keyboard)

def select_lang(lang):
    if lang == 'Русский 🇷🇺':
        lang = 'ru'
    elif lang == 'English 🇺🇸':
        lang = 'eng'
    elif lang == 'Ўзбекча 🇺🇿':
        lang = 'uz'
    else:
        lang = 'uz'
    return lang

async def check_lang(message: types.Message):
    user_id = message.from_user.id
    lang = message.text
    lang = select_lang(lang)
    user_data[user_id]["language"] = lang
    lang = importlib.import_module(f'lang.{lang}')
    button = [
        [types.KeyboardButton(text= lang.phone_button_text, request_contact=True)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(f"{lang.phone_text}", reply_markup=keyboard)

async def check_phone(message: types.Message):
    user_id = message.from_user.id

    if message.contact is not None:
        phone = message.contact.phone_number
    else:
       phone = message.text
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    user_data[user_id]['phone'] = phone
    sms = randint(100000,999999)
    user_data[user_id]['code'] = sms
    await message.answer(f'{sms},{lang.sms_text}')

async def check_sms(message: types.Message):
    user_id = message.from_user.id
    code = message.text
    code_true = user_data[user_id]['code']
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')

    if code == str(code_true):
        user_data[user_id]['status'] = 'verified'
        await first_menu(message)
    else:
        await message.answer(f'{lang.text_error_sms}')

async def first_menu(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    button = [
        [types.KeyboardButton(text=lang.text_order)],
        [types.KeyboardButton(text=lang.text_setting),
         types.KeyboardButton(text=lang.text_about)],
        [types.KeyboardButton(text=lang.text_my_orders),
         types.KeyboardButton(text=lang.text_feedback)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(f'{lang.text_first_menu}', reply_markup=keyboard)

    global menu
    menu = {
        lang.text_burgers:{
            lang.text_cheeseburger:{'price':22000,'image':'cheeseburger.jpg'},
            lang.text_chicken_burger:{'price':29000,'image':'chicken_burger.jpg'},
            lang.text_hamburger:{'price':31000,'image':'hamburger.jpg'}
        },
        lang.text_salads:{
            lang.text_coul_slow:{'price':6000,'image':'coul_slow.jpg'},
            lang.text_loook:{'price':16000,'image':'loook.png'},
            lang.text_bun:{'price':3000,'image':'bun.jpg'}
        },
        lang.text_drinks:{
            lang.text_ice_tea:{'price':15000,'image':'ice_tea.jpg'},
            lang.text_ice_capuchino:{'price':12000,'image':'ice_capuchino.png'},
            lang.text_tea_lemon:{'price':8000,'image':'tea_lemon.png'}
        }
    }
async def choice_menu(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    user_data[user_id]['state'] = 'none'
    if message.text == lang.text_order:
        button = [
            [types.KeyboardButton(text=lang.text_delivery),
             types.KeyboardButton(text=lang.text_self_pickup)],
            [types.KeyboardButton(text=lang.text_back)]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
        await message.answer(f'{lang.text_choice}',reply_markup=keyboard)


async def show_menu(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]['state'] = 'categories'
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    if message.text == lang.text_back:
        del user_data[user_id]['state']
        await first_menu(message)
    else:
        user_data[user_id]['type_delivery'] = message.text
        await show_category(message)
    print(1,user_data)

    print("HIII <3")
    print("HIII <3")
    print("HIII <3")
    print("HIII <3")
    print("how are you?")
    print("love, bae")