from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from api_tests.common import *
from utils.dates import *
import requests as r
import pytest
import allure

# all langs
# langs = ["BG", "CS", "DA", "DE", "EL", "EN-GB", "EN-US", "ES", "ET", "FI", "FR", "HU", "ID", "IT", "JA", "KO", "LT",
#          "LV","NB", "NL", "PL", "PT-BR", "PT-PT", "RO", "RU", "SK", "SL", "SV", "TR", "UK", "ZH", "qq", ""]

# necessary langs
langs = ["EN-GB", "EN-US", "ES", "PT-BR", "PT-PT", "RU", "qq", ""]


@pytest.fixture(scope="module")  # Фикстура выполняется 1 раз на весь модуль
def setup_user():
    with allure.step("Create user (once for all tests)"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD, upload_call=True)
        user_token = get_token(API_URL, LOGIN, PASSWORD)
        yield USER_ID, TOKEN, LOGIN, user_token  # Возвращаем данные для тестов
    with allure.step("Delete user (after all tests)"):
        delete_user(API_URL, TOKEN, USER_ID)

@pytest.mark.api
@allure.title("test_translate_communication_comment")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_translate_communication_comment")
@pytest.mark.parametrize("language", langs)
def test_translate_communication_comment(language, setup_user):
    USER_ID, TOKEN, LOGIN, user_token = setup_user  # Распаковываем фикстуру

    with allure.step("Get call_id from today's search calls"):
        headers = {'Authorization': user_token}

        get_calls = r.post(url=API_URL + f'/search_calls/?start_date={today.strftime("%Y-%m-%d")}&end_date={today.strftime("%Y-%m-%d")}', headers=headers)
        call_id = get_calls.json()["call_ids"][0].replace('"', '')

    with allure.step("Check status code == 200 and we get call_id in response"):
        assert get_calls.status_code == 200
        assert len(call_id) == 24

    with allure.step("Add comment to call"):
        comment = {"call":call_id.capitalize(),"title":"яблоко","message":"яблоко","isPrivate":False}
        add_comment = r.post(url=API_URL + '/comment/', headers=headers, json=comment)
        comment_id = add_comment.text.replace('"', '')

    with allure.step("Check status code == 200 and comment_id returned"):
        assert add_comment.status_code == 200
        assert len(comment_id) == 24

    with allure.step("Translate comment"):
        translate_comment = r.get(url=API_URL + f'/comment/{comment_id}/translate?language={language}', headers=headers)
        translation_json = translate_comment.json()

    with allure.step("Check that translated"):
        if language in {"qq", ""}:
            assert translate_comment.status_code == 422
            assert translation_json == {"detail":"Invalid language"}
        else:
            assert translate_comment.status_code == 200
            assert translation_json["comment"] == comment_id
            assert translation_json["language"] == language
            assert translation_json["translatedTitle"] == translation_json["translatedMessage"]
            assert len(translation_json["translatedTitle"]) > 0
            assert len(translation_json["translatedMessage"]) > 0








# @pytest.mark.api
# @allure.title("test_translate_communication_comment")
# @allure.severity(allure.severity_level.NORMAL)
# @allure.description("test_translate_communication_comment")
# @pytest.mark.parametrize("language", langs)
# def test_translate_communication_comment(language):
#     with allure.step("Create user"):
#         USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD, upload_call=True)
#
#     with allure.step("Get token for user"):
#         user_token = get_token(API_URL, LOGIN, PASSWORD)
#
#     with allure.step("Get call_id from today's search calls"):
#         headers = {'Authorization': user_token}
#
#         get_calls = r.post(url=API_URL + f'/search_calls/?start_date={today.strftime("%Y-%m-%d")}&end_date={today.strftime("%Y-%m-%d")}', headers=headers)
#         call_id = get_calls.json()["call_ids"][0].replace('"', '')
#
#     with allure.step("Check status code == 200 and we get call_id in response"):
#         assert get_calls.status_code == 200
#         assert len(call_id) == 24
#
#     with allure.step("Add comment to call"):
#         comment = {"call":call_id.capitalize(),"title":"яблоко","message":"яблоко","isPrivate":False}
#         add_comment = r.post(url=API_URL + '/comment/', headers=headers, json=comment)
#         comment_id = add_comment.text.replace('"', '')
#
#     with allure.step("Check status code == 200 and comment_id returned"):
#         assert add_comment.status_code == 200
#         assert len(comment_id) == 24
#
#     with allure.step("Translate comment"):
#         translate_comment = r.get(url=API_URL + f'/comment/{comment_id}/translate?language={language}', headers=headers)
#         translation_json = translate_comment.json()
#
#     with allure.step("Check that translated"):
#         if language in {"qq", " ", ""}:
#             assert translate_comment.status_code == 422
#             assert translation_json == {"detail":"Invalid language"}
#         else:
#             assert translate_comment.status_code == 200
#             assert translation_json["comment"] == comment_id
#             assert translation_json["language"] == language
#             assert translation_json["translatedTitle"] == translation_json["translatedMessage"]
#             assert len(translation_json["translatedTitle"]) > 2
#             assert len(translation_json["translatedMessage"]) > 2
#
#     with allure.step("Delete user"):
#         delete_user(API_URL, TOKEN, USER_ID)


