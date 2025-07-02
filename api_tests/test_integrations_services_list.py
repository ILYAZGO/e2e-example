from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from api_tests.common import *
import requests as r
import pytest
import allure


@pytest.mark.api
@allure.title("test_integrations_services_list")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("/integrations/services?detail=true")
def test_integrations_services_list():

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("Get gpt engines list"):
        headers = {'Authorization': user_token}

        get_services_list = r.get(url=API_URL + "/integrations/services?detail=true", headers=headers)

        count = sum(1 for item in get_services_list.json() if "service_name" in item) # total integrations count

    with allure.step("Check status code == 200 and list correct"):
        assert get_services_list.status_code == 200
        assert count == 48

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)