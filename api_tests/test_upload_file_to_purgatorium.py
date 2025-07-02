from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from api_tests.common import get_token
import requests as r
import pytest
import allure
import os

@pytest.mark.api
@allure.title("test_upload_file_to_purgatorium")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_upload_file_to_purgatorium")
def test_upload_file_to_purgatorium():
    purgatorium="unique"

    filename = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audio/stereo.opus")

    files = {"fileobject": ("stereo.opus", open(filename, 'rb'), 'audio/opus')}

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)
        headers = {'Authorization': user_token}

    with allure.step("Get empty list"):
        get_files_list = r.get(url=API_URL + f"/uploads?purgatorium={purgatorium}", headers=headers)

    with allure.step("Check that list empty"):
        assert get_files_list.status_code == 200
        assert get_files_list.text == "[]"

    with allure.step("Upload file to purgatorium"):
        upload_file_to_purgatorium = r.post(url=API_URL + f"/upload?purgatorium={purgatorium}", headers=headers, files=files)
        filepath = upload_file_to_purgatorium.text.replace('"', '')

    with allure.step("Check that file uploaded"):
        assert upload_file_to_purgatorium.status_code == 200
        assert USER_ID in upload_file_to_purgatorium.text
        assert len(filepath) == 73

    with allure.step("Get list"):
        get_files_list = r.get(url=API_URL + f"/uploads?purgatorium={purgatorium}", headers=headers)

    with allure.step("Check that list empty"):
        assert get_files_list.status_code == 200
        assert filepath in get_files_list.text

    with allure.step("Delete file"):
        delete_file = r.delete(url=API_URL + f"/upload?purgatorium={purgatorium}&remote_path={filepath}", headers=headers)

    with allure.step("Check"):
        assert delete_file.status_code == 204

    with allure.step("Get empty list"):
        get_files_list = r.get(url=API_URL + f"/uploads?purgatorium={purgatorium}", headers=headers)

    with allure.step("Check that list empty"):
        assert get_files_list.status_code == 200
        assert get_files_list.text == "[]"

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)