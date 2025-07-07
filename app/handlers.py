from aiogram import F, Router
from aiogram.client.default import Default
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, TelegramObject
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

user_router = Router()

from app.deepseek_api import deepseek_generate
from app.middleware import MessagesLog
import app.keyboards as kb
from app import weatherapicom_api
from app.roulet import roulet
import config
from app.hm import queue_temp_day, queue_temp_hour, queue_usage_hour, queue_usage_day, show_temp, get_usage, get_temperature



user_router.message.middleware(MessagesLog())


# command start
@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('🫡', reply_markup= kb.commandstart)


# weather blok
@user_router.message(F.text == 'Погода')
async def cmd_weather(message: Message):
    await message.answer('🌎', reply_markup= kb.weather_inline)


@user_router.callback_query(F.data == 'Быково')
async def bykovo_weather(callback: CallbackQuery):
    await callback.message.answer(text=weatherapicom_api.get_weather_forecast("volgograd", "bykovo"))
    await callback.message.answer_photo(photo= f'http:{weatherapicom_api.get_weather_icon("volgograd", "bykovo")}',
                                   caption= f'{weatherapicom_api.get_weather_text("volgograd", "bykovo")}',
                                   parse_mode=None)


@user_router.callback_query(F.data == 'Волгоград')
async def bykovo_weather(callback: CallbackQuery):
    await callback.message.answer(text=weatherapicom_api.get_weather_forecast("volgograd"))
    await callback.message.answer_photo(photo=f'http:{weatherapicom_api.get_weather_icon("volgograd")}',
                                        caption=f'{weatherapicom_api.get_weather_text("volgograd")}',
                                        parse_mode=None)

class Pogoda(StatesGroup):
    wait_promt = State()
    quit1 = State()
@user_router.callback_query(F.data == 'Выбрать')
async def wait_prompt_region(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Pogoda.wait_promt)
    await callback.message.answer(text='Напиши интересующий город в формате\n"Регион, город"')



@user_router.message(Pogoda.wait_promt)
async def prompt_region(message: Message, state: FSMContext):
    await state.update_data(wait_promt=message.text)
    await message.answer(text= 'Нейросеть определяет наиболее подходящий регион...\nОжидание займет несколько секунд')
    await message.answer_photo(photo=f'http:{weatherapicom_api.get_weather_icon(weatherapicom_api.finding_sity(str(message.text)))}',
                                        caption=
                                        f'Наиболее подходящий найденный пункт:\n{weatherapicom_api.translating_city(weatherapicom_api.get_weather_name((weatherapicom_api.finding_sity(str(message.text)))))}\n{weatherapicom_api.get_weather_text(weatherapicom_api.finding_sity(str(message.text)))}',
                                        parse_mode=None)
    await message.answer(text=weatherapicom_api.get_weather_forecast(weatherapicom_api.finding_sity(str(message.text))))
    await state.clear()






# weather blok finish


@user_router.message(F.text == 'Сервер')
async def servers(message: Message):
    await message.answer('Собираем данные..')
    await message.answer(F'Сейчас:\nCpu usage - {get_usage()[1]}%\nMemory free - {get_usage()[2]}, memory use - {get_usage()[3]}\nДатчики:\n{show_temp(get_temperature())}')
    await message.answer(F'За последний час:\nCpu usage - {queue_usage_hour.get()[0]}%\nMemory free - {queue_usage_hour.get()[1]}, memory use - {queue_usage_hour.get()[2]}\nДатчики:\n{show_temp(queue_temp_hour.get())}')
    await message.answer(F'За сутки:\nCpu usage - {queue_usage_day.get()[0]}%\nMemory free - {queue_usage_day.get()[1]}, memory use - {queue_usage_day.get()[2]}\nДатчики:\n{show_temp(queue_temp_day.get())}')


@user_router.message(F.text == 'popajopa')
async def jopa(message: Message):
    await message.answer('POPA')


@user_router.message(F.text == 'Рулетка')
async def roll(message: Message):
    await message.answer(f'{roulet()}')


# gtp blok
class Neiro(StatesGroup):
    wait_promt = State()
    quit = State()


@user_router.message(F.text == 'Нейронка')
async def neiro_start(message: Message, state: FSMContext):
    await state.set_state(Neiro.wait_promt)
    await message.answer('promt')
    await message.answer('🦾', reply_markup=kb.neiro)


@user_router.message(F.text == 'Quit')
async def neiro_quit(message: Message, state: FSMContext):
    await state.set_state(Neiro.quit)
    await message.answer('🫡', reply_markup=kb.commandstart)
    await state.clear()


@user_router.message(Neiro.wait_promt)
async def promt(message: Message, state: FSMContext):
    await state.update_data(wait_promt=message.text)
    await message.answer("Нейросеть думает...")
    response = await deepseek_generate(user_id=message.from_user.id,
                                       text=message.text)
    await message.reply(response)
# gpt block final


# message info (optional ON)
# @user_router.message()
# async def handle_message(message: TelegramObject):
#     print(f"Message ID: {message.message_id}")
#     print(f"From: {message.from_user.full_name} (ID: {message.from_user.id})")
#     print(f"Chat ID: {message.chat.id}")
#     print(f"Text: {message.text}")
#     print(f"Date: {message.date}")


# unknown command
@user_router.message(F.text)
async def hozyain(message: Message):
    if message not in config.commands_words:
        await message.answer_photo(photo= (config.hozyain_id),
                                   caption= 'Чего надо, хозяин?\n||Неизвестная команда, введите /start||',
                                   parse_mode='MarkdownV2')





