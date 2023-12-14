from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    MAIN_MENU = State()

    INPUT_LIST = State()
    WORK_NAME = State()
    INPUT_RANGE_ONE = State()
    INPUT_RANGE_TWO = State()
    SELECT_UNIT = State()
    FINISH_ADDING_WORK = State()
