import aiohttp

from core.localSettings import REPORT_API_URL, GET_USER_BY_ID_API_URL, CHECK_USER_BY_ID_API_URL, GET_WORK_LIST_API_URL
from core.localSettings import UPDATE_USER_STATE_API_URL, UPDATE_PIVOT_TABLES_API_URL, GET_SELECTED_WORK_API_URL, \
    GET_WORK_TYPE_LIST_API_URL, EDIT_WORK_TYPE_API_URL, GET_WORK_BY_ID_API_URL, DELETE_WORK_API_URL, \
    CREATE_NEW_WORK_API_URL, CREATE_NEW_WORK_TYPE_API_URL


async def get_report():
    async with aiohttp.ClientSession() as session:
        async with session.get(REPORT_API_URL) as response:
            return await response.text()


async def get_user(user_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(GET_USER_BY_ID_API_URL, data=user_data) as response:
            return await response.text()


async def check_user(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.post(CHECK_USER_BY_ID_API_URL, data=user_id) as response:
            return await response.text()


async def update_user(chat_id, state, message_id):
    data = {"chat_id": chat_id, "state": state, 'message_id': message_id}
    async with aiohttp.ClientSession() as session:
        async with session.post(UPDATE_USER_STATE_API_URL, data=data) as response:
            return await response.text()


async def get_work_list():
    async with aiohttp.ClientSession() as session:
        async with session.get(GET_WORK_LIST_API_URL) as response:
            return await response.json()


async def update_pivot_tables():
    async with aiohttp.ClientSession() as session:
        async with session.get(UPDATE_PIVOT_TABLES_API_URL) as response:
            return await response.text()


async def get_selected_work(data, type_response):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(GET_SELECTED_WORK_API_URL,
                                    data={"work_name": data, "type_response": type_response}) as response:
                return await response.json()
        except Exception as message:
            print(str(message))
            return False


async def get_user_by_id(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.post(GET_USER_BY_ID_API_URL, data=user_id) as response:
            return await response.json()


async def get_work_by_id(work_id, new_value, field):
    print(work_id)
    async with aiohttp.ClientSession() as session:
        async with session.post(GET_WORK_BY_ID_API_URL, data={'work_id': int(work_id),
                                                              'new_value': new_value,
                                                              'field': field}) as response:
            return await response.json()


async def get_works_type():
    async with aiohttp.ClientSession() as session:
        async with session.get(GET_WORK_TYPE_LIST_API_URL) as response:
            return await response.json()


async def edit_work_type(selected_work):
    async with aiohttp.ClientSession() as session:
        async with session.post(EDIT_WORK_TYPE_API_URL, data={'work_type': selected_work}) as response:
            return await response.text()


async def delete_work(work_name):
    async with aiohttp.ClientSession() as session:
        async with session.post(DELETE_WORK_API_URL, data={'work_name': work_name}) as response:
            return await response.text()


# async def test_table(first_name, last_name, user_name):
#     async with aiohttp.ClientSession() as session:
#         data = {'first_name': first_name, "last_name": last_name, "user_name": user_name}
#         async with session.post(TEST_TABLE_API_URL, data=data) as response:
#             return await response.json()


async def create_new_work(new_work):
    async with aiohttp.ClientSession() as session:
        async with session.post(CREATE_NEW_WORK_API_URL, data=new_work) as response:
            return await response.json()


async def create_new_work_type(new_work_type):
    async with aiohttp.ClientSession() as session:
        async with session.post(CREATE_NEW_WORK_TYPE_API_URL, data=new_work_type) as response:
            return await response.json()
