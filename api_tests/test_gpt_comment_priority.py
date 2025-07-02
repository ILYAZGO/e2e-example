import time
from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from api_tests.common import *
from utils.dates import *
import requests as r
import pytest
import allure

@pytest.mark.api
@allure.title("test_gpt_comment_priority")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_gpt_comment_priority")
def est_gpt_comment_priority():

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("Create gpt rule"):
        headers = {'Authorization': user_token}

        payload = {
            "engine":"imotio_gpt",
            "model":"auto",
            "assistantText":"",
            "entityType":"CALL",
            "temperature":"0.1",
            "title":"3comments",
            "simpleQuestions":[
                {"question":"short summary","tagName":"first","isComment":True,"isTag":False,"tagSeparators":"","priority":"1","yamlKey":""},
                {"question":"short summary","tagName":"second","isComment":True,"isTag":False,"tagSeparators":"","priority":"2","yamlKey":""},
                {"question":"short summary","tagName":"third","isComment":True,"isTag":False,"tagSeparators":"","priority":"3","yamlKey":""}
            ]
        }
        create_gpt_rule = r.post(url=API_URL + "/gpt/", headers=headers, json=payload)
        gpt_rule_id = create_gpt_rule.text.replace('"', '')

    with allure.step("Check that rule created"):
        assert create_gpt_rule.status_code == 200
        assert len(gpt_rule_id)  == 24

    with allure.step("Enable gpt rule"):
        enable = {"enabled":True}
        enable_rule = r.patch(url=API_URL + f"/gpt/{gpt_rule_id}", headers=headers, json=enable)

    with allure.step("Check gpt rule enabled"):
        assert enable_rule.status_code == 204

    with allure.step("Get gpt rules list"):
        get_gpt_rules_list = r.get(url=API_URL + "/gpt/", headers=headers)
        gpt_rules_list = get_gpt_rules_list.json()

    with allure.step("Check that rule in list"):
        assert get_gpt_rules_list.status_code == 200
        assert gpt_rule_id in gpt_rules_list[0]["id"]
        assert gpt_rules_list[0]["enabled"] == True
        assert gpt_rules_list[0]["isFree"] == False
        assert gpt_rules_list[0]["entityType"] == "CALL"

    with allure.step("Get call_id from created user"):
        get_calls = r.post(
            url=API_URL + f'/search_calls/?start_date={today.strftime("%Y-%m-%d")}&end_date={today.strftime("%Y-%m-%d")}',
            headers=headers)
        call_id = get_calls.json()["call_ids"][0].replace('"', '')

    with allure.step("Check status code == 200 and we get call_id in response"):
        assert get_calls.status_code == 200
        assert len(call_id) == 24

    with allure.step("Apply gpt rule to call"):
        data = {
            "start_date": today.strftime("%Y-%m-%d"),
            "end_date": today.strftime("%Y-%m-%d"),
            "action": "apply_gpt"
        }
        apply_gpt_rule = r.post(url=API_URL + "/calls/action", headers=headers, json=data)
        task_id = apply_gpt_rule.json()["task_id"]

    with allure.step("Check that status code == 200 and task created "):
        assert apply_gpt_rule.status_code == 200
        assert len(task_id) == 36

    with allure.step("Wait for 40 sec"):
        time.sleep(50)

    with allure.step("Get call"):
        get_call_comments = r.get(url=API_URL + f"/call/{call_id}", headers=headers)
        call_comments_list = get_call_comments.json()

    with allure.step("Check comments priority : first, second, third"):
        assert get_call_comments.status_code == 200
        assert len(call_comments_list["comments"]) == 3
        assert "first" in call_comments_list["comments"][0]["title"]
        assert "second" in call_comments_list["comments"][1]["title"]
        assert "third" in call_comments_list["comments"][2]["title"]

    with allure.step("Change rules priority"):
        update = {
            "simpleQuestions":
                [
                    {"question":"short summary","tagName":"first","isComment":True,"isTag":False,"tagSeparators":"","priority":"1000","yamlKey":""},
                    {"question":"short summary","tagName":"second","isComment":True,"isTag":False,"tagSeparators":"","priority":"999","yamlKey":""},
                    {"question":"short summary","tagName":"third","isComment":True,"isTag":False,"tagSeparators":"","priority":"998","yamlKey":""}
                ]
        }

        change_comments_priority = r.patch(url=API_URL + f"/gpt/{gpt_rule_id}", headers=headers, json=update)

    with allure.step("Check status code == 204"):
        assert change_comments_priority.status_code == 204

    with allure.step("Apply gpt rule to call"):
        data = {
            "start_date": today.strftime("%Y-%m-%d"),
            "end_date": today.strftime("%Y-%m-%d"),
            "action": "apply_gpt"
        }
        apply_gpt_rule = r.post(url=API_URL + "/calls/action", headers=headers, json=data)
        task_id = apply_gpt_rule.json()["task_id"]

    with allure.step("Check status code == 200 and task created"):
        assert apply_gpt_rule.status_code == 200
        assert len(task_id) == 36

    with allure.step("Wait for 20 sec"):
        time.sleep(25)

    with allure.step("Check call comments"):
        get_call_comments = r.get(url=API_URL + f"/call/{call_id}", headers=headers)
        call_comments_list = get_call_comments.json()

    with allure.step("Check comments priority changed: third, second, first"):
        assert get_call_comments.status_code == 200
        assert len(call_comments_list["comments"]) == 3
        assert "third" in call_comments_list["comments"][0]["title"]
        assert "second" in call_comments_list["comments"][1]["title"]
        assert "first" in call_comments_list["comments"][2]["title"]

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)