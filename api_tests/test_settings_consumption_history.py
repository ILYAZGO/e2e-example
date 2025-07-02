from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from utils.dates import *
from api_tests.common import get_token
import requests as r
import pytest
import allure

consumption = ["calls", "gpt", "chats"]

@pytest.mark.api
@allure.title("test_check_consumption_history")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_check_consumption_history. Check that requests working")
@pytest.mark.parametrize("consumption_type", consumption)
def test_check_consumption_history(consumption_type):

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("Get consumption history without dates"):
        headers = {'Authorization': user_token}
        url_for_test = API_URL + f'/user/{USER_ID}/history/{consumption_type}'
        get_consumption_history_without_dates = r.get(url=url_for_test, headers=headers)

    with allure.step("Check status code == 200"):
        assert get_consumption_history_without_dates.status_code == 200

    with allure.step("Get consumption history with default date"):
        start_date = first_day_this_month.strftime("%Y-%m-%d")
        end_date = last_day_this_month.strftime("%Y-%m-%d")
        url_for_test = API_URL + f'/user/{USER_ID}/history/{consumption_type}?start_date={start_date}&end_date={end_date}'

        get_consumption_history_default = r.get(url=url_for_test, headers=headers)

    with allure.step("Check status code == 200"):
        assert get_consumption_history_default.status_code == 200

    with allure.step("Get consumption history with changed for today date"):
        start_date = today.strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
        url_for_test = API_URL + f'/user/{USER_ID}/history/{consumption_type}?start_date={start_date}&end_date={end_date}'

        get_consumption_history_changed = r.get(url=url_for_test, headers=headers)

    with allure.step("Check status code == 200"):
        assert get_consumption_history_changed.status_code == 200

    with allure.step("Get consumption history for absent user"):
        absent_user_id = "123456789012345678901234"
        url_for_test = API_URL + f'/user/{absent_user_id}/history/{consumption_type}?start_date={start_date}&end_date={end_date}'

        get_consumption_history_absent_user = r.get(url=url_for_test, headers=headers)

    with allure.step("Check status code == 404"):
        assert get_consumption_history_absent_user.status_code == 404
        assert get_consumption_history_absent_user.text == '{"detail":"User not found"}'

    with allure.step("Get consumption history with changed date"):
        start_date = absent_user_id
        end_date = last_day_this_month.strftime("%Y-%m-%d")
        url_for_test = API_URL + f'/user/{USER_ID}/history/{consumption_type}?start_date={start_date}&end_date={end_date}'

        get_consumption_history_broken = r.get(url=url_for_test, headers=headers)

    with allure.step("Check status code == 422"):
        assert get_consumption_history_broken.status_code == 422

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)