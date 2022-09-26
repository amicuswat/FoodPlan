import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests
from pathlib import PurePath, Path

import asyncio

from foodmanager.models import User, Dish, DishProduct, DishStep, UsedTag, UserDish

logging.basicConfig(level=logging.INFO)

bot = Bot("5656387036:AAHwrd28ThB1YOwM4jHqAom8LgnCgo8svXA")
dp = Dispatcher(bot, storage=MemoryStorage())


def pic_download(url):
    url = f"http:{url}"
    response = requests.get(url)
    response.raise_for_status()
    filename = "dish_pic.jpg"
    Path("images/").mkdir(parents=True, exist_ok=True)
    path = PurePath("images", filename)
    with open(path, 'wb') as file:
        file.write(response.content)
    return path


class reg_states(StatesGroup):
    self_data = State()
    name = State()
    phone = State()
    main_menu = State()
    personal_cab = State()
    new_recipe = State()
    like_dislike = State()
    rand_new_recipe = State()



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not User.objects.filter(telegram_id=message.from_user.id).first():
        global self_data_markup
        self_data_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        yes_button = types.KeyboardButton("Соглашаюсь")
        no_button = types.KeyboardButton("Не соглашаюсь")
        self_data_markup.add(yes_button, no_button)
        await bot.send_message(message.chat.id,
                                f"Здравствуйте, вы даёте соглашение на обработку персональных данных?",
                               reply_markup=self_data_markup)
        await reg_states.self_data.set()

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        new_recipe_button = types.KeyboardButton("Новый рецептик😋")
        pers_cab_button = types.KeyboardButton("Личный кабинет👤")
        markup.add(new_recipe_button, pers_cab_button)
        await bot.send_message(message.chat.id,
                               f"Чем вы хотите полакомиться? Что-то новое, или вами уже знакомое?",
                               reply_markup=markup)
        await reg_states.main_menu.set()


@dp.message_handler(state=reg_states.self_data)
async def get_permission(message: types.Message):
    if message.text == "Соглашаюсь":
        name_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        use_tg_first_name = types.KeyboardButton("Имя из телеграма")
        name_markup.add(use_tg_first_name)
        await bot.send_message(message.chat.id,
                           "Как вы хотите чтобы к вам обращались? Нажмите на кнопку или введите ваше имя.",
                           reply_markup=name_markup)
        await reg_states.name.set()
    if message.text == "Не соглашаюсь":
        await bot.send_message(message.chat.id,
                               "Для продолжения вы должны дать согласие.",
                               reply_markup=self_data_markup)


@dp.message_handler(state=reg_states.name)
async def get_name(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    use_tg_phone = types.KeyboardButton("Номер из телеграма", request_contact=True)
    markup.add(use_tg_phone)
    if message.chat.type == 'private':
        if message.text == "Имя из телеграма":
            user_name = message.from_user.first_name
        else:
            user_name = message.text
        await state.update_data(name=user_name)
        await bot.send_message(message.chat.id,
                               f"Хорошо, {user_name}, теперь нажмите на кнопку, или введите свой телефон.",
                               reply_markup=markup)
        await reg_states.phone.set()


@dp.message_handler(state=reg_states.phone, content_types=types.ContentTypes.CONTACT)
async def get_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as user:
        if message.chat.type == 'private':
            if message.contact is not None:
                user['phone'] = message.contact.phone_number
            else:
                user['phone'] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        new_recipe_button = types.KeyboardButton("Новый рецептик😋")
        pers_cab_button = types.KeyboardButton("Личный кабинет👤")
        markup.add(new_recipe_button, pers_cab_button)
        await bot.send_message(message.chat.id,
                               f"Вы завершили регистрацию.\n"
                               f"Ваше имя: {user['name']}\n"
                               f"Ваш номер телефона:{user['phone']}")
        await bot.send_message(message.chat.id,
                               f"Чем вы хотите полакомиться? Что-то новое, или вами уже знакомое?",
                               reply_markup=markup)
        User.objects.create(name=user['name'], phone=user['phone'], telegram_id=message.from_user.id)
        await reg_states.main_menu.set()


@dp.message_handler(state=reg_states.main_menu)
async def main_menu(message: types.Message):
    global main_menu_markup
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
        rand_recipe_button = types.KeyboardButton("Любой🍽")
        nongluten_recipe_button = types.KeyboardButton("Безглютеновый🍪")
        vegetarian_recipe_button = types.KeyboardButton("Вегетарианский🥗")
        nonlactose_recipe_button = types.KeyboardButton("Безлактозный🍰")
        go_to_main_menu = types.KeyboardButton("Главное меню📚")
        new_recipe_markup.add(vegetarian_recipe_button, nongluten_recipe_button,
                              nonlactose_recipe_button).row(rand_recipe_button).row(go_to_main_menu)
        await bot.send_message(message.chat.id,
                               f"Выберите категорию",
                               reply_markup=new_recipe_markup)
        await reg_states.new_recipe.set()
    if message.text == "Личный кабинет👤":
        pers_cab_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        liked_recipes_button = types.KeyboardButton("Показать любимые❤")
        go_to_main_menu = types.KeyboardButton("Главное меню📚")
        pers_cab_markup.add(liked_recipes_button, go_to_main_menu)
        user = User.objects.get(telegram_id=message.from_user.id)
        await bot.send_message(message.chat.id,
                               "Добро пожаловать в ваш личный кабинет.\n"
                               f"Ваше имя {user.name}\n"
                               f"Ваш номер телефона {user.phone}",
                               reply_markup=pers_cab_markup)
        await reg_states.personal_cab.set()


@dp.message_handler(state=reg_states.personal_cab)
@dp.message_handler(state=reg_states.personal_cab)
async def pers_cab(message: types.Message):
    global current_dish
    if message.text == "Главное меню📚":
        await bot.send_message(message.chat.id,
                               f"Чем вы хотите полакомиться? Что-то новое, или вами уже знакомое?",
                               reply_markup=main_menu_markup)
        await reg_states.main_menu.set()
    if message.text == "Показать любимые❤":
        liked_recipes_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        go_forward = types.KeyboardButton("Вперёд➡️")
        go_back = types.KeyboardButton("⬅️Назад")
        go_to_main_menu = types.KeyboardButton("Главное меню📚")
        liked_recipes_markup.row(go_back, go_forward).add(go_to_main_menu)
        await bot.send_message(message.chat.id,
                               "Вот ваши любимые рецептики:",
                               reply_markup=liked_recipes_markup)
        user = User.objects.get(telegram_id=message.from_user.id)
        user_dishes = UserDish.objects.filter(user=user, liked=True)
        current_dish = 0
        await show_user_recipe(message, current_dish, user_dishes)
    if message.text == "Вперёд➡️":
        try:
            user = User.objects.get(telegram_id=message.from_user.id)
            user_dishes = UserDish.objects.filter(user=user)
            current_dish += 1
            await show_user_recipe(message, current_dish, user_dishes)
        except IndexError:
            current_dish -= 1
            await bot.send_message(message.chat.id,
                                   "Это было последнее сохранённое вами блюдо")
    if message.text == "⬅️Назад":
        user = User.objects.get(telegram_id=message.from_user.id)
        user_dishes = UserDish.objects.filter(user=user)
        current_dish -= 1
        try:
            await show_user_recipe(message, current_dish, user_dishes)
        except AssertionError:
            current_dish += 1
            await bot.send_message(message.chat.id,
                                   "Это первое сохранённое вами блюдо")


@dp.message_handler(state=reg_states.new_recipe)
async def new_recipe(message: types.Message):
    if message.text == "Главное меню📚":
        await bot.send_message(message.chat.id,
                               f"Чем вы хотите полакомиться? Что-то новое, или вами уже знакомое?",
                               reply_markup=main_menu_markup)
        await reg_states.main_menu.set()
    global like_dislike_markup
    like_dislike_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    like_button = types.KeyboardButton("Сохранить❤")
    dislike_button = types.KeyboardButton("Больше не показывать👎")
    go_to_main_menu = types.KeyboardButton("Главное меню📚")
    like_dislike_markup.row(like_button, dislike_button).add(go_to_main_menu)
    if message.text == "Любой🍽":
        global rand_dish
        rand_dish = Dish.objects.order_by('?').first()
        user_dish = UserDish.objects.filter(dish=rand_dish, user=message.from_user.id, disliked=True).first()
        if user_dish is not None:
            rand_dish = Dish.objects.order_by('?').first()
        dish_ingredients = DishProduct.objects.filter(dish=rand_dish)
        dish_steps = DishStep.objects.all().filter(dish=rand_dish)
        await bot.send_message(message.chat.id,
                               f"Вот ваше блюдо:\n"
                               f"{rand_dish.title}\n",
                               reply_markup=like_dislike_markup)
        with open(pic_download(rand_dish.picture), 'rb') as file:
            await bot.send_photo(message.chat.id,
                                 file)
        if rand_dish.description is not None:
            await bot.send_message(message.chat.id,
                                f"{rand_dish.description}")

        await bot.send_message(message.chat.id,
                               f"Ингредиенты:")

        for dish_ingredient in dish_ingredients:
            await bot.send_message(message.chat.id,
                                   f"{dish_ingredient.product}{dish_ingredient.amount}\n")

        await bot.send_message(message.chat.id,
                               "Инструкция по приготовлению:")
        for dish_step in dish_steps:
            if dish_step.picture:
                await bot.send_message(message.chat.id,
                                       f"{dish_step.order}. {dish_step.description}")
                with open(pic_download(dish_step.picture), 'rb') as file:
                    await bot.send_photo(message.chat.id,
                                         file)
            else:
                await bot.send_message(message.chat.id,
                                       f"{dish_step.order}. {dish_step.description}")
        await reg_states.rand_new_recipe.set()

    if message.text == "Безглютеновый🍪":
        tag = 3
        await show_recipe(message, tag)

    if message.text == "Вегетарианский🥗":
        tag = 2
        await show_recipe(message, tag)

    if message.text == "Безлактозный🍰":
        tag = 1
        await show_recipe(message, tag)


@dp.message_handler(state=reg_states.rand_new_recipe)
async def like_dislike(message: types.Message):
    if message.text == "Сохранить❤":
        like(message.from_user.id, rand_dish)
        await bot.send_message(message.chat.id,
                               "Блюдо успешно сохранено")
        await bot.send_message(message.chat.id,
                               f"Чем вы хотите полакомиться? Что-то новое, или вами уже знакомое?",
                               reply_markup=main_menu_markup)
        await reg_states.main_menu.set()
    if message.text == "Больше не показывать👎":
        dislike(message.from_user.id, rand_dish)
        await bot.send_message(message.chat.id,
                               "Блюдо больше не будет показываться")
        await bot.send_message(message.chat.id,
                               f"Чем вы хотите полакомиться? Что-то новое, или вами уже знакомое?",
                               reply_markup=main_menu_markup)
        await reg_states.main_menu.set()
    if message.text == "Главное меню📚":
        await bot.send_message(message.chat.id,
                               f"Чем вы хотите полакомиться? Что-то новое, или вами уже знакомое?",
                               reply_markup=main_menu_markup)
        await reg_states.main_menu.set()


async def show_recipe(message, tag):
    rand_used_tag = UsedTag.objects.order_by('?').filter(tag=tag).first().dish
    global rand_dish
    rand_dish = Dish.objects.get(title=rand_used_tag)
    user_dish = UserDish.objects.filter(dish=rand_dish, user=message.from_user.id, disliked=True).first()
    if user_dish is not None:
        rand_used_tag = UsedTag.objects.order_by('?').filter(tag=tag).first().dish
        rand_dish = Dish.objects.get(title=rand_used_tag)

    rand_dish_ingredients = DishProduct.objects.filter(dish=rand_dish)
    rand_dish_steps = DishStep.objects.all().filter(dish=rand_dish)
    await bot.send_message(message.chat.id,
                           "Вот ваше блюдо:\n"
                           f"{rand_dish.title}\n",
                           reply_markup=like_dislike_markup)

    with open(pic_download(rand_dish.picture), 'rb') as file:
        await bot.send_photo(message.chat.id,
                             file)
    if rand_dish.description is not None:
        await bot.send_message(message.chat.id,
                               f"{rand_dish.description}")

    await bot.send_message(message.chat.id,
                           f"Ингредиенты:")

    for rand_dish_ingredient in rand_dish_ingredients:
        await bot.send_message(message.chat.id,
                               f"{rand_dish_ingredient.product}{rand_dish_ingredient.amount}\n")

    await bot.send_message(message.chat.id,
                           "Инструкция по приготовлению:")
    for rand_dish_step in rand_dish_steps:
        if rand_dish_step.picture is not None:
            await bot.send_message(message.chat.id,
                                   f"{rand_dish_step.order}. {rand_dish_step.description}")
            with open(pic_download(rand_dish_step.picture), 'rb') as file:
                await bot.send_photo(message.chat.id,
                                     file)
        else:
            await bot.send_message(message.chat.id,
                                   f"{rand_dish_step.order}. {rand_dish_step.description}")
    await reg_states.rand_new_recipe.set()


async def show_user_recipe(message, current_dish, user_dishes):
    user_dish = Dish.objects.get(userdish=user_dishes[current_dish])
    dish_ingredients = DishProduct.objects.filter(dish=user_dish)
    dish_steps = DishStep.objects.all().filter(dish=user_dish)
    await bot.send_message(message.chat.id,
                           f"Вот ваше блюдо:\n"
                           f"{user_dish.title}\n")
    with open(pic_download(user_dish.picture), 'rb') as file:
        await bot.send_photo(message.chat.id,
                             file)

    await bot.send_message(message.chat.id,
                           f"{user_dish.description}"
                           )
    await bot.send_message(message.chat.id,
                           f"Ингредиенты:")

    for dish_ingredient in dish_ingredients:
        await bot.send_message(message.chat.id,
                               f"{dish_ingredient.product}{dish_ingredient.amount}\n")

    await bot.send_message(message.chat.id,
                           "Инструкция по приготовлению:")
    for dish_step in dish_steps:
        if dish_step.picture:
            await bot.send_message(message.chat.id,
                                   f"{dish_step.order}. {dish_step.description}")
            with open(pic_download(dish_step.picture), 'rb') as file:
                await bot.send_photo(message.chat.id,
                                     file)
        else:
            await bot.send_message(message.chat.id,
                                   f"{dish_step.order}. {dish_step.description}")


def like(user_telegram, dish):
    user = User.objects.get(telegram_id=user_telegram)
    UserDish.objects.create(dish=dish, user=user, liked=True)


def dislike(user_telegram, dish):
    user = User.objects.get(telegram_id=user_telegram)
    UserDish.objects.create(dish=dish, user=user, disliked=True)


def is_dish_disliked(user_telegram, dish):
    user = User.objects.get(telegram_id=user_telegram)
    UserDish.objects.get(user=user, dish=dish, disliked=True)


def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


def main():
    print("Бот Запущен")
    loop = get_or_create_eventloop()
    executor.start_polling(dp, loop=loop)


if __name__ == "__main__":
    main()
