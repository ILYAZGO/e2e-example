from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from api_tests.common import *
from utils.dates import *
import requests as r
import pytest
import allure

@pytest.mark.api
@allure.title("test_add_update_delete_communication_comment")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_add_update_delete_communication_comment")
def test_add_update_delete_communication_comment():
    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD, upload_call=True)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("Get call_id from today's search calls"):
        headers = {'Authorization': user_token}

        get_calls = r.post(url=API_URL + f'/search_calls/?start_date={today.strftime("%Y-%m-%d")}&end_date={today.strftime("%Y-%m-%d")}', headers=headers)
        call_id = get_calls.json()["call_ids"][0].replace('"', '')

    with allure.step("Check status code == 200 and we get call_id in response"):
        assert get_calls.status_code == 200
        assert len(call_id) == 24

    with allure.step("Add comment to call"):
        comment = {"call":call_id.capitalize(),"title":"test_comment","message":"test_comment_text","isPrivate":False}
        add_comment = r.post(url=API_URL + '/comment/', headers=headers, json=comment)
        comment_id = add_comment.text.replace('"', '')

    with allure.step("Check status code == 200 and comment_id returned"):
        assert add_comment.status_code == 200
        assert len(comment_id) == 24

    with allure.step("Get comment from call"):
        get_comment = r.get(url=API_URL + f'/call/{call_id}?split_tag_info=true', headers=headers)
        get_comment_json = get_comment.json()

    with allure.step("Check comment"):
        assert get_comment.status_code == 200
        assert get_comment_json["comments"][0]["id"] == comment_id
        assert get_comment_json["comments"][0]["call"] == call_id.lower()
        assert get_comment_json["comments"][0]["fragment"] is None
        assert get_comment_json["comments"][0]["deal"] is None
        assert get_comment_json["comments"][0]["title"] == "test_comment"
        assert get_comment_json["comments"][0]["message"] == "test_comment_text"
        assert get_comment_json["comments"][0]["creator"] == USER_ID
        assert get_comment_json["comments"][0]["creatorName"] == LOGIN
        assert get_comment_json["comments"][0]["editor"] is None
        assert get_comment_json["comments"][0]["editorName"] is None
        assert get_comment_json["comments"][0]["rule"] is None
        assert get_comment_json["comments"][0]["isPrivate"] == False
        assert today.strftime("%Y-%m-%d") in get_comment_json["comments"][0]["addTime"]
        assert get_comment_json["comments"][0]["editTime"] is None
        assert get_comment_json["comments"][0]["owner"] == USER_ID
        assert get_comment_json["comments"][0]["priority"] == 0

    with allure.step("Update comment"):
        comment_update = {"title":"test_comment_update","message":"test_comment_text_update", "isPrivate":True}
        add_comment = r.patch(url=API_URL + f'/comment/{comment_id}', headers=headers, json=comment_update)

    with allure.step("Check status code == 204"):
        assert add_comment.status_code == 204

    with allure.step("Get comment from call"):
        get_comment = r.get(url=API_URL + f'/call/{call_id}?split_tag_info=true', headers=headers)
        get_comment_json = get_comment.json()

    with allure.step("Check comment"):
        assert get_comment.status_code == 200
        assert get_comment_json["comments"][0]["id"] == comment_id
        assert get_comment_json["comments"][0]["call"] == call_id.lower()
        assert get_comment_json["comments"][0]["fragment"] is None
        assert get_comment_json["comments"][0]["deal"] is None
        assert get_comment_json["comments"][0]["title"] == "test_comment_update"
        assert get_comment_json["comments"][0]["message"] == "test_comment_text_update"
        assert get_comment_json["comments"][0]["creator"] == USER_ID
        assert get_comment_json["comments"][0]["creatorName"] == LOGIN
        assert get_comment_json["comments"][0]["editor"] == USER_ID
        assert get_comment_json["comments"][0]["editorName"] == LOGIN
        assert get_comment_json["comments"][0]["rule"] is None
        assert get_comment_json["comments"][0]["isPrivate"] == True
        assert today.strftime("%Y-%m-%d") in get_comment_json["comments"][0]["addTime"]
        assert today.strftime("%Y-%m-%d") in get_comment_json["comments"][0]["editTime"]
        assert get_comment_json["comments"][0]["owner"] == USER_ID
        assert get_comment_json["comments"][0]["priority"] == 0

    with allure.step("Delete comment"):
        delete_comment = r.delete(url=API_URL + f'/comment/{comment_id}', headers=headers)

    with allure.step("Check status code == 204"):
        assert delete_comment.status_code == 204

    with allure.step("Get comment from call"):
        get_comment = r.get(url=API_URL + f'/call/{call_id}?split_tag_info=true', headers=headers)
        get_comment_json = get_comment.json()

    with allure.step("Check comment"):
        assert get_comment.status_code == 200
        assert get_comment_json["comments"] == []

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


