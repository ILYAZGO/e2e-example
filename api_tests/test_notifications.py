from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from api_tests.common import *
import requests as r
import pytest
import allure

available_directions = ["Telegram","Email","API"]

@pytest.mark.api
@allure.title("test_create_update_delete_email_notification_rule")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_create_update_delete_email_notification_rule")
def test_create_update_delete_email_notification_rule():
    rule_name = "auto_api_test_email"
    direction = available_directions[1]

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("Get call_id from today's search calls"):
        headers = {'Authorization': user_token}

    with allure.step("Get available directions"):
        get_available_directions = r.get(url=API_URL + "/notify_rules/available_directions", headers=headers)

    with allure.step("Check available directions status code == 200 and list"):
        assert get_available_directions.status_code == 200
        assert get_available_directions.json() == available_directions

    with allure.step("Check notify rule variables"):
        get_notify_rule_variables = r.get(url=API_URL + "/notify_rules/notify_rule_variables", headers=headers)
        json_get_notify_rule_variables = get_notify_rule_variables.json()

    with allure.step("Check status code == 200 and content"):
        expected_keys_call_vars = {
            'call_id', 'duration', 'public_link_old', 'link_old', 'get_stt_json()', 'public_link_new',
            'call_min_points', 'conversation_id', 'json()', 'public_link', 'operator_phone', 'call_max_points',
            'get_all_text(1000)', "get_fragments('tag_name', 2, 2)", 'call_time', 'link', 'call_timestamp',
            'client_phone', 'unique_id', 'link_new', 'call_points', 'in_line()'
        }
        expected_keys_descriptions = {
            'unique_id', 'client_phone', 'call_points', 'json()', 'call_min_points', 'get_all_text(1000)', 'in_line()',
            'call_id', "get_fragments('tag_name', 2, 2)", 'duration', 'operator_phone', 'link', 'public_link',
            'get_stt_json()', 'call_timestamp', 'call_max_points', 'call_time', 'conversation_id'
        }

        actual_keys_call_vars = set(json_get_notify_rule_variables["call_vars"].keys())
        actual_keys_descriptions = set(json_get_notify_rule_variables["descriptions"].keys())

        assert get_notify_rule_variables.status_code == 200
        assert json_get_notify_rule_variables["call_vars"]
        assert json_get_notify_rule_variables["descriptions"]
        assert actual_keys_call_vars == expected_keys_call_vars
        assert actual_keys_descriptions == expected_keys_descriptions

    with allure.step("Get notify rules empty list "):
        get_notify_rules_list = r.get(url=API_URL + "/notify_rules/", headers=headers)

        assert get_notify_rules_list.status_code == 200
        assert get_notify_rules_list.text == "[]"

    ####
    with allure.step("GET /notify_rules/ empty with fake ?rule_owner"):
        get_notify_rules_list = r.get(url=API_URL + f'/notify_rules/?rule_owner={fake_id}', headers=headers)

    with allure.step("Check status code == 404 and Setting rule_owner not allowed"):
        assert get_notify_rules_list.status_code == 403
        assert get_notify_rules_list.text == '{"detail":"Setting rule_owner not allowed"}'

    with allure.step("GET /notify_rules/ empty with ecotelecom ?rule_owner"):
        get_notify_rules_list = r.get(url=API_URL + f'/notify_rules/?rule_owner={ecotelecom_id}', headers=headers)

    with allure.step("Check status code == 403 and Setting rule_owner not allowed"):
        assert get_notify_rules_list.status_code == 403
        assert get_notify_rules_list.text == '{"detail":"Setting rule_owner not allowed"}'

    with allure.step("GET /notify_rules/ empty with broken ?rule_owner"):
        get_notify_rules_list = r.get(url=API_URL + f'/notify_rules/?rule_owner={fake_id[:10]}', headers=headers)

    with allure.step("Check status code == 422 and empty"):
        assert get_notify_rules_list.status_code == 422
        assert "Value error, Not a valid ObjectId" in get_notify_rules_list.text
######
    with allure.step("Create email notify rule"):
        rule_payload = {
            "owner":USER_ID,
            "title":rule_name,
            "enabled":True,
            "cloneParent":"",
            "activeTgChats":[],
            "tgBody":"",
            "tgAudio":False,
            "emailDst":rule_name,
            "emailSubject":"auto_api_test_email_subject",
            "emailBody":rule_name,
            "apiUrl":"",
            "apiMethod":"",
            "apiResend":False,
            "allowOwerwriteFields":False,
            "apiHeaders":"",
            "apiBody":"",
            "amoNotifyEnabled":True,
            "amoBody":"",
            "amoContactFields":{},
            "amoLeadFields":{},
            "bitrixContactFields":{},
            "bitrixLeadFields":{},
            "bitrixDealFields":{},
            "bitrixBody":"",
            "bitrixNotificationDirection":"",
            "globalFilter":{
                "title":rule_name,
                "items":[{"key":"search_by_tags","logic":"and","complexValues":[{"name":"auto_rule"}]}]},
            "direction":direction}

        create_notify_rule = r.post(url=API_URL + "/notify_rules/", headers=headers, json=rule_payload)
        notify_rule_id = create_notify_rule.text.replace('"', '')

    with allure.step("Check status code == 200 and rule_id in response"):
        assert create_notify_rule.status_code == 200
        assert len(notify_rule_id) == 24

    with allure.step("Get notify rules list with created notify rule"):
        get_notify_rules_list = r.get(url=API_URL + "/notify_rules/", headers=headers)

        rule_description = [
            {
                "id":notify_rule_id,
                "owner":USER_ID,
                "title":rule_name,
                "enabled":True,
                "cloneParent":None,
                "direction":direction
            }
        ]

        assert get_notify_rules_list.status_code == 200
        assert get_notify_rules_list.json() == rule_description

    with allure.step("Update notify rule"):
        rule_payload["title"] = "updated_title"
        rule_payload["apiMethod"] = "POST"
        update_notify_rule = r.put(url=API_URL + f"/notify_rules/{notify_rule_id}", headers=headers, json=rule_payload)

    with allure.step("Check status code == 204"):
        assert update_notify_rule.status_code == 204

    with allure.step("Get notify rules list with updated value"):
        get_notify_rules_list = r.get(url=API_URL + "/notify_rules/", headers=headers)

        rule_description_updated = [
            {
                "id": notify_rule_id,
                "owner": USER_ID,
                "title": "updated_title",
                "enabled": True,
                "cloneParent": None,
                "direction": direction
            }
        ]

        assert get_notify_rules_list.status_code == 200
        assert get_notify_rules_list.json() == rule_description_updated

    with allure.step("Delete notify rule"):
        delete_notify_rule = r.delete(url=API_URL + f"/notify_rules/{notify_rule_id}", headers=headers)

    with allure.step("Check status code == 204"):
        assert delete_notify_rule.status_code == 204

    with allure.step("Get empty notify rules list"):
        get_notify_rules_list = r.get(url=API_URL + "/notify_rules/", headers=headers)

        assert get_notify_rules_list.status_code == 200
        assert get_notify_rules_list.text == "[]"

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)