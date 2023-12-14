from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo


def get_main_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Получить отчёт")
    kb.button(text="Настройка отчёта")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_setting_report_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Добавить информацию")
    kb.button(text="Редактировать информацию")
    kb.button(text="Удалить информацию")
    kb.button(text="Назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_editing_report_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Редактировать ячейки данных")
    kb.button(text="Редактировать названия работ")
    kb.button(text="Назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_adding_info_to_report() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Добавить новую информацию")
    kb.button(text="Включить в отчёт имеющуюся информацию")
    kb.button(text="Назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


# def get_editing_info_to_report() -> ReplyKeyboardMarkup:
#     kb = ReplyKeyboardBuilder()
#     kb.button(text="Редактировать ячейки данных")
#     kb.button(text="Редактировать названия работ")
#     kb.button(text="Назад")
#     kb.adjust(1)
#     return kb.as_markup(resize_keyboard=True)


def get_unit_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="тонны", callback_data="tonn")
    kb.button(text="гектары", callback_data="ga")
    kb.adjust(1)
    return kb.as_markup()


