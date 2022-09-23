import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig (level= logging.INFO)

bot = Bot("5656387036:AAHwrd28ThB1YOwM4jHqAom8LgnCgo8svXA")
dp = Dispatcher(bot, storage=MemoryStorage())

class reg_states(StatesGroup):
    name = State()
    phone = State()
    main_menu = State()
    personal_cab = State()
    new_recipe = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    use_tg_first_name = types.KeyboardButton("Использовать ваше имя в телеграме")
    markup.add(use_tg_first_name)
    await bot.send_message(message.chat.id,
                     f"Здравствуйте, как вы хотите чтобы к вам обращались? Нажмите на кнопку или введите ваше имя.",
                     reply_markup=markup)
    await reg_states.name.set()
@dp.message_handler(state=reg_states.name)
async def get_name(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    use_tg_phone = types.KeyboardButton("Использовать номер телефона привязанный к телеграму", request_contact=True)
    markup.add(use_tg_phone)
    if message.chat.type == 'private':
        if message.text == "Использовать ваше имя в телеграме":
            user_name = message.from_user.first_name

        else:
            user_name = message.text
        await state.update_data(name=user_name)
        await bot.send_message(message.chat.id,
                                f"Хорошо, {user_name}, теперь нажмите на кнопку, или введите свой телефон.",
                                reply_markup=markup)
        await reg_states.phone.set()

@dp.message_handler(state=reg_states.phone, content_types= types.ContentTypes.CONTACT)
async def get_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as user:
        if message.chat.type == 'private':
            if message.contact is not None:
                user['phone'] = message.contact.phone_number
            else:
                user['phone'] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        go_to_main_menu = types.KeyboardButton("Главное меню📚")
        markup.add(go_to_main_menu)
        await bot.send_message(message.chat.id,
                                   f"Вы завершили регистрацию.\n"
                                   f"Ваше имя: {user['name']}\n"
                                   f"Ваш номер телефона:{user['phone']}",
                               reply_markup=markup)


        await reg_states.main_menu.set()


@dp.message_handler(state=reg_states.main_menu)
async def main_menu(message: types.Message, state: FSMContext):
    main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    new_recipe_button = types.KeyboardButton("Новый рецептик😋")
    pers_cab_button = types.KeyboardButton("Личный кабинет👤")
    main_menu_markup.add(new_recipe_button, pers_cab_button)
    if message.text == "Главное меню📚":
        await bot.send_message(message.chat.id,
                            f"Чем вы хотите полакомиться? Что-то новое, или вами уже знакомое?",
                            reply_markup=main_menu_markup)
    if message.text == "Новый рецептик😋":
        new_recipe_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        rand_recipe_button = types.KeyboardButton("Любой рецептик🍽")
        nongluten_recipe_button = types.KeyboardButton("Безглютеновый рецептик🍪")
        vegetarian_recipe_button = types.KeyboardButton("Вегетарианский рецептик🥗")
        nonlactose_recipe_button = types.KeyboardButton("Безлактозный рецептик🍰")
        go_to_main_menu = types.KeyboardButton("Главное меню📚")
        new_recipe_markup.add(vegetarian_recipe_button, nongluten_recipe_button,
                              nonlactose_recipe_button, rand_recipe_button, go_to_main_menu)
        await bot.send_message(message.chat.id,
                               f"Выберите категорию",
                               reply_markup=new_recipe_markup)
        await reg_states.new_recipe.set()
    if message.text == "Личный кабинет👤":
        async with state.proxy() as user:
            pers_cab_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            liked_recipes_button = types.KeyboardButton("Показать любимые рецептики❤")
            go_to_main_menu = types.KeyboardButton("Главное меню📚")
            pers_cab_markup.add(liked_recipes_button, go_to_main_menu)
            await bot.send_message(message.chat.id,
                                   "Добро пожаловать в ваш личный кабинет.\n"
                                   f"Ваше имя {user['name']}\n"
                                   f"Ваш номер телефона {user['phone']}",
                                   reply_markup=pers_cab_markup)
        await reg_states.personal_cab.set()

@dp.message_handler(state=reg_states.personal_cab)
async def pers_cab(message: types.Message):
    if message.text == "Главное меню📚":
        main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        new_recipe_button = types.KeyboardButton("Новый рецептик😋")
        pers_cab_button = types.KeyboardButton("Личный кабинет👤")
        main_menu_markup.add(new_recipe_button, pers_cab_button)
        await bot.send_message(message.chat.id,
                            f"Чем вы хотите полакомиться? Что-то новое, или вами уже знакомое?",
                            reply_markup=main_menu_markup)
        await reg_states.main_menu.set()
    if message.text == "Показать любимые рецептики❤":
        liked_recipes_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        go_forward = types.KeyboardButton("Вперёд➡️")
        go_back = types.KeyboardButton("⬅️Назад")
        go_to_main_menu = types.KeyboardButton("Главное меню📚")
        liked_recipes_markup.add(go_back, go_forward, go_to_main_menu)
        await bot.send_message(message.chat.id,
                         "Вот ваши любимые рецептики:",
                               reply_markup=liked_recipes_markup)

@dp.message_handler(state=reg_states.new_recipe)
async def new_recipe(message: types.Message):
    if message.text == "Главное меню📚":
        main_menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        new_recipe_button = types.KeyboardButton("Новый рецептик😋")
        pers_cab_button = types.KeyboardButton("Личный кабинет👤")
        main_menu_markup.add(new_recipe_button, pers_cab_button)
        await bot.send_message(message.chat.id,
                            f"Чем вы хотите полакомиться? Что-то новое, или вами уже знакомое?",
                            reply_markup=main_menu_markup)
        await reg_states.main_menu.set()
    like_dislike_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    like_button = types.KeyboardButton("Сохранить❤")
    dislike_button = types.KeyboardButton("Больше не показывать👎")
    go_to_main_menu = types.KeyboardButton("Главное меню📚")
    like_dislike_markup.add(like_button, dislike_button, go_to_main_menu)
    if message.text == "Любой рецептик🍽":
        await bot.send_message(message.chat.id,
                               "Вот ваше блюдо:",
                               reply_markup=like_dislike_markup)

    if message.text == "Безглютеновый рецептик🍪":
        await bot.send_message(message.chat.id,
                               "Вот ваше безглютеновое блюдо:",
                               reply_markup=like_dislike_markup)
    if message.text == "Вегетарианский рецептик🥗":
        await bot.send_message(message.chat.id,
                               "Вот ваше вегетарианское блюдо:",
                               reply_markup=like_dislike_markup)
    if message.text == "Безлактозный рецептик🍰":
        await bot.send_message(message.chat.id,
                               "Вот ваше безлактозное блюдо:",
                               reply_markup=like_dislike_markup)

if __name__ == "__main__":
    executor.start_polling(dp)
