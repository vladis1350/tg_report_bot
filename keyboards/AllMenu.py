from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton

import utils.btn_names as btn


def get_main_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=btn.GET_REPORT)
    kb.button(text=btn.SETTING_REPORT)
    kb.button(text=btn.PIVOT_DATA)
    kb.button(text=btn.TEST)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_setting_report_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=btn.ADD_INFO_REP)
    kb.button(text=btn.EDIT_INFO_REP)
    kb.button(text=btn.DELETE_INFO_REP)
    kb.button(text=btn.ON_OFF_REPORT_DATA)
    kb.button(text=btn.CANCEL)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_pivot_data_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=btn.WORK_LIST)
    kb.button(text=btn.PREPARATION_TABLES)
    kb.button(text=btn.INSERT_PIVOT_DATA)
    kb.button(text=btn.CANCEL)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_dop_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=btn.ONE)
    kb.button(text=btn.TWO)
    kb.button(text=btn.THREE)
    kb.button(text=btn.CANCEL)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_work_list_buttons(ww) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for i in ww:
        kb.button(text=i, callback_data=i)
    kb.adjust(1)
    return kb.as_markup()


def get_work_list_for_add_info(ww) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for i in ww:
        kb.button(text=i, callback_data=i)
    kb.row(InlineKeyboardButton(text=btn.ADD_NEW_WORK, callback_data=btn.ADD_NEW_WORK), width=1)
    kb.adjust(1)
    return kb.as_markup()


def get_editing_report_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Редактировать ячейки данных")
    kb.button(text="Редактировать названия работ")
    kb.button(text="Назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_edit_work_menu(work) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Лист: " + work['list_name'], callback_data='list_name_' + str(work['id']))
    kb.button(text="План: " + work['plan'], callback_data='plan_' + str(work['id']))
    kb.button(text="Факт: " + work['fact'], callback_data='fact_' + str(work['id']))
    kb.button(text="За день: " + work['per_day'], callback_data='per_day_' + str(work['id']))
    kb.adjust(1)
    return kb.as_markup()


def get_unit_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="тонны", callback_data="tonn")
    kb.button(text="гектары", callback_data="ga")
    kb.adjust(1)
    return kb.as_markup()


def get_works_type_btn_list(works_type_list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for _ in works_type_list:
        if _['is_report']:
            kb.button(text="✅ " + _['work_name'], callback_data=_['work_name'])
        else:
            kb.button(text="❌ " + _['work_name'], callback_data=_['work_name'])
    kb.adjust(2)
    return kb.as_markup()


def get_farms_buttons_list() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for _ in btn.FARMS:
        kb.button(text=_, callback_data=_)
    kb.adjust(1)
    return kb.as_markup()


def get_confirmation_button() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Да", callback_data="yes_del")
    kb.button(text="Нет", callback_data="no_del")
    kb.adjust(1)
    return kb.as_markup()
