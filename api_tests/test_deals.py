#from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from api_tests.common import *
import requests as r
import pytest
import allure



@pytest.mark.api
@allure.title("test_search_all_deals")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_search_all_deals. Request like in interface.")
def test_search_all_deals():
    # backend have test deal_search_test.py later here we can make more checks
    with allure.step("Get token for user"):
        user_token = get_token(API_URL, ECOTELECOM, ECOPASS)

    with allure.step("Get call_id from today's search calls"):
        headers = {'Authorization': user_token}

    with allure.step("Search all deals for Ecotelecom"):
        get_all_deals = r.post(url=API_URL + "/deals/search?return_deal_info=true&skip=0&limit=50", headers=headers)
        json_all_deals = get_all_deals.json()

    with allure.step("Check"):
        assert get_all_deals.status_code == 200
        assert json_all_deals["total"] == 2169
        assert json_all_deals['found'] == 2169
        assert len(json_all_deals['dealIds']) == 50