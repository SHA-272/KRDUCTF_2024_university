import logging
import sqlite3
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import getenv

TOKEN = getenv("TOKEN")
FLAG = getenv("FLAG")

# Настройки логирования
logging.basicConfig(level=logging.INFO)

# Создаем объекты бота и диспетчера
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

# Настройки для подключения к базе данных SQLite
DB_FILE = "online_store.db"

# Создаем соединение с базой данных
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

# Создаем таблицу пользователей, если её нет
cursor.execute(
    """
	CREATE TABLE IF NOT EXISTS users (
		id INTEGER PRIMARY KEY,
		user_id INTEGER NOT NULL,
		balance INTEGER NOT NULL DEFAULT 0
	)
	"""
)
conn.commit()

# Создаем таблицу товаров, если её нет
cursor.execute(
    """
	CREATE TABLE IF NOT EXISTS products (
		id INTEGER PRIMARY KEY,
		name TEXT NOT NULL,
		price INTEGER NOT NULL,
        file TEXT NOT NULL
	)
	"""
)
conn.commit()

# Создаем таблицу заказов, если её нет
cursor.execute(
    """
	CREATE TABLE IF NOT EXISTS orders (
		id INTEGER PRIMARY KEY,
		user_id INTEGER NOT NULL,
		product_id INTEGER NOT NULL,
		quantity INTEGER NOT NULL,
		FOREIGN KEY(user_id) REFERENCES users(user_id),
		FOREIGN KEY(product_id) REFERENCES products(id)
	)
	"""
)
conn.commit()

# Добавляем тестовые товары для каталога товаров, если их нет
cursor.execute(
    """
	INSERT INTO products (name, price, file) VALUES
		("🍚 Миска рис", 10, "./files/rice.png"),
		("😻 Кошка-жена", 200, "./files/catwife.jpeg"),
        ("📱 Сяоми", 75, "./files/xiaomi.jpg"),
        ("🚩 Великий флаг", 10000000, "./files/flag.png")
	"""
)
conn.commit()


# Начальное сообщение бота
start_message = (
    "Добро пожаловать в наш великий магазин! Это список доступные команды:\n\n"
    "/catalog - Смотреть каталог товар\n"
    "/cart - Смотреть корзина\n"
    "/balance - Смотреть деньга\n"
    "/help - Помогать"
)


# Класс состояний для работы с количеством товара
class Quantity(StatesGroup):
    quantity = State()


# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    cursor.execute(
        "INSERT INTO users (user_id, balance) VALUES (?, ?)",
        (message.from_user.id, 100),
    )
    await message.answer(start_message)


# Обработчик команды /help
@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    await message.answer(start_message)


# Обработчик команды /catalog
@dp.message_handler(commands=["catalog"])
async def cmd_catalog(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    cursor.execute("SELECT id, name, price FROM products")
    products = cursor.fetchall()

    for product in products:
        keyboard.add(
            types.InlineKeyboardButton(
                f"{product[1]} - {product[2]}💷", callback_data=f"get_{product[0]}"
            )
        )

    await message.answer("Выбрать товар:", reply_markup=keyboard)


# Обработчик нажатия на кнопку товара
@dp.callback_query_handler(lambda query: query.data.startswith("get_"), state=None)
async def process_callback_product(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    product_id = int(callback_query.data.split("_")[1])

    cursor.execute("SELECT name, price FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()

    await bot.delete_message(
        callback_query.from_user.id, callback_query.message.message_id
    )
    await bot.send_message(
        callback_query.from_user.id,
        f"Вы выбрать: {product[0]} - {product[1]}💷\n\n" "Ввести сколько товар:",
    )
    await state.update_data(product_id=product_id)
    await Quantity.quantity.set()
    await bot.answer_callback_query(callback_query.id)


# Обработчик ввода количества товара
@dp.message_handler(state=Quantity.quantity)
async def process_product_quantity(message: types.Message, state: FSMContext):
    try:
        quantity = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, ввести число.")
        return

    product_id = (await state.get_data()).get("product_id")
    user_id = message.from_user.id

    cursor.execute(
        "INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)",
        (user_id, product_id, quantity),
    )
    conn.commit()

    await message.answer("Товар добавить в корзина!")
    await state.finish()


# Обработчик команды /cart
@dp.message_handler(commands=["cart"])
async def cmd_cart(message: types.Message):
    user_id = message.from_user.id

    cursor.execute(
        """
		SELECT products.name, products.price, orders.quantity
		FROM orders
		JOIN products ON orders.product_id = products.id
		WHERE orders.user_id=?
		""",
        (user_id,),
    )
    cart_items = cursor.fetchall()

    total_price = sum(item[1] * item[2] for item in cart_items)

    if len(cart_items) == 0:
        await message.answer("Ваш корзина пуст.")
    else:
        cart_text = "Ваш корзина:\n"
        for item in cart_items:
            cart_text += f"{item[0]} - {item[1]}💷 x {item[2]}\n"
        cart_text += f"\Всего сумма: {total_price}💷\n\n"

        inline_keyboard = types.InlineKeyboardMarkup()
        inline_keyboard.add(
            types.InlineKeyboardButton("Купить", callback_data="buy_cart"),
            types.InlineKeyboardButton("Чистить корзина", callback_data="clear_cart"),
        )
        await message.answer(cart_text, reply_markup=inline_keyboard)


# Обработчик кнопки очистки корзины
@dp.callback_query_handler(lambda query: query.data == "clear_cart")
async def process_clear_cart(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    cursor.execute("DELETE FROM orders WHERE user_id=?", (user_id,))
    conn.commit()

    await bot.delete_message(
        callback_query.from_user.id, callback_query.message.message_id
    )
    await bot.answer_callback_query(callback_query.id, "Корзина чисто!")


@dp.callback_query_handler(lambda query: query.data == "buy_cart")
async def process_buy_cart(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    balance = cursor.fetchone()

    cursor.execute(
        """
		SELECT products.name, products.price, orders.quantity, products.file
		FROM orders
		JOIN products ON orders.product_id = products.id
		WHERE orders.user_id=?
		""",
        (user_id,),
    )
    cart_items = cursor.fetchall()

    cart_total = sum(item[1] * item[2] for item in cart_items)

    if balance and cart_total and balance[0] >= cart_total:
        cursor.execute(
            "UPDATE users SET balance = balance - ? WHERE user_id=?",
            (cart_total, user_id),
        )
        conn.commit()

        cursor.execute("DELETE FROM orders WHERE user_id=?", (user_id,))
        conn.commit()

        await bot.delete_message(
            callback_query.from_user.id, callback_query.message.message_id
        )
        await bot.send_message(user_id, "Заказ оплачено! Партия гордится тобой!")
        for item in cart_items:
            file_path = item[3]
            if file_path:
                with open(file_path, "rb") as file:
                    await bot.send_photo(user_id, file, caption=f"{item[0]} x{item[2]}")
        await bot.answer_callback_query(callback_query.id)
    else:
        await bot.send_message(
            user_id,
            "Мало средств для платить заказ! Вы разочаровывать партию!",
        )
        await bot.answer_callback_query(callback_query.id)
    conn.commit()


# Обработчик команды /balance
@dp.message_handler(commands=["balance"])
async def cmd_balance(message: types.Message):
    user_id = message.from_user.id

    cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    balance = cursor.fetchone()

    if balance:
        await message.answer(f"Ваш настоящий деньга: {balance[0]}💷")
    else:
        await message.answer("Нету деньга. Ввести /start")


# Обработчик неизвестной команды
@dp.message_handler()
async def unknown(message: types.Message):
    await message.reply("Извините, я не понимаю.")


# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
