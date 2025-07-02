from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from utils.dates import *
from api_tests.common import *
import requests as r
import pytest
import allure
import time
from uuid import UUID


actions = ["analyze", "apply_gpt", "stt", "swap_channels", "get_api_tags", "apply_notify_rules",
           "apply_addressbook_tags", "delete"]
           #"call_reload_source_integration", "handle_continuous_recordings", "restore_continuous_recordings"]

@pytest.mark.api
@allure.title("test_settings_actions_with_communcations")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_settings_actions_with_communcations. settings, actions with communications. parametrize")
@pytest.mark.parametrize("task_type", actions)
def test_settings_actions_with_communications(task_type):

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD, upload_call=True)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("Give all rights for user"):
        headers_for_rights = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': TOKEN
        }

        data_for_rights = {
            "restt": True,
            "delete_call": True,
            "call_info_processing": True
        }

        give_rights_to_user = r.put(url=API_URL + f"/user/{USER_ID}/access_rights", headers=headers_for_rights, json=data_for_rights)

    with allure.step("Check status code == 204"):
        assert give_rights_to_user.status_code == 204

    with allure.step("Create task"):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': user_token,
        }

        data = {
            "start_date": today.strftime("%Y-%m-%d"),
            "end_date": today.strftime("%Y-%m-%d"),
            "action": task_type,
        }

        data_for_stt = {
            "start_date": today.strftime("%Y-%m-%d"),
            "end_date": today.strftime("%Y-%m-%d"),
            "action":task_type,
            "sttOptions":{
                "sttEngine":"vosk",
                "sttEconomize": True,
                "sttOptionsMap":{
                    "language":"ru-RU",
                    "model":"default",
                    "merge_all_to_one_audio": True,
                    "count_per_iteration":1,
                    "diarization": False}
            }
        }

        if task_type == "stt":
            create_task = r.post(url=API_URL + "/calls/action", headers=headers, json=data_for_stt)
        else:
            create_task = r.post(url=API_URL + "/calls/action", headers=headers, json=data)

        task_id = create_task.json()["task_id"]

    with allure.step("Check status code == 200 and we get UUID"):
        assert create_task.status_code == 200
        assert isinstance(UUID(task_id), UUID)  # Ensure it's a UUID instance
        assert UUID(task_id).version == 4  # Check if it's a version 4 UUID

    with allure.step("Sleep 10 sec"):
        time.sleep(10)

    with allure.step("Get tasks"):
        get_progress_tasks = r.get(url=API_URL + "/progress_tasks", headers=headers)
        json_get_progress_tasks = get_progress_tasks.json()

    with allure.step("Check status code == 200 and response"):
        assert get_progress_tasks.status_code == 200
        assert json_get_progress_tasks[0]["task_id"] == task_id  # check task_id
        assert json_get_progress_tasks[0]["owner"] == USER_ID  # check task belongs to created user
        assert json_get_progress_tasks[0]["status"] == "SUCCESS" # check status
        assert json_get_progress_tasks[0]["action"] == task_type  # check action type
        assert json_get_progress_tasks[0]["progress"] == {}
        assert today.strftime("%Y-%m-%d") in json_get_progress_tasks[0]["add_time"]
        assert today.strftime("%Y-%m-%d") in json_get_progress_tasks[0]["done_time"]
        #assert json_get_progress_tasks[0]["title"] == {}
        #  https://task.imot.io/browse/DEV-3222
        assert json_get_progress_tasks[0]["task_interval"] == f"Коммуникации за: {today_with_dots}-{today_with_dots}"
        assert json_get_progress_tasks[0]["total"] == 1
        assert json_get_progress_tasks[0]["current"] == 1

    with allure.step("Get task"):
        get_task_status = r.get(url=API_URL + f"/task/{task_id}/status", headers=headers)
        json_get_task_status = get_task_status.json()

    with allure.step("Check status code == 200 and response"):
        assert get_task_status.status_code == 200
        assert json_get_task_status["task_id"] == task_id  # check task_id
        assert json_get_task_status["owner"] == USER_ID  # check task belongs to created user
        assert json_get_task_status["status"] == "SUCCESS"  # check status
        assert json_get_task_status["action"] == task_type  # check action type
        assert json_get_task_status["progress"] == {}
        assert today.strftime("%Y-%m-%d") in json_get_task_status["add_time"]
        assert today.strftime("%Y-%m-%d") in json_get_task_status["done_time"]
        # assert json_get_task_status["title"] == {}
        #  https://task.imot.io/browse/DEV-3222
        assert json_get_task_status["task_interval"] == f"Коммуникации за: {today_with_dots}-{today_with_dots}"
        assert json_get_task_status["total"] == 1
        assert json_get_task_status["current"] == 1

    with allure.step("Delete task"):
        delete_task = r.delete(url=API_URL + f"/task/{task_id}", headers=headers)

    with allure.step("Check that status code == 204"):
        assert delete_task.status_code == 204

    with allure.step("Get tasks and check status code == 200 and []"):
        get_progress_tasks = r.get(url=API_URL + "/progress_tasks", headers=headers)

        assert  get_progress_tasks.status_code == 200
        assert get_progress_tasks.json() == []

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)

