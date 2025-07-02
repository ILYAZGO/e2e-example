from utils.create_delete_user import create_user, delete_user
from utils.variables import *
from api_tests.common import *
import requests
import pytest
import allure


@pytest.mark.api
@allure.title("test_create_update_delete_check_list")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_create_update_delete_check_list")
def test_create_update_delete_check_list():

    check_list_title = "auto_api_check_list"

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("GET /checklists/ empty without ?rule_owner"):
        headers = {'Authorization': user_token}

        get_checklists = requests.get(url=API_URL + "/checklists/", headers=headers)

    with allure.step("Check status code == 200 and have default checklist"):
        assert get_checklists.status_code == 200
        response_data = get_checklists.json()

        assert len(response_data) == 1
        checklist = response_data[0]

        # checking default check list without id. id is unique for every check list
        assert checklist["owner"] == USER_ID
        assert checklist["enabledUsers"] == []
        assert checklist["title"] == "auto_call_ch_list"
        assert checklist["entityType"] == "CALL"
        assert checklist["enabled"] is True
        assert checklist["deleted"] is False
        assert checklist["priority"] == 0
        assert checklist["maxPoints"] == 10.0
        assert checklist["minPoints"] == -10.0

    with allure.step("GET /checklists/ empty with fake ?rule_owner"):
        get_checklists = requests.get(url=API_URL + f'/checklists/?rule_owner={fake_id}', headers=headers)

    with allure.step("Check status code == 404 and User not found"):
        assert get_checklists.status_code == 404
        assert get_checklists.text == '{"detail":"User not found"}'

    with allure.step("GET /checklists/ empty with ecotelecom ?rule_owner"):
        get_checklists = requests.get(url=API_URL + f'/checklists/?rule_owner={ecotelecom_id}', headers=headers)

    with allure.step("Check status code == 403 and Access to user denied"):
        assert get_checklists.status_code == 403
        assert get_checklists.text == '{"detail":"Access to user denied"}'

    with allure.step("GET /checklists/ empty with broken ?rule_owner"):
        get_checklists = requests.get(url=API_URL + f'/checklists/?rule_owner={fake_id[:10]}', headers=headers)

    with allure.step("Check status code == 422 and empty"):
        assert get_checklists.status_code == 422
        assert "Value error, Not a valid ObjectId" in get_checklists.text

    with allure.step("POST /checklists/ with empty payload"):
        create_check_list_empty = requests.post(url=API_URL + "/checklists/", headers=headers, json={})

    with allure.step("Check status code == 422 and field required"):
        assert create_check_list_empty.status_code == 422
        assert "Field required" in create_check_list_empty.text

    with allure.step("POST /checklists/ Create check list"):
        json_check_list = {
            "enabledUsers":[],
            "title":check_list_title,
            "entityType":"CALL",
            "enabled":True,
            "priority":1,
            "globalFilter":{
                "title":None,
                "items":
                    [
                        {"key":"search_by_tags",
                         "complexValues":
                             [
                                 {"name":"auto","value":"test"}
                             ],
                         "logic":"and"}
                    ]
            },
            "questions":
                [
                    {"id":"",
                     "text":"question 1",
                     "answerValues":["answer 1"],
                     "answerAutoSelectSearchFilters":
                         {"answer 1":{"title":None,"items":[{"key":"any_of_tags","values":["auto"]}]}},
                     "answerSelectedTaggingLogic":
                         {"answer 1":[{"strategyOnSet":"ADD","strategyOnUnset":"REMOVE","tags":["auto"]}]},
                     "answerPoints":
                         {"answer 1":1}}],
            "appraisers":[
                {"title":"appriser",
                 "points":1,
                 "globalFilter":
                     {"items":[
                         {
                             "key":"search_by_tags",
                             "values":[],
                             "complexValues":[{"name":"auto","value":"test"}],
                             "logic":"and"
                         }
                     ],
                      "title":None}
                 }
            ],
            "generateReport":False}

        create_check_list = requests.post(url=API_URL + "/checklists/", headers=headers, json=json_check_list)
        check_list_id = create_check_list.text.replace('"', '')

    with allure.step("Check status code == 200 and have user_id"):
        assert create_check_list.status_code == 200
        assert len(check_list_id) == 24

    with allure.step("GET /checklists/"):
        get_checklists = requests.get(url=API_URL + "/checklists/", headers=headers)

    with allure.step("Check status code == 200 and have 2 check lists in list. Check that we created"):
        # check_lists_list = [
        #     {
        #         "id": check_list_id,
        #         "owner": USER_ID,
        #         "enabledUsers": [],
        #         "title": check_list_title,
        #         "entityType": "CALL",
        #         "enabled": True,
        #         "deleted": False,
        #         "priority": 1,
        #         "maxPoints": 1.0,
        #         'minPoints': 0.0
        #     }
        # ]

        assert get_checklists.status_code == 200
        # assert get_checklists.json() == check_lists_list

        response_data = get_checklists.json()

        assert len(response_data) == 2
        checklist = response_data[1]

        assert checklist["id"] == check_list_id
        assert checklist["owner"] == USER_ID
        assert checklist["enabledUsers"] == []
        assert checklist["title"] == check_list_title
        assert checklist["entityType"] == "CALL"
        assert checklist["enabled"] is True
        assert checklist["deleted"] is False
        assert checklist["priority"] == 1
        assert checklist["maxPoints"] == 1.0
        assert checklist["minPoints"] == 0.0

    with allure.step("GET /checklists/check_list_id"):
        get_check_list_by_id = requests.get(url=API_URL + f'/checklists/{check_list_id}', headers=headers)

    with allure.step("Check status code == 200 and have info abou check list"):
        assert get_check_list_by_id.status_code == 200
        assert check_list_title in get_check_list_by_id.text

    # commented because of https://task.imot.io/browse/DEV-3260

    # with allure.step("DELETE check list with broken id"):
    #     delete_check_list_broken_id = requests.delete(url=API_URL + f'/checklists/{fake_id[:10]}', headers=headers)
    #
    # with allure.step("Check status code == 422"):
    #     assert delete_check_list_broken_id.status_code == 422
    #     assert "Value error, Not a valid ObjectId" in delete_check_list_broken_id.text

    with allure.step("DELETE check list with broken id"):
        delete_check_list_user_not_found = requests.delete(url=API_URL + f'/checklists/{fake_id}', headers=headers)

    with allure.step("Check status code == 404"):
        assert delete_check_list_user_not_found.status_code == 404
        assert delete_check_list_user_not_found.text == '{"detail":"Checklist not found"}'

    with allure.step("DELETE check list"):
        delete_check_list = requests.delete(url=API_URL + f'/checklists/{check_list_id}', headers=headers)

    with allure.step("Check status code == 204"):
        assert delete_check_list.status_code == 204

    with allure.step("GET /checklists/ empty without ?rule_owner"):
         get_checklists = requests.get(url=API_URL + "/checklists/", headers=headers)

    with allure.step("Check status code == 200 and have default checklist"):
        assert get_checklists.status_code == 200
        response_data = get_checklists.json()

        assert len(response_data) == 1
        checklist = response_data[0]

        # checking default check list without id. id is unique for every check list
        assert checklist["owner"] == USER_ID
        assert checklist["enabledUsers"] == []
        assert checklist["title"] == "auto_call_ch_list"
        assert checklist["entityType"] == "CALL"
        assert checklist["enabled"] is True
        assert checklist["deleted"] is False
        assert checklist["priority"] == 0
        assert checklist["maxPoints"] == 10.0
        assert checklist["minPoints"] == -10.0

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)
