from config import token
from check import check
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token)
dp = Dispatcher(bot)

start_text = '''<em>Здравствуй, этот бот предназначен для автоматической проверки теста по электронике и 
схемотехнике</em>'''

advice_text = ('<em>Отправь нам фото решенного теста,\nНа фото не должно попадать лишних деталей,'
               ' следует делать снимок только содержимого листа с тестом, без краев листа, также фото должно'
               ' быть сделано в хорошем качестве и при хорошем освещении</em>')

start_markup = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton('Начать', callback_data='старт')
start_markup.add(button1)


@dp.message_handler(commands=['start'])
async def hello(message: types.Message):
    await bot.send_message(message.chat.id, start_text, parse_mode='HTML', reply_markup=start_markup)


@dp.message_handler(content_types='photo')
async def face(message: types.Message):
    await message.photo[-1].download(destination_file='img.jpg')
    result, photo_name = check('img.jpg')
    if len(result) == 19:
        balls = 0
        answer = 'Результат теста:\n'

        # Проверка первого вопроса
        if result[:3] == [1, 0, 0]:
            answer += '1. Верно\n'
            balls += 1
        else:
            answer += '1. Не верно\n'

        # Проверка второго вопроса
        if result[3:7] == [0, 0, 1, 0]:
            answer += '2. Верно\n'
            balls += 1
        else:
            answer += '2. Не верно\n'

        # Проверка третьего вопроса
        if result[7:11] == [0, 0, 1, 0]:
            answer += '3. Верно\n'
            balls += 1
        else:
            answer += '3. Не верно\n'

        # Проверка четвертого вопроса
        if result[11:15] == [0, 1, 0, 0]:
            answer += '4. Верно\n'
            balls += 1
        else:
            answer += '4. Не верно\n'

        # Проверка пятого вопроса
        if result[15:] == [0, 1, 0, 0]:
            answer += '5. Верно\n'
            balls += 1
        else:
            answer += '5. Не верно\n'

        answer += f'Количесво набранных баллов: {balls}'

        await message.answer(answer)
    else:
        await message.answer('Ошибка при сканировании, отправьте другое фото')

    photo = open(photo_name, 'rb')
    await message.answer_photo(photo)


@dp.callback_query_handler()
async def call(callback: types.CallbackQuery):
    if callback.data == 'старт':
        await callback.bot.send_message(callback.message.chat.id,
                                        advice_text,
                                        parse_mode='HTML')
        await callback.answer('ждем фоток')


executor.start_polling(dp)
