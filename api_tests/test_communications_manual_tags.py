from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from api_tests.common import *
from utils.dates import *
import requests as r
import pytest
import allure
import time

@pytest.mark.api
@allure.title("test_communications_manual_tags")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_communications_manual_tags. add, delete manual tag")
def test_communications_manual_tags():

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD, upload_call=True)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("Get call_id from today's search calls"):
        headers = {'Authorization': user_token}

        get_calls = r.post(url=API_URL + f'/search_calls/?start_date={today.strftime("%Y-%m-%d")}&end_date={today.strftime("%Y-%m-%d")}', headers=headers)
        call_id = get_calls.json()["call_ids"][0].replace('"', '')

    with allure.step("Check status code == 200 and we get call_id in response"):
        assert get_calls.status_code == 200
        assert len(call_id) == 24


    with allure.step("Check that call dont have any manual tags"):
        get_manual_tags_list = r.get(url=API_URL + "/tag_names?tag_group=manual", headers=headers)

    with allure.step("Check status code == 200 and list is empty"):
        assert get_calls.status_code == 200
        assert get_manual_tags_list.text == "[]"

    with allure.step("Add manual tag to call"):

        manual_tag_payload = {"name":"auto_api_test","tagType":"manual"}

        add_manual_tag = r.post(url=API_URL + f"/call/{call_id}/tag", headers=headers, json=manual_tag_payload)

        manual_tag_id = add_manual_tag.text.replace('"', '')

    with allure.step("Check status code == 201 and tag_id returned"):
        assert add_manual_tag.status_code == 201
        assert len(manual_tag_id) == 24

    with allure.step("Check that call have manual tags"):
        get_manual_tags_list = r.get(url=API_URL + "/tag_names?tag_group=manual", headers=headers)

    with allure.step("Check status code == 200 and tag exists"):
        assert get_calls.status_code == 200
        assert get_manual_tags_list.text == '["auto_api_test"]'

    with allure.step("Delete manual tag"):
        delete_manual_tag = r.delete(url=API_URL + f"/call/{call_id}/tag/{manual_tag_id}", headers=headers)

    with allure.step("Check status code == 204"):
        assert delete_manual_tag.status_code == 204

        #time.sleep(23)

    with allure.step("Wait until manual tags are cleared"):
        timeout = 40
        start_time = time.time()

        while True:
            get_manual_tags_list = r.get(url=API_URL + "/tag_names?tag_group=manual", headers=headers)

            if get_manual_tags_list.status_code == 200 and get_manual_tags_list.text == "[]":
                break

            if time.time() - start_time > timeout:
                raise AssertionError(f"Manual tags not cleared after {timeout} seconds")

            time.sleep(2)

    with allure.step("Check that call dont have any manual tags"):
        get_manual_tags_list = r.get(url=API_URL + "/tag_names?tag_group=manual", headers=headers)

    with allure.step("Check status code == 200 and list is empty"):
        assert get_calls.status_code == 200
        assert get_manual_tags_list.text == "[]"

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)