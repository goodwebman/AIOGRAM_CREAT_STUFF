from dotenv import load_dotenv # для скрытия токена
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove # клавиатура
import os # для извлечения токена из .env файла
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup # для голосования
from aiogram.types import Poll, PollOption # для создания опросника


load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)


async def on_startup(_):
    print('Бот был успешно запущен!')

@dp.message_handler(commands=['start'])
async def help_command(message: types.Message):
    await message.answer(text="Добро пожаловать в наш телеграмм бот!",
                         reply_markup=kb)
    await message.delete()



HELP_COMMAND = '''
/help - список команд
/start - начать работу с ботом
/location - локация
/picture - картинка
/vote - оценка
/pool - голосование 
'''

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND,
                        reply_markup=kb)


DISCRIPTION = 'Данный бот предназначен для рофла йоу'

@dp.message_handler(commands=['description'])
async def help_command(message: types.Message):
    await message.answer(text=DISCRIPTION,
                        reply_markup=kb)


@dp.message_handler(commands=['picture'])
async def send_img(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo='https://static.kinoafisha.info/k/news/610/upload/news/518836787230.jpg')
    await message.delete()

@dp.message_handler(commands=['location'])
async def set_point(message: types.Message):
    await bot.send_location(chat_id=message.from_user.id,
                            latitude=55,
                            longitude=74)
    await message.delete()

# Клавиатура

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add('Помощь').add('Описание бота').add('Скинь мне Джимми').add('бля, где я?')



# Чтобы работала клавиатура


@dp.message_handler(text='бля, где я?')
async def set_point(message: types.Message):
    await bot.send_location(chat_id=message.from_user.id,
                            latitude=55,
                            longitude=74)
    await message.delete()

@dp.message_handler(text='Описание бота')
async def help_command(message: types.Message):
    await message.answer(text=DISCRIPTION,
                        reply_markup=kb)

@dp.message_handler(text='Скинь мне Джимми')
async def send_img(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo='https://static.kinoafisha.info/k/news/610/upload/news/518836787230.jpg')
    await message.delete()

@dp.message_handler(text='Помощь')
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND,
                        reply_markup=kb)



# @dp.message_handler(commands=['id'])
# async def id(message: types.Message): # Узнать id юзера
#     await message.answer(f'{message.from_user.id}')

# @dp.message_handler(content_types=['document', 'photo'])
# async def forward_message(message: types.Message):       # - команда чтобы пересылать что то в группы
#     await bot.forward_message(os.getenv('GROUP_ID'), message.from_user.id, message.message_id)


# @dp.message_handler(content_types=['sticker'])
# async def check_sticket(message: types.Message):
    # await message.answer(message.sticker.file_id) - команда чтоб узнать id стикера
    # await bot.send_message(message.from_user.id, message.chat.id) - команда чтобы узнать id группы


# Инлайн клавиатура


ikb = InlineKeyboardMarkup(row_width=2)

ib1 = InlineKeyboardButton(text='Button-1',
                            url='https://github.com/goodwebman')

ib2 = InlineKeyboardButton(text='Button-2',
                            url='https://github.com/goodwebman')

ikb.add(ib1, ib2)

@dp.message_handler(commands=['keyboard'])
async def help_command(message: types.Message):
    await message.answer(text="Добро пожаловать в наш телеграмм бот!",
                         reply_markup=ikb)
    await message.delete()


@dp.message_handler(commands=['vote']) # handler example
async def vote_command(message: types.Message):
    ikb = InlineKeyboardMarkup(row_width=2)
    ib1 = InlineKeyboardButton(text='❤️',
                               callback_data="like")
    ib2 = InlineKeyboardButton(text='👎',
                               callback_data="dislike")
    ikb.add(ib1, ib2)

    await bot.send_photo(chat_id=message.from_user.id,
                         photo="https://cdn.mos.cms.futurecdn.net/xs77NtybWu6MPkoRtYApuJ-320-80.jpg",
                         caption='Нравится ли тебе данная фотография?',
                         reply_markup=ikb)

@dp.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery):
    if callback.data == 'like':
        await callback.answer(text='Тебе понравилась данная фотография!')
    await callback.answer('Тебе не понравилась данная фотография!')

# Голосование

@dp.message_handler(commands=["pool"])
async def cmd_pool(message: types.Message):
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(types.KeyboardButton(text="Создать викторину",
                                           request_poll=types.KeyboardButtonPollType(type=types.PollType.REGULAR)))
    poll_keyboard.add(types.KeyboardButton(text="Отмена"))
    await message.answer("Нажмите на кнопку ниже и создайте викторину!", reply_markup=poll_keyboard)

# handler на текстовое сообщение с текстом “Отмена”
@dp.message_handler(lambda message: message.text == "Отмена")
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Действие отменено. Введите /pool, чтобы начать заново.", reply_markup=remove_keyboard)


# Фильтр матов

from aiogram.dispatcher.filters import Text
import re

# Создаем регулярное выражение для поиска матов
bad_words_pattern = re.compile(r"\b(хуй|пизда|ебать|блять)\b", re.IGNORECASE)
# Создаем фильтр матов
async def bad_words_filter(message: types.Message):
    if bad_words_pattern.search(message.text):
        # Если в сообщении есть мат, то отбрасываем его
        return True
    else:
        # Иначе, передаем сообщение дальше
        return False
# Декорируем хэндлер фильтром матов
@dp.message_handler(Text, bad_words_filter)
async def handle_message(message: types.Message):
    await message.answer("Вы использовали ненормативную лексику. Пожалуйста, не используйте ее в дальнейшем.")
    await message.delete()



if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)