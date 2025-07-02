from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from api_tests.common import *
import requests as r
import pytest
import allure


gpt_engines = ["chat_gpt","yandex_gpt","imotio_gpt"]

chat_gpt = {
    "$defs": {
        "ChatGPTModel": {
            "enum": [
                "auto",
                "chatgpt-4o-latest",
                "gpt-4.1",
                "gpt-4.1-mini",
                "gpt-4.1-nano",
                "gpt-4o",
                "gpt-4o-mini",
                "o1",
                "o3-mini",
                "o4-mini",
            ],
            "title": "ChatGPTModel",
            "type": "string"
        }
    },
    "properties": {
        "model": {
            "$ref": "#/$defs/ChatGPTModel",
            "default": "auto"
        },
        "temperature": {
            "default": 0,
            "maximum": 2.0,
            "minimum": 0.0,
            "title": "Temperature",
            "type": "number"
        },
        "frequency_penalty": {
            "default": 0,
            "maximum": 2.0,
            "minimum": -2.0,
            "title": "Frequency Penalty",
            "type": "number"
        },
        "presence_penalty": {
            "default": 0,
            "maximum": 2.0,
            "minimum": -2.0,
            "title": "Presence Penalty",
            "type": "number"
        }
    },
    "title": "ChatGPTOptions",
    "type": "object"
}

yandex_gpt = {
    "$defs": {
        "YandexGPTModel": {
            "enum": [
                # "summarization",
                "yandexgpt",
                "yandexgpt-lite"
            ],
            "title": "YandexGPTModel",
            "type": "string"
        }
    },
    "properties": {
        "model": {
            "$ref": "#/$defs/YandexGPTModel",
            "default": "yandexgpt-lite"
        },
        "temperature": {
            "default": 0,
            "maximum": 1.0,
            "minimum": 0.0,
            "title": "Temperature",
            "type": "number"
        }
    },
    "title": "YandexGPTOptions",
    "type": "object"
}

imotio_gpt = {
    "$defs": {
        "VLLMModel": {
            "enum": [
                "auto"
            ],
            "title": "VLLMModel",
            "type": "string"
        }
    },
    "properties": {
        "model": {
            "$ref": "#/$defs/VLLMModel",
            "default": "auto"
        },
        "temperature": {
            "default": 0,
            "maximum": 0.4,
            "minimum": 0.0,
            "title": "Temperature",
            "type": "number"
        },
        "frequency_penalty": {
            "default": 0,
            "maximum": 2.0,
            "minimum": -2.0,
            "title": "Frequency Penalty",
            "type": "number"
        },
        "presence_penalty": {
            "default": 0,
            "maximum": 2.0,
            "minimum": -2.0,
            "title": "Presence Penalty",
            "type": "number"
        },
        "top_k": {
            "default": -1,
            "maximum": 50.0,
            "minimum": -1.0,
            "title": "Top K",
            "type": "number"
        },
    },
    "title": "VLLMOptions",
    "type": "object"
}


@pytest.mark.api
@allure.title("test_gpt_engine_selectors")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_gpt_engine_selectors")
def test_gpt_engine_selectors():

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("Get gpt engines list"):
        headers = {'Authorization': user_token}

        get_gpt_engine_selectors = r.get(url=API_URL + "/gpt/gpt_engine_selectors", headers=headers)

    with allure.step("Check status code == 200 and list correct"):
        assert get_gpt_engine_selectors.status_code == 200
        assert get_gpt_engine_selectors.json() == gpt_engines

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)

@pytest.mark.api
@allure.title("test_gpt_engine_selectors")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_gpt_engine_selectors")
@pytest.mark.parametrize("gpt_engine", gpt_engines)
def test_gpt_options(gpt_engine):

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("Get options for engine"):
        headers = {'Authorization': user_token}

        get_gpt_engine_selectors = r.get(url=API_URL + f"/gpt/{gpt_engine}/gpt_options", headers=headers)

    with allure.step("Chck status code ==200 and json with options is correct for engine"):
        assert get_gpt_engine_selectors.status_code == 200

        if gpt_engine == "chat_gpt":
            assert get_gpt_engine_selectors.json() == chat_gpt
        elif gpt_engine == "yandex_gpt":
            assert get_gpt_engine_selectors.json() == yandex_gpt
        else:
            assert get_gpt_engine_selectors.json() == imotio_gpt

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)