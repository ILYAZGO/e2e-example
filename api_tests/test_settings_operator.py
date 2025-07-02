from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from api_tests.common import get_token
import requests
import pytest
import allure
from datetime import datetime


@pytest.mark.api
@allure.title("test_create_update_delete_employee_positive")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_create_update_delete_employee_positive")
def test_create_update_delete_operator_positive():
    NEW_OPERATOR_LOGIN = f"auto_test_operator_{datetime.now().strftime('%m%d%H%M')}_{datetime.now().microsecond}"
    CHANGED_OPERATOR_LOGIN = f"auto_test_operator_changed{datetime.now().strftime('%m%d%H%M')}_{datetime.now().microsecond}"
    EMAIL = f"mail{datetime.now().microsecond}@mail.ru"
    CHANGED_EMAIL = f"{datetime.now().microsecond}mail@mail.ru"

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)
        headers = {'Authorization': user_token}

    with allure.step("Create operator with not valid email by user"):
        json = {
            "role":"operator",
            "login":NEW_OPERATOR_LOGIN,
            "name":NEW_OPERATOR_LOGIN,
            "email":NEW_OPERATOR_LOGIN,
            "password":PASSWORD,
            "comment":NEW_OPERATOR_LOGIN,
            "parentUser":USER_ID,
            "phoneNumber":NEW_OPERATOR_LOGIN
        }

        create_operator = requests.post(url=API_URL + "/user", headers=headers, json=json)
        #operator_id = create_operator.text.replace('"', '')

    with allure.step("Check status code == 422"):
        assert create_operator.status_code == 422
        assert create_operator.text == '{"detail":"Некорректный email"}'

    with allure.step("Create operator with not valid email by user"):
        json = {
            "role":"operator",
            "login":NEW_OPERATOR_LOGIN,
            "name":NEW_OPERATOR_LOGIN,
            "email":EMAIL,
            "password":PASSWORD,
            "comment":NEW_OPERATOR_LOGIN,
            "parentUser":USER_ID,
            "phoneNumber":NEW_OPERATOR_LOGIN
        }

        create_operator = requests.post(url=API_URL + "/user", headers=headers, json=json)
        operator_id = create_operator.text.replace('"', '')

    with allure.step("Check status code == 200 and we get operator_id in response"):
        assert create_operator.status_code == 200
        assert len(operator_id) == 24 # check len of created operator id with "

    with allure.step("Get operators list"):
        get_operators = requests.get(url=API_URL + f"/user/{USER_ID}/operators", headers=headers)

    with allure.step("Check status code == 200 and json is correct"):
        json_operators = [
            {
                "id": operator_id,
                "role": "operator",
                "login": NEW_OPERATOR_LOGIN,
                "name": NEW_OPERATOR_LOGIN,
                "timezone": "Europe/Moscow",
                "parentUser": USER_ID,
                "createdBy": USER_ID,
                "partner": None,
                "industry": None,
                "comment": NEW_OPERATOR_LOGIN,
                "useBilling": False,
                "lanbillingInfo": None,
                "email": EMAIL,
                "phoneNumber": NEW_OPERATOR_LOGIN,
                "password": None,
                "makeDeals": False,
                "language": "ru",
                "sttOptions": None,
                "defaultSttOptions": {},
                "sttLanguage": None,
                "enableGpt": None,
                "publicLinkAge": None,
                "excludedGrammarRuleList": [],
                "excludedGrammarRuleCategoryList": []
            }
        ]

        assert get_operators.status_code == 200
        assert get_operators.json() == json_operators

    with allure.step("Change operator info"):
        json_for_change = {
            "id":operator_id,
            "role":"operator",
            "login":NEW_OPERATOR_LOGIN,   #user cant change login for operator
            "name":CHANGED_OPERATOR_LOGIN,
            "timezone":"",
            "email":CHANGED_EMAIL,
            "phoneNumber":CHANGED_OPERATOR_LOGIN,
            "password":PASSWORD,
            "comment":CHANGED_OPERATOR_LOGIN,
            "language":"ru",
            "industry":"",
            "partner":"",
            "useBilling":False,
            "lanbillingInfo":None}

        patch_operator = requests.patch(url=API_URL + f"/user/{operator_id}", headers=headers, json=json_for_change)

    with allure.step("Check that operator updated"):
        assert patch_operator.status_code == 204

    with allure.step("Get operators list"):
        get_operators = requests.get(url=API_URL + f"/user/{USER_ID}/operators", headers=headers)

    with allure.step("Check status code == 200 and json is correct"):
        json_operators_after_change = [
            {
                "id": operator_id,
                "role": "operator",
                "login": NEW_OPERATOR_LOGIN,
                "name": CHANGED_OPERATOR_LOGIN,
                "timezone": "Europe/Moscow",
                "parentUser": USER_ID,
                "createdBy": USER_ID,
                "partner": None,
                "industry": None,
                "comment": CHANGED_OPERATOR_LOGIN,
                "useBilling": False,
                "lanbillingInfo": None,
                "email": CHANGED_EMAIL,
                "phoneNumber": CHANGED_OPERATOR_LOGIN,
                "password": None,
                "makeDeals": False,
                "language": "ru",
                "sttOptions": None,
                "defaultSttOptions": {},
                "sttLanguage": None,
                "enableGpt": None,
                "publicLinkAge": None,
                "excludedGrammarRuleList": [],
                "excludedGrammarRuleCategoryList": []
            }
        ]

        assert get_operators.status_code == 200
        assert get_operators.json() == json_operators_after_change


    with allure.step("Delete created operator"):
        delete_operator = requests.delete(url=API_URL + f"/user/{operator_id}", headers=headers)

    with allure.step("Check status code == 204"):
        assert delete_operator.status_code == 204

    with allure.step("Get operators list"):
        get_operators = requests.get(url=API_URL + f"/user/{USER_ID}/operators", headers=headers)

    with allure.step("Check status code == 200"):
        assert get_operators.status_code == 200
        assert get_operators.text == "[]"

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.api
@allure.title("test_give_take_report_to_from_operator")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_give_take_report_to_from_operator")
def test_give_take_report_to_from_operator():
    NEW_OPERATOR_LOGIN = f"auto_test_operator_{datetime.now().strftime('%m%d%H%M')}_{datetime.now().microsecond}"

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD, create_report=True)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("Create operator by user"):
        headers = {'Authorization': user_token}

        json = {
            "role":"operator",
            "login":NEW_OPERATOR_LOGIN,
            "name":NEW_OPERATOR_LOGIN,
            "email":"",
            "password":PASSWORD,
            "comment":"",
            "parentUser":USER_ID,
            "phoneNumber":""
        }

        create_operator = requests.post(url=API_URL + "/user", headers=headers, json=json)
        operator_id = create_operator.text.replace('"', '')

    with allure.step("Check status code == 200 and we get operator_id in response"):
        assert create_operator.status_code == 200
        assert len(operator_id) == 24 # check len of created operator id with "

    with allure.step("Get all reports that we can give to operator"):
        get_all_reports = requests.get(url=API_URL + f"/user/{operator_id}/all_reports", headers=headers)
        report_id = get_all_reports.json()[0]["id"]

    with allure.step("Check status code == 200 and report_id, name and other params is null"):
        assert get_all_reports.status_code == 200
        assert len(report_id) == 24
        assert "auto_test_report" in get_all_reports.json()[0]["name"]
        assert get_all_reports.json()[0]["period"] is None
        assert get_all_reports.json()[0]["from_dt"] is None
        assert get_all_reports.json()[0]["to_dt"] is None
        assert get_all_reports.json()[0]["notification_status"] is None

    with allure.step("Get operators reports"):
        get_report_limitation = requests.get(url=API_URL + f"/user/{operator_id}/report_limitation", headers=headers)

    with allure.step("Check status code == 200 and no given reports"):
        assert get_all_reports.status_code == 200
        assert get_report_limitation.text == "[]"

    with allure.step("Give report to operator"):
        give_report_to_operator = requests.put(url=API_URL + f"/user/{operator_id}/report_limitation", headers=headers, data=f'["{report_id}"]')

    with allure.step("Check status code == 204 and no text"):
        assert give_report_to_operator.status_code == 204
        assert give_report_to_operator.text == ""

    with allure.step("Get list of given reports"):
        get_report_limitation = requests.get(url=API_URL + f"/user/{operator_id}/report_limitation", headers=headers)

    with allure.step("Check status code == 200 and response have report_id"):
        assert get_all_reports.status_code == 200
        assert report_id in get_report_limitation.text

    with allure.step("Take report from operator"):
        take_report_from_operator = requests.put(url=API_URL + f"/user/{operator_id}/report_limitation", headers=headers, data="[]")

    with allure.step("Check status code == 204 and no text"):
        assert take_report_from_operator.status_code == 204
        assert take_report_from_operator.text == ""

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)