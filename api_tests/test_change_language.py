from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from api_tests.common import *
import requests as r
import pytest
import allure

langs = ["ru", "en", "es", "pt", "qq", "", " "]

@pytest.mark.api
@allure.title("test_change_lang_for_user")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_change_lang_for_user. parametrize. interface language")
@pytest.mark.parametrize("language", langs)
def test_change_lang_for_user(language):
    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("Get user info"):
        headers = {'Authorization': user_token}
        get_lang = r.get(url=API_URL + f"/user/me", headers=headers)

    with allure.step("Check language"):
        assert get_lang.json()["language"] == "ru"

    with allure.step("Change lang for user"):
        payload = {
            "id":f"{USER_ID}",
            "language":language
        }

        change_lang = r.patch(url=API_URL + f"/user/{USER_ID}", headers=headers, json=payload)

    with allure.step("Check status code == 204 or 403 if not valid"):
        if language == langs[4] or language == langs[6]:
            assert change_lang.status_code == 422
            assert change_lang.text == '{"detail":"Некорректный код языка пользователя"}'
        # elif language == langs[5]:  # 204 and lang and keep previous lang
        #     assert change_lang.status_code == 403
        else:
            assert change_lang.status_code == 204

    with allure.step("Get user info"):
        get_updated_lang = r.get(url=API_URL + f"/user/me", headers=headers)

    with allure.step("Check that language changed or keep old in not valid"):
        if language in [langs[4], langs[5], langs[6]]:
            assert get_updated_lang.json()["language"] == "ru"
        else:
            assert get_updated_lang.json()["language"] == language

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


