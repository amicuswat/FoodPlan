import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests
from pathlib import PurePath, Path



from foodmanager.models import User, Dish, DishProduct, DishStep, UsedTag

logging.basicConfig (level= logging.INFO)

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
    name = State()
    phone = State()
    main_menu = State()
    personal_cab = State()
    new_recipe = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    use_tg_first_name = types.KeyboardButton("Имя из телеграма")
    markup.add(use_tg_first_name)
    await bot.send_message(message.chat.id,
                     f"Здравствуйте, как вы хотите чтобы к вам обращались? Нажмите на кнопку или введите ваше имя.",
                     reply_markup=markup)
    await reg_states.name.set()
@dp.message_handler(state=reg_states.name)
async def get_name(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    use_tg_phone = types.KeyboardButton("Номер из телеграма", request_contact=True)
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

        # User.objects.create(name=user['name'], phone=user['phone'], telegram_id=message.contact.user_id) Это чтобы сохранить пользователя если ты забудешь

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
        rand_recipe_button = types.KeyboardButton("Любой🍽")
        nongluten_recipe_button = types.KeyboardButton("Безглютеновый🍪")
        vegetarian_recipe_button = types.KeyboardButton("Вегетарианский🥗")
        nonlactose_recipe_button = types.KeyboardButton("Безлактозный🍰")
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

            liked_recipes_button = types.KeyboardButton("Показать любимые❤")
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
    if message.text == "Показать любимые❤":
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
    if message.text == "Любой🍽":
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

        await bot.send_message(message.chat.id,
                                f"{rand_dish.description}"
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

    if message.text == "Безглютеновый🍪":
        nongluten_rand_used_tag = UsedTag.objects.order_by('?').filter(tag=3).first().dish
        nongluten_rand_dish_query = Dish.objects.filter(title=nongluten_rand_used_tag)
        for nongluten_rand_dish in nongluten_rand_dish_query:
            nongluten_dish_ingredients = DishProduct.objects.filter(dish=nongluten_rand_dish)
            nongluten_dish_steps = DishStep.objects.all().filter(dish=nongluten_rand_dish)
            await bot.send_message(message.chat.id,
                                   "Вот ваше безглютеновое блюдо:\n"
                                   f"{nongluten_rand_dish.title}\n",
                                   reply_markup=like_dislike_markup)

            with open(pic_download(nongluten_rand_dish.picture), 'rb') as file:
                await bot.send_photo(message.chat.id,
                                     file)

            await bot.send_message(message.chat.id,
                                   f"{nongluten_rand_dish.description}"
                                   )
            await bot.send_message(message.chat.id,
                                   f"Ингредиенты:")

            for nongluten_dish_ingredient in nongluten_dish_ingredients:
                await bot.send_message(message.chat.id,
                                       f"{nongluten_dish_ingredient.product}{nongluten_dish_ingredient.amount}\n")

            await bot.send_message(message.chat.id,
                                   "Инструкция по приготовлению:")
            for nongluten_dish_step in nongluten_dish_steps:
                if nongluten_dish_step.picture is not None:
                    await bot.send_message(message.chat.id,
                                           f"{nongluten_dish_step.order}. {nongluten_dish_step.description}")
                    with open(pic_download(nongluten_dish_step.picture), 'rb') as file:
                        await bot.send_photo(message.chat.id,
                                             file)
                else:
                    await bot.send_message(message.chat.id,
                                           f"{nongluten_dish_step.order}. {nongluten_dish_step.description}")

    if message.text == "Вегетарианский🥗":
        veg_rand_used_tag = UsedTag.objects.order_by('?').filter(tag=2).first().dish
        veg_rand_dish_query = Dish.objects.filter(title=veg_rand_used_tag)
        for veg_rand_dish in veg_rand_dish_query:
            veg_dish_ingredients = DishProduct.objects.filter(dish=veg_rand_dish)
            veg_dish_steps = DishStep.objects.all().filter(dish=veg_rand_dish)
            await bot.send_message(message.chat.id,
                                   "Вот ваше безглютеновое блюдо:\n"
                                   f"{veg_rand_dish.title}\n",
                                   reply_markup=like_dislike_markup)

            with open(pic_download(veg_rand_dish.picture), 'rb') as file:
                await bot.send_photo(message.chat.id,
                                     file)

            await bot.send_message(message.chat.id,
                                   f"{veg_rand_dish.description}"
                                   )
            await bot.send_message(message.chat.id,
                                   f"Ингредиенты:")

            for veg_dish_ingredient in veg_dish_ingredients:
                await bot.send_message(message.chat.id,
                                       f"{veg_dish_ingredient.product}{veg_dish_ingredient.amount}\n")

            await bot.send_message(message.chat.id,
                                   "Инструкция по приготовлению:")
            for veg_dish_step in veg_dish_steps:
                if veg_dish_step.picture is not None:
                    await bot.send_message(message.chat.id,
                                           f"{veg_dish_step.order}. {veg_dish_step.description}")
                    with open(pic_download(veg_dish_step.picture), 'rb') as file:
                        await bot.send_photo(message.chat.id,
                                             file)
                else:
                    await bot.send_message(message.chat.id,
                                           f"{veg_dish_step.order}. {veg_dish_step.description}")
    if message.text == "Безлактозный🍰":
        nonlactose_rand_used_tag = UsedTag.objects.order_by('?').filter(tag=1).first().dish
        nonlactose_rand_dish_query = Dish.objects.filter(title=nonlactose_rand_used_tag)
        for nonlactose_rand_dish in nonlactose_rand_dish_query:
            nonlactose_dish_ingredients = DishProduct.objects.filter(dish=nonlactose_rand_dish)
            nonlactose_dish_steps = DishStep.objects.all().filter(dish=nonlactose_rand_dish)
            await bot.send_message(message.chat.id,
                                   "Вот ваше безглютеновое блюдо:\n"
                                   f"{nonlactose_rand_dish.title}\n",
                                   reply_markup=like_dislike_markup)

            with open(pic_download(nonlactose_rand_dish.picture), 'rb') as file:
                await bot.send_photo(message.chat.id,
                                     file)

            await bot.send_message(message.chat.id,
                                   f"{nonlactose_rand_dish.description}"
                                   )
            await bot.send_message(message.chat.id,
                                   f"Ингредиенты:")

            for nonlactose_dish_ingredient in nonlactose_dish_ingredients:
                await bot.send_message(message.chat.id,
                                       f"{nonlactose_dish_ingredient.product}{nonlactose_dish_ingredient.amount}\n")

            await bot.send_message(message.chat.id,
                                   "Инструкция по приготовлению:")
            for nonlactose_dish_step in nonlactose_dish_steps:
                if nonlactose_dish_step.picture is not None:
                    await bot.send_message(message.chat.id,
                                           f"{nonlactose_dish_step.order}. {nonlactose_dish_step.description}")
                    with open(pic_download(nonlactose_dish_step.picture), 'rb') as file:
                        await bot.send_photo(message.chat.id,
                                             file)
                else:
                    await bot.send_message(message.chat.id,
                                           f"{nonlactose_dish_step.order}. {nonlactose_dish_step.description}")


def main():
    executor.start_polling(dp)
if __name__ == "__main__":
    main()
