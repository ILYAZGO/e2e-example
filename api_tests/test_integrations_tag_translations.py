from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from api_tests.common import *
import requests
import pytest
import allure


@pytest.mark.api
@allure.title("test_integrations_create_update_delete_tag_translation")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_integrations_create_update_delete_tag_translation")
def test_integrations_create_update_delete_tag_translation():
    tag_list = ["auto","auto_rule"]

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD, upload_call=True)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("Get tags only for integration"):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': user_token,
        }

        get_tags_list = requests.get(url=API_URL + f'/tag_names?only_form_integrations=true', headers=headers)

    with allure.step("Check status code == 200 and not empty"):
        assert get_tags_list.status_code == 200
        assert len(get_tags_list.json()) == 12
        assert "auto" in get_tags_list.text
        assert "auto_rule" in get_tags_list.text

    with allure.step("GET /tag_translations/user"):
        get_translations_list = requests.get(url=API_URL + f'/tag_translations/user', headers=headers)

    with allure.step("Check status code == 200 and empty"):
        assert get_translations_list.status_code == 200
        assert get_translations_list.text == "[]"

    with allure.step("Create tag translation"):
        payload = {
            "language":"ru",
            "owner":f"{USER_ID}",
            "originalTagName":"auto",
            "translatedTagName":"otua",
            "integrationServiceName":"comment",
            "isGlobal":False
        }
        create_tag_translation = requests.post(url=API_URL + f'/tag_translations', headers=headers, json=payload)
        translation_id = create_tag_translation.text.replace('"', '')

    with allure.step("Check status code == 200 and we get id"):
        assert create_tag_translation.status_code == 200
        assert len(translation_id) == 24

    with allure.step("GET /tag_translations/user"):
        get_translations_list = requests.get(url=API_URL + f'/tag_translations/user', headers=headers)

    with allure.step("Check status code == 200 and empty"):
        list_with_translation = [
            {
                "id": f"{translation_id}",
                "language": "ru",
                "owner": "None",
                "originalTagName": "auto",
                "translatedTagName": "otua",
                "integrationServiceName": "comment",
                "isGlobal": False
            }
        ]

        assert get_translations_list.status_code == 200
        assert get_translations_list.json() == list_with_translation

    with allure.step("Update tag translation"):
        payload = {
            "language": "ru",
            "owner": f"{USER_ID}",
            "originalTagName": "auto_rule",
            "translatedTagName": "update",
            "integrationServiceName": "update",
            "isGlobal": False
        }
        update_tag_translation = requests.put(url=API_URL + f'/tag_translations/{translation_id}', headers=headers, json=payload)

    with allure.step("Check status code == 204 "):
        assert update_tag_translation.status_code == 204

    with allure.step("GET /tag_translations/user"):
        get_translations_list = requests.get(url=API_URL + f'/tag_translations/user', headers=headers)

    with allure.step("Check status code == 200 and empty"):
        updated_list_with_translation = [
            {
                "id": f"{translation_id}",
                "language": "ru",
                "owner": "None",
                "originalTagName": "auto_rule",
                "translatedTagName": "update",
                "integrationServiceName": "update",
                "isGlobal": False
            }
        ]

        assert get_translations_list.status_code == 200
        assert get_translations_list.json() == updated_list_with_translation

    with allure.step("DELETE tag translation"):
        delete_tag_translation = requests.delete(url=API_URL + f'/tag_translations/{translation_id}', headers=headers)

    with allure.step("Check status code == 204"):
        assert delete_tag_translation.status_code == 204


    with allure.step("GET /tag_translations/user"):
        get_translations_list = requests.get(url=API_URL + f'/tag_translations/user', headers=headers)

    with allure.step("Check status code == 200 and empty"):
        assert get_translations_list.status_code == 200
        assert get_translations_list.text == "[]"

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)

        # delete_tag_translation = requests.delete(url=API_URL + f'/tag_translations/679ccd6cc26a88a5e294f870', headers=headers)
        #
        # assert delete_tag_translation.status_code == 204
