from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import DataBaseTgBot as mdb
import GenerateReport as gr
from core.WorkData import WorkData
from keyboards.AllMenu import get_main_menu, get_setting_report_menu, get_adding_info_to_report, get_unit_menu
from utils.stateform import StepsForm

router = Router()
work = WorkData(None, None, None, None, None)


@router.message(Command("start"))
async def cmd_start(message: Message):
    mdb.createNewUser({'chat_id': message.from_user.id, 'user_name': message.from_user.username,
                       'first_name': message.from_user.first_name,
                       'second_name': message.from_user.last_name})
    await message.answer('Главное меню', reply_markup=get_main_menu())


@router.message(F.text == "Получить отчёт")
async def get_report(message: Message):
    report = gr.generateReport()
    # report = gr.initial_ranges()
    await message.answer(report, reply_markup=get_main_menu())


@router.message(F.text == "Настройка отчёта")
async def setting_report(message: Message):
    await message.answer("Настройка отчёта", reply_markup=get_setting_report_menu())


@router.message(F.text == "Добавить информацию")
async def add_info(message: Message):
    await message.answer("Меню добавления информации в отчёт", reply_markup=get_adding_info_to_report())


@router.message(F.text == "Редактировать информацию")
async def add_info(message: Message):
    await message.answer(" ", reply_markup=get_adding_info_to_report())


@router.message(F.text == 'Добавить новую информацию')
async def add_new_info(message: Message, state: FSMContext):
    await message.answer("Введите название листа: ")
    await state.set_state(StepsForm.INPUT_LIST)


@router.message(StepsForm.INPUT_LIST)
async def input_list(message: Message, state: FSMContext):
    work.set_list_name(message.text)
    await message.answer("Введите наименование работы: ")
    await state.set_state(StepsForm.WORK_NAME)


@router.message(StepsForm.WORK_NAME)
async def input_work_name(message: Message, state: FSMContext):
    await message.answer("Введите номер ячейки со значение ФАКТ: ")
    work.set_work_name(message.text)
    await state.set_state(StepsForm.INPUT_RANGE_ONE)


@router.message(StepsForm.INPUT_RANGE_ONE)
async def input_range_one(message: Message, state: FSMContext):
    work.set_range_one(message.text)
    await message.answer("Введите номер ячейки со значение ЗА ДЕНЬ: ")
    await state.set_state(StepsForm.INPUT_RANGE_TWO)


@router.message(StepsForm.INPUT_RANGE_TWO)
async def input_range_two(message: Message, state: FSMContext):
    work.set_range_two(message.text)
    await message.answer("Выберите единицу измерения: ", reply_markup=get_unit_menu())
    await state.set_state(StepsForm.SELECT_UNIT)


@router.callback_query(StepsForm.SELECT_UNIT)
async def select_unit(callback: types.CallbackQuery, state: FSMContext):
    work.set_unit_w(callback.data)
    await callback.message.answer(f"Вы добавили работу: \n"
                                  f"Наименование работы: {work.work_name}\n"
                                  f"Наименование листа: {work.list_name}\n"
                                  f"Ячейка ФАКТ: {work.range_one}\n"
                                  f"Ячейка ЗА ДЕНЬ: {work.range_two}\n"
                                  f"Единица измерения: {work.unit_w}")
    mdb.createWork(work)
    await state.set_state(StepsForm.FINISH_ADDING_WORK)


@router.message(StepsForm.FINISH_ADDING_WORK)
async def finish_adding_work(message: Message, state: FSMContext):
    await message.answer(f"Работа успешно добавлена!", reply_markup=get_main_menu())
    # await state.set_state(StepsForm.MAIN_MENU)


@router.message(F.text == 'Редактировать ячейки данных')
async def edit_cell(message: Message):
    await message.answer(": ")
