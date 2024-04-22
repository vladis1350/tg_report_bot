from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import utils.btn_names as btn
from DBDataParser import parse_work_list
from core.dataFetcher import get_works_type, update_user, edit_work_type, get_work_list, get_selected_work, \
    get_work_by_id
from keyboards.AllMenu import get_works_type_btn_list, get_work_list_buttons_for_edit, get_edit_work_menu
from utils.stateform import StepsForm

router = Router()
reserve_field = {}


@router.message(F.text == btn.ADD_INFO_REP)
async def add_info(message: Message, state: FSMContext):
    await message.answer("Добавление")


@router.message(F.text == btn.EDIT_INFO_REP)
async def add_info(message: Message, state: FSMContext):
    try:
        work_list = await get_work_list()
        ww = parse_work_list(work_list)
        await message.answer("Выберите работу для редактирования ячеек данных:",
                             reply_markup=get_work_list_buttons_for_edit(ww))
        await state.set_state(StepsForm.SELECT_WORK_FOR_EDIT)
        await update_user(message.from_user.id, StepsForm.SELECT_WORK_FOR_EDIT, message.message_id)
    except Exception as mess:
        await message.answer("Ошибка получения данных\n" + str(mess))


@router.callback_query(StepsForm.SELECT_WORK_FOR_EDIT)
async def select_work_for_edit(callback: CallbackQuery, state: FSMContext):
    work = await get_selected_work(callback.data, "summ")
    try:
        message_text = callback.data.upper() + f"\n(лист - '{work['list_name']}')"
        await callback.message.edit_text(message_text)
        await callback.message.edit_reply_markup(reply_markup=get_edit_work_menu(work))
        await state.set_state(StepsForm.EDIT_SELECTED_WORK)
        await update_user(callback.message.from_user.id, StepsForm.EDIT_SELECTED_WORK, callback.message.message_id)
    except Exception as mess:
        await callback.message.answer("Ошибка получения данных\n" + str(mess))


@router.callback_query(StepsForm.EDIT_SELECTED_WORK)
async def edit_selected_work(callback: CallbackQuery, state: FSMContext):
    reserve_field['field'] = callback.data.lower()
    await callback.message.answer(f"Введите новую ячейку\n")
    await state.set_state(StepsForm.INPUT_NEW_VALUE_FOR_EDIT)


@router.message(StepsForm.INPUT_NEW_VALUE_FOR_EDIT)
async def input_new_value_for_edit(message: Message, state: FSMContext):
    message_text = message.text
    print(reserve_field)
    work = ''
    if 'plan_' in reserve_field['field']:
        work = await get_work_by_id(reserve_field['field'][5:], message_text, "plan")
    elif 'fact_' in reserve_field['field']:
        work = await get_work_by_id(reserve_field['field'][5:], message_text, "fact")
    elif 'per_day_' in reserve_field['field']:
        work = await get_work_by_id(reserve_field['field'][8:], message_text, "per_day")

    await message.answer("Изменения сохранены!", reply_markup=get_edit_work_menu(work))


@router.message(F.text == btn.DELETE_INFO_REP)
async def add_info(message: Message):
    await message.answer("Удаление")


@router.message(F.text == btn.ON_OFF_REPORT_DATA)
async def add_info(message: Message, state: FSMContext):
    try:
        works_type_list = await get_works_type()
        await message.answer("Отчётные данные: ", reply_markup=get_works_type_btn_list(works_type_list))
        await state.set_state(StepsForm.SELECT_WORK_TYPE_FOR_REPORT)
        await update_user(message.from_user.id, StepsForm.SELECT_WORK_TYPE_FOR_REPORT, message.message_id)
    except Exception as e:
        await message.answer("Ошибка получения данных от сервера, попробуйте позже. \n\n " + str(e))
        await state.set_state(StepsForm.SETTINGS_REPORT)
        await update_user(message.from_user.id, StepsForm.SETTINGS_REPORT, message.message_id)


@router.callback_query(StepsForm.SELECT_WORK_TYPE_FOR_REPORT)
async def select_work_type_for_rep(callback: CallbackQuery, state: FSMContext):
    try:
        await edit_work_type(callback.data)
        works_type_list = await get_works_type()
        await callback.message.edit_reply_markup(reply_markup=get_works_type_btn_list(works_type_list))
        await state.set_state(StepsForm.SELECT_WORK_TYPE_FOR_REPORT)
    except Exception as e:
        await callback.message.answer("Ошибка получения данных от сервера, попробуйте позже. \n\n " + str(e))
        await state.set_state(StepsForm.SETTINGS_REPORT)
        await update_user(callback.message.from_user.id, StepsForm.SETTINGS_REPORT, callback.message.message_id)
