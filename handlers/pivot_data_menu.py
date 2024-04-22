from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bs4 import BeautifulSoup

import utils.btn_names as btn
from DBDataParser import parse_work_list, parse_work_to_string
from core.dataFetcher import get_work_list, update_user, update_pivot_tables, get_selected_work, get_user_by_id
from keyboards.AllMenu import get_pivot_data_menu, get_work_list_buttons, get_main_menu, get_dop_menu, \
    get_setting_report_menu
from utils.stateform import StepsForm

router = Router()


@router.message(F.text == btn.PIVOT_DATA)
async def pivot_data_menu(message: Message, state: FSMContext):
    await message.answer(btn.PIVOT_DATA, reply_markup=get_pivot_data_menu())
    await state.set_state(StepsForm.GET_WORK_LIST)
    await update_user(message.from_user.id, StepsForm.PIVOT_DATA_MENU, message.message_id)


@router.message(F.text == btn.WORK_LIST)
async def pivot_data_menu(message: Message, state: FSMContext):
    try:
        work_list = await get_work_list()
        ww = parse_work_list(work_list)
        await message.answer("Список выполняемых работ:", reply_markup=get_work_list_buttons(ww))
        await state.set_state(StepsForm.SELECT_WORK)
        await update_user(message.from_user.id, StepsForm.SELECT_WORK, message.message_id)
    except Exception as e:
        await message.answer(str(e), reply_markup=get_pivot_data_menu())
        await state.set_state(StepsForm.PIVOT_DATA_MENU)
        await update_user(message.from_user.id, StepsForm.PIVOT_DATA_MENU, message.message_id)


@router.message(F.text == btn.PREPARATION_TABLES)
async def reparation_tables(message: Message, state: FSMContext):
    result = await update_pivot_tables()
    soup = BeautifulSoup(result, 'html.parser')
    s = ""
    res_list = soup.find_all('p')
    for _ in res_list:
        s += _.text + "\n"
    try:
        await message.answer(s, reply_markup=None)
    except Exception as e:
        await message.answer("Ошибка получения данных от сервера!\n" + str(e), reply_markup=None)
    await state.set_state(StepsForm.PREPARATION_TABLES)
    await update_user(message.from_user.id, StepsForm.PREPARATION_TABLES, message.message_id)


@router.callback_query(StepsForm.SELECT_WORK)
async def select_work(callback: types.CallbackQuery, state: FSMContext):
    work = await get_selected_work(callback.data, "list")
    try:
        work_string = callback.data.upper() + ":" + parse_work_to_string(work)
        await callback.message.delete()
        await callback.message.answer(work_string, reply_markup=get_pivot_data_menu())
        await state.set_state(StepsForm.PIVOT_DATA_MENU)
    except Exception:
        work_string = callback.data + ":\n\nНет данных"
        await callback.message.delete()
        await callback.message.answer(work_string, reply_markup=get_pivot_data_menu())
        await state.set_state(StepsForm.PIVOT_DATA_MENU)


@router.message(F.text == btn.CANCEL)
async def cancel(message: Message, state: FSMContext):
    user = await get_user_by_id({'chat_id': message.from_user.id})
    if user['state_bot'] in str([StepsForm.SELECT_WORK, StepsForm.PIVOT_DATA_MENU, StepsForm.GET_WORK_LIST,
                                 StepsForm.PREPARATION_TABLES, StepsForm.SETTINGS_REPORT,
                                 StepsForm.SELECT_WORK_TYPE_FOR_REPORT, StepsForm.SELECT_WORK_FOR_EDIT]):
        await message.answer("Главное меню", reply_markup=get_main_menu())
        await state.set_state(StepsForm.MAIN_MENU)
        await update_user(message.from_user.id, StepsForm.MAIN_MENU, message.message_id)
    elif user['state_bot'] in str([StepsForm.DOP_MENU]):
        await message.answer("Меню сводные данные", reply_markup=get_pivot_data_menu())
        await state.set_state(StepsForm.PIVOT_DATA_MENU)
        await update_user(message.from_user.id, StepsForm.PIVOT_DATA_MENU, message.message_id)
    elif user['state_bot'] in str([StepsForm.ADDING_NEW_REPORT_INFO_MENU]):
        await message.answer("Настройка отчёта", reply_markup=get_setting_report_menu())
        await state.set_state(StepsForm.SETTINGS_REPORT)
        await update_user(message.from_user.id, StepsForm.SETTINGS_REPORT, message.message_id)


@router.message(F.text == "DOP")
async def dop_menu(message: Message, state: FSMContext):
    await message.answer("DOP MENU", reply_markup=get_dop_menu())
    await state.set_state(StepsForm.DOP_MENU)
    await update_user(message.from_user.id, StepsForm.DOP_MENU, message.message_id)
