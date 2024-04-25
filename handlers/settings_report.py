from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import utils.btn_names as btn
from DBDataParser import parse_work_list
from core.dataFetcher import get_works_type, update_user, edit_work_type, get_work_list, get_selected_work, \
    get_work_by_id, delete_work, create_new_work, create_new_work_type
from keyboards.AllMenu import get_works_type_btn_list, get_work_list_buttons, get_edit_work_menu, \
    get_confirmation_button, get_setting_report_menu, get_work_list_for_add_info
from utils.stateform import StepsForm

router = Router()
reserve_field = {}
new_work = {}
new_work_type = {}


@router.message(F.text == btn.ADD_INFO_REP)
async def add_info(message: Message, state: FSMContext):
    try:
        work_list = await get_work_list()
        ww = parse_work_list(work_list)
        await message.answer("При добавлении данных вводятся ячейки Google таблиц где хранятся данные!")
        await message.answer("Выберите работу для добавления данных", reply_markup=get_work_list_for_add_info(ww))
        await state.set_state(StepsForm.SELECT_WORK_FOR_ADD_DATA)
        await update_user(message.from_user.id, StepsForm.SELECT_WORK_FOR_ADD_DATA, message.message_id)
    except Exception as m:
        await message.answer(f"Ошибка получения списка работ\n{m}",
                             reply_markup=None)


@router.callback_query(StepsForm.SELECT_WORK_FOR_ADD_DATA)
async def select_work_for_add_data(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    if callback.data == btn.ADD_NEW_WORK:
        await callback.message.answer("Введите название работы: ")
        await state.set_state(StepsForm.ADD_NEW_WORK_TYPE)
    else:
        new_work['work_name'] = callback.data
        await callback.message.delete()
        await callback.message.answer("Введите название листа: ")
        await state.set_state(StepsForm.INPUT_LIST)
        await update_user(callback.message.from_user.id, StepsForm.INPUT_LIST, callback.message.message_id)


@router.message(StepsForm.ADD_NEW_WORK_TYPE)
async def add_new_work_type(message: Message, state: FSMContext):
    new_work_type['work_name'] = message.text
    await message.answer("Введите название категории: ")
    await state.set_state(StepsForm.INPUT_CATEGORY)
    await update_user(message.from_user.id, StepsForm.INPUT_CATEGORY, message.message_id)


@router.message(StepsForm.INPUT_CATEGORY)
async def enter_category(message: Message, state: FSMContext):
    new_work_type['categories'] = message.text
    await message.answer("Введите единицу измерения: ")
    await state.set_state(StepsForm.INPUT_UNIT_TYPE)
    await update_user(message.from_user.id, StepsForm.INPUT_UNIT_TYPE, message.message_id)


@router.message(StepsForm.INPUT_UNIT_TYPE)
async def input_category(message: Message, state: FSMContext):
    new_work_type['unit'] = message.text
    resp = await create_new_work_type(new_work_type)
    print(resp)
    if resp['status'] == 201:
        new_work['work_name'] = new_work_type['work_name']
        await message.answer("Введите название листа: ")
        await state.set_state(StepsForm.INPUT_LIST)
        await update_user(message.from_user.id, StepsForm.INPUT_LIST, message.message_id)
    else:
        await message.answer("Что-то пошло не так!")
        await state.set_state(StepsForm.SETTINGS_REPORT)
        await update_user(message.from_user.id, StepsForm.SETTINGS_REPORT, message.message_id)


@router.message(StepsForm.INPUT_LIST)
async def input_list(message: Message, state: FSMContext):
    new_work['list_name'] = message.text
    await message.answer("Введите номер ячейки со значение - ПЛАН: ")
    await state.set_state(StepsForm.INPUT_RANGE_ONE)
    await update_user(message.from_user.id, StepsForm.INPUT_RANGE_ONE, message.message_id)


@router.message(StepsForm.INPUT_RANGE_ONE)
async def input_range_one(message: Message, state: FSMContext):
    new_work['plan'] = message.text
    await message.answer("Введите номер ячейки со значение - ФАКТ: ")
    await state.set_state(StepsForm.INPUT_RANGE_TWO)
    await update_user(message.from_user.id, StepsForm.INPUT_RANGE_TWO, message.message_id)


@router.message(StepsForm.INPUT_RANGE_TWO)
async def input_range_two(message: Message, state: FSMContext):
    new_work['fact'] = message.text
    await message.answer("Введите номер ячейки со значение - ЗА ДЕНЬ: ")
    await state.set_state(StepsForm.INPUT_RANGE_THREE)
    await update_user(message.from_user.id, StepsForm.INPUT_RANGE_THREE, message.message_id)


@router.message(StepsForm.INPUT_RANGE_THREE)
async def input_range_two(message: Message, state: FSMContext):
    new_work['per_day'] = message.text
    resp = await create_new_work(new_work)
    if resp['status'] == 201:
        await message.answer(f"Успешно добавленно!")
    else:
        await message.answer(
            f"Данные для этого вида работ уже добавлены ранее, вы можете отредактировать их нажав 'Изменить данные'!",
            reply_markup=get_setting_report_menu())
    await state.set_state(StepsForm.SETTINGS_REPORT)
    await update_user(message.from_user.id, StepsForm.SETTINGS_REPORT, message.message_id)


@router.message(F.text == btn.EDIT_INFO_REP)
async def add_info(message: Message, state: FSMContext):
    try:
        work_list = await get_work_list()
        ww = parse_work_list(work_list)
        await message.answer("Выберите работу для редактирования ячеек данных:",
                             reply_markup=get_work_list_buttons(ww))
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
    work = ''
    if 'plan_' in reserve_field['field']:
        work = await get_work_by_id(reserve_field['field'][5:], message_text, "plan")
    elif 'fact_' in reserve_field['field']:
        work = await get_work_by_id(reserve_field['field'][5:], message_text, "fact")
    elif 'per_day_' in reserve_field['field']:
        work = await get_work_by_id(reserve_field['field'][8:], message_text, "per_day")

    await message.answer("Изменения сохранены!", reply_markup=get_edit_work_menu(work))


@router.message(F.text == btn.DELETE_INFO_REP)
async def select_work_for_del(message: Message, state: FSMContext):
    try:
        work_list = await get_work_list()
        ww = parse_work_list(work_list)
        await message.answer("Выберите работу для удаления:",
                             reply_markup=get_work_list_buttons(ww))
        await state.set_state(StepsForm.SELECT_WORK_FOR_DELETE)
        await update_user(message.from_user.id, StepsForm.SELECT_WORK_FOR_DELETE, message.message_id)
    except Exception as mess:
        await message.answer("Ошибка получения данных\n" + str(mess))


@router.callback_query(StepsForm.SELECT_WORK_FOR_DELETE)
async def confirm_delete_info(callback: CallbackQuery, state: FSMContext):
    reserve_field['field_for_del'] = callback.data
    await callback.message.delete()
    await callback.message.answer(f"Вы действительно хотите удалить информацию: {callback.data}\n",
                                  reply_markup=get_confirmation_button())
    await state.set_state(StepsForm.DELETE_INFO)
    await update_user(callback.message.from_user.id, StepsForm.DELETE_INFO, callback.message.message_id)


@router.callback_query(StepsForm.DELETE_INFO)
async def delete_info(callback: CallbackQuery, state: FSMContext):
    work_name = reserve_field['field_for_del']
    await callback.message.delete()
    if callback.data == 'yes_del':
        a = await delete_work(work_name)
        await callback.message.answer(f"{work_name} - Удаленно!\n {a}",
                                      reply_markup=get_setting_report_menu())
    elif callback.data == 'no_del':
        await callback.message.answer(f"Удаление отмененно!\n",
                                      reply_markup=get_setting_report_menu())

    await state.set_state(StepsForm.SETTINGS_REPORT)
    await update_user(callback.message.from_user.id, StepsForm.SETTINGS_REPORT, callback.message.message_id)


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
