from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bs4 import BeautifulSoup

import utils.btn_names as btn
from core.dataFetcher import get_report as get_rep, get_user, check_user, update_user
from keyboards.AllMenu import get_main_menu, get_setting_report_menu
from utils.stateform import StepsForm

router = Router()
new_work = {}


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    try:
        is_true = await check_user({'chat_id': message.from_user.id})
        soup = BeautifulSoup(is_true, 'html.parser')
        rep = soup.p.string
        if rep == "True":
            await message.answer('Main MEnu', reply_markup=get_main_menu())
            await state.set_state(StepsForm.MAIN_MENU)
            await update_user(message.from_user.id, StepsForm.MAIN_MENU, message.message_id)
        else:
            await message.answer('Введите пароль для доступа к боту', reply_markup=None)
            await state.set_state(StepsForm.INPUT_PASS)
            await update_user(message.from_user.id, StepsForm.INPUT_PASS, message.message_id)
    except Exception as error_message:
        await message.answer(str(error_message), reply_markup=None)


@router.message(StepsForm.INPUT_PASS)
async def input_pass(message: Message, state: FSMContext):
    if message.text == "332261":
        await get_user({'chat_id': message.from_user.id, 'user_name': message.from_user.username,
                        'first_name': message.from_user.first_name,
                        'second_name': message.from_user.last_name,
                        'message_id': message.message_id,
                        'state': StepsForm.START})
        await message.answer("Всё верно", reply_markup=get_main_menu())
        await state.set_state(StepsForm.MAIN_MENU)
    else:
        await message.answer("Не верный пароль!")
        await state.set_state(StepsForm.INPUT_PASS)


@router.message(F.text == btn.GET_REPORT)
async def get_report(message: Message):
    try:
        report = await get_rep()
        soup = BeautifulSoup(report, 'html.parser')
        rep = soup.textarea.string
        await message.answer(rep, reply_markup=get_main_menu())
    except Exception as e:
        await message.answer("Ошибка получения данных\n\n " + str(e), reply_markup=get_main_menu())


@router.message(F.text == btn.SETTING_REPORT)
async def setting_report(message: Message, state: FSMContext):
    await message.answer(btn.SETTING_REPORT, reply_markup=get_setting_report_menu())
    await state.set_state(StepsForm.SETTINGS_REPORT)
    await update_user(message.from_user.id, StepsForm.SETTINGS_REPORT, message.message_id)


@router.message(StepsForm.INPUT_LIST)
async def input_list(message: Message, state: FSMContext):
    new_work['list_name'] = message.text
    await message.answer("Введите наименование работы: ")
    await state.set_state(StepsForm.WORK_NAME)


# @router.message(StepsForm.WORK_NAME)
# async def input_work_name(message: Message, state: FSMContext):
#     await message.answer("Введите номер ячейки со значение ФАКТ: ")
#     work.set_work_name(message.text)
#     await state.set_state(StepsForm.INPUT_RANGE_ONE)
#
#
# @router.message(StepsForm.INPUT_RANGE_ONE)
# async def input_range_one(message: Message, state: FSMContext):
#     work.set_range_one(message.text)
#     await message.answer("Введите номер ячейки со значение ЗА ДЕНЬ: ")
#     await state.set_state(StepsForm.INPUT_RANGE_TWO)
#
#
# @router.message(StepsForm.INPUT_RANGE_TWO)
# async def input_range_two(message: Message, state: FSMContext):
#     work.set_range_two(message.text)
#     await message.answer("Выберите единицу измерения: ", reply_markup=get_unit_menu())
#     await state.set_state(StepsForm.SELECT_UNIT)
#
#
# @router.callback_query(StepsForm.SELECT_UNIT)
# async def select_unit(callback: types.CallbackQuery, state: FSMContext):
#     work.set_unit_w(callback.data)
#     await callback.message.answer(f"Вы добавили работу: \n"
#                                   f"Наименование работы: {work.work_name}\n"
#                                   f"Наименование листа: {work.list_name}\n"
#                                   f"Ячейка ФАКТ: {work.range_one}\n"
#                                   f"Ячейка ЗА ДЕНЬ: {work.range_two}\n"
#                                   f"Единица измерения: {work.unit_w}")
#     mdb.createWork(work)
#     await state.set_state(StepsForm.FINISH_ADDING_WORK)


@router.message(StepsForm.FINISH_ADDING_WORK)
async def finish_adding_work(message: Message, state: FSMContext):
    await message.answer(f"Работа успешно добавлена!", reply_markup=get_main_menu())
    # await state.set_state(StepsForm.MAIN_MENU)


@router.message(F.text == 'Редактировать ячейки данных')
async def edit_cell(message: Message):
    await message.answer(": ")
