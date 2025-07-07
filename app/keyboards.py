from aiogram.types import  (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import  ReplyKeyboardBuilder, InlineKeyboardBuilder

# knopke reply
commandstart = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Погода'), KeyboardButton(text='Нейронка')],
    [KeyboardButton(text= 'Сервер')],
    [KeyboardButton(text= 'Рулетка')]
],
resize_keyboard=True,
input_field_placeholder='commands')


# neiro
# knopke reply
neiro = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Reset chat')],

    [KeyboardButton(text= 'Quit')]
],
resize_keyboard=True,
input_field_placeholder='commands')
# callback knopke

weather_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text= 'Быково', callback_data='Быково')],
    [InlineKeyboardButton(text= 'Волгоград', callback_data='Волгоград')],
    [InlineKeyboardButton(text= 'Выбрать', callback_data='Выбрать')]
])


# knopke inline
settings = InlineKeyboardMarkup(inline_keyboard= [
[InlineKeyboardButton(text='youtube', url='https://www.youtube.com/')]
])

# knopke inline/reply cherez buider

cars = ['Uaz', 'Gazel', 'Volga']

async def reply_cars():
    keyboard = ReplyKeyboardBuilder()
    for car in cars:
        keyboard.add(KeyboardButton(text=car))
    return keyboard.adjust(2).as_markup()


async def inline_cars():
    keyboard = InlineKeyboardBuilder()
    for car in cars:
        keyboard.add(InlineKeyboardButton(text=car, url='https://youtube.com'))
    return keyboard.adjust(2).as_markup()

