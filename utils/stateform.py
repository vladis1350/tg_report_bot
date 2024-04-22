from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    INPUT_NEW_VALUE_FOR_EDIT = State()
    EDIT_SELECTED_WORK = State()
    SELECT_WORK_FOR_EDIT = State()
    SELECT_WORK_TYPE_FOR_REPORT = State()
    SETTINGS_REPORT = State()
    SELECT_WORK = State()
    PREPARATION_TABLES = State()
    START = State()
    GET_WORK_LIST = State()

    ADDING_NEW_REPORT_INFO_MENU = State()
    PIVOT_DATA_MENU = State()
    MAIN_MENU = State()
    DOP_MENU = State()

    INPUT_PASS = State()
    WRONG_PASS = State()

    INPUT_LIST = State()
    WORK_NAME = State()
    INPUT_RANGE_ONE = State()
    INPUT_RANGE_TWO = State()
    SELECT_UNIT = State()
    FINISH_ADDING_WORK = State()
