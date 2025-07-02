from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from api_tests.common import *
import requests
import pytest
import allure


@pytest.mark.api
@allure.title("test_integrations_create_delete_api_token")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_integrations_create_delete_api_token")
def test_integrations_create_delete_api_token():

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD, upload_call=True)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("GET /api_keys status code==403 with ecotelecom user_id"):
        headers = {'Authorization': user_token}

        get_tokens = requests.get(url=API_URL + f'/user/{ecotelecom_id}/api_keys', headers=headers)

    with allure.step("Check status code == 403"):
        assert get_tokens.status_code == 403
        assert get_tokens.text == '{"detail":"Access to user denied"}'

    with allure.step("GET /api_keys status code==404 with fake_id"):
        get_tokens = requests.get(url=API_URL + f'/user/{fake_id}/api_keys', headers=headers)

    with allure.step("Check status code == 404"):
        assert get_tokens.status_code == 404
        assert get_tokens.text == '{"detail":"User not found"}'

    with allure.step("GET /api_keys status code==422 with fake_id[:10]"):
        get_tokens = requests.get(url=API_URL + f'/user/{fake_id[:10]}/api_keys', headers=headers)

    with allure.step("Check status code == 422"):
        assert get_tokens.status_code == 422
        assert "Value error, Not a valid ObjectId" in get_tokens.text

    with allure.step("GET /api_keys status code==200 with correct user_id"):
         get_tokens = requests.get(url=API_URL + f'/user/{USER_ID}/api_keys', headers=headers)

    with allure.step("Check status code == 200 and empty"):
        assert get_tokens.status_code == 200
        assert get_tokens.text == "[]"

    with allure.step("POST /api_key with ecotelecom user_id"):
        add_token = requests.post(url=API_URL + f'/user/{ecotelecom_id}/api_key', headers=headers)

    with allure.step("Check status code == 403"):
        assert add_token.status_code == 403
        assert add_token.text == '{"detail":"Access to user denied"}'

    with allure.step("POST /api_key with fake user_id"):
        add_token = requests.post(url=API_URL + f'/user/{fake_id}/api_key', headers=headers)

    with allure.step("Check status code == 404"):
        assert add_token.status_code == 404
        assert add_token.text == '{"detail":"User not found"}'

    with allure.step("POST /api_key with fake_id[:10] user_id"):
        add_token = requests.post(url=API_URL + f'/user/{fake_id[:10]}/api_key', headers=headers)

    with allure.step("Check status code == 422"):
        assert add_token.status_code == 422
        assert "Value error, Not a valid ObjectId" in add_token.text

    with allure.step("POST /api_key with correct user_id"):
        add_token = requests.post(url=API_URL + f'/user/{USER_ID}/api_key', headers=headers)
        api_token = add_token.text.replace('"', '')

    with allure.step("Check status code == 200 and we get api_token with 36 symbols"):
        assert add_token.status_code == 200
        assert len(api_token) == 36

#########
    with allure.step("GET /api_keys without correct user_id"):
         get_tokens = requests.get(url=API_URL + f'/user/{USER_ID}/api_keys', headers=headers)

    with allure.step("Check status code == 200 and have api_token in list"):
        assert get_tokens.status_code == 200
        assert api_token in get_tokens.text

#########
    with allure.step("DELETE /api_key/api_token with ecotelecom user_id"):
        delete_token = requests.delete(url=API_URL + f'/user/{ecotelecom_id}/api_key/{api_token}', headers=headers)

    with allure.step("Check status code == 403"):
        assert delete_token.status_code == 403
        assert delete_token.text == '{"detail":"Access to user denied"}'

    with allure.step("DELETE /api_key/api_token with fake user_id"):
        delete_token = requests.delete(url=API_URL + f'/user/{fake_id}/api_key/{api_token}', headers=headers)

    with allure.step("Check status code == 404"):
        assert delete_token.status_code == 404
        assert delete_token.text == '{"detail":"User not found"}'

    with allure.step("DELETE /api_key/api_token with fake_id[:10]"):
        delete_token = requests.delete(url=API_URL + f'/user/{fake_id[:10]}/api_key/{api_token}', headers=headers)

    with allure.step("Check status code == 422"):
        assert delete_token.status_code == 422
        assert "Value error, Not a valid ObjectId" in delete_token.text

    with allure.step("DELETE /api_key/api_token with correct user_id"):
        delete_token = requests.delete(url=API_URL + f'/user/{USER_ID}/api_key/{api_token}', headers=headers)

    with allure.step("Check status code == 204"):
        assert delete_token.status_code == 204

#########
    with allure.step("DELETE /api_key/api_token with correct user_id"):
        get_tokens = requests.get(url=API_URL + f'/user/{USER_ID}/api_keys', headers=headers)

    with allure.step("Check status code == 200 and empty"):
        assert get_tokens.status_code == 200
        assert get_tokens.text == "[]"

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)
