from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from api_tests.common import *
import requests as r
import pytest
import allure

@pytest.mark.api
@allure.title("test_get_all_translation_languages")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_get_translation_all_languages")
def test_get_all_translation_languages():

    laguages = [
        {
            "label": "Bulgarian",
            "value": "BG"
        },
        {
            "label": "Czech",
            "value": "CS"
        },
        {
            "label": "Danish",
            "value": "DA"
        },
        {
            "label": "German",
            "value": "DE"
        },
        {
            "label": "Greek",
            "value": "EL"
        },
        {
            "label": "English (British)",
            "value": "EN-GB"
        },
        {
            "label": "English (American)",
            "value": "EN-US"
        },
        {
            "label": "Spanish",
            "value": "ES"
        },
        {
            "label": "Estonian",
            "value": "ET"
        },
        {
            "label": "Finnish",
            "value": "FI"
        },
        {
            "label": "French",
            "value": "FR"
        },
        {
            "label": "Hungarian",
            "value": "HU"
        },
        {
            "label": "Indonesian",
            "value": "ID"
        },
        {
            "label": "Italian",
            "value": "IT"
        },
        {
            "label": "Japanese",
            "value": "JA"
        },
        {
            "label": "Korean",
            "value": "KO"
        },
        {
            "label": "Lithuanian",
            "value": "LT"
        },
        {
            "label": "Latvian",
            "value": "LV"
        },
        {
            "label": "Norwegian (Bokmål)",
            "value": "NB"
        },
        {
            "label": "Dutch",
            "value": "NL"
        },
        {
            "label": "Polish",
            "value": "PL"
        },
        {
            "label": "Portuguese (Brazilian)",
            "value": "PT-BR"
        },
        {
            "label": "Portuguese",
            "value": "PT-PT"
        },
        {
            "label": "Romanian",
            "value": "RO"
        },
        {
            "label": "Russian",
            "value": "RU"
        },
        {
            "label": "Slovak",
            "value": "SK"
        },
        {
            "label": "Slovenian",
            "value": "SL"
        },
        {
            "label": "Swedish",
            "value": "SV"
        },
        {
            "label": "Turkish",
            "value": "TR"
        },
        {
            "label": "Ukrainian",
            "value": "UK"
        },
        {
            "label": "Chinese",
            "value": "ZH"
        }
    ]

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("Get call_id from today's search calls"):
        headers = {'Authorization': user_token}


    with allure.step("Add comment to call"):
        get_languages = r.get(url=API_URL + '/translation/get_all_languages', headers=headers)

    with allure.step("Check status code == 200 and comment_id returned"):
        assert get_languages.status_code == 200
        assert get_languages.json() == laguages

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


