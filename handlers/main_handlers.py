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


# @router.message(F.text == btn.TEST)
# async def setting_report(message: Message, state: FSMContext):
#     test = await test_table()
#     print(test)
#     await message.answer("Good")
