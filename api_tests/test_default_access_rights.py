from utils.create_delete_user import create_user, delete_user, create_operator
from utils.variables import *
from api_tests.common import *
import requests as r
import pytest
import allure


@pytest.mark.api
@allure.title("test_check_default_access_rights_for_admin")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("/user/me/access_rights for admin")
def test_check_default_access_rights_for_admin():

    with allure.step("Create admin"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Get access rights list"):
        headers = {'Authorization': TOKEN}

        get_access_rights = r.get(url=API_URL + "/user/me/access_rights", headers=headers)

    with allure.step("Check status code == 200 and list correct"):

        access_rights = {
            "search":True,
             "audio":True,
             "video":True,
             "gpt":True,
             "stt":True,
             "upload":True,
             "report":True,
             "report_manage":True,
             "operators_report":False,
             "dictionary":True,
             "tagging":True,
             "notify":True,
             "address_book":True,
             "phone_number":True,
             "tags":True,
             "export":True,
             "calls_actions":True,
             "retag":True,
             "deals":True,
             "restt":True,
             "delete_call":True,
             "delete_user":True,
             "set_filter_user":True,
             "add_user":True,
             "add_operator":True,
             "delete_operator":True,
             "set_default_engine":True,
             "quota_view":True,
             "quota_edit":True,
             "admin":True,
             "edit_admin_rights":False,
             "choose_gpt_engine":True,
             "fill_gpt_template":True,
             "checklist":True,
             "checklist_view":True,
             "checklist_update":True,
             "import_foreign_rules":True,
             "integration_view":True,
             "integration_edit":True,
             "edit_operator":True,
             "edit_user":True,
             "industry":True,
             "generate_public_link":True,
             "public_link_age":True,
             "edit_manager":True,
             "edit_admin":True,
             "edit_user_login":True,
             "call_info_tech_data":True,
             "call_info_processing":True,
             "gpt_quota":True,
             "manual_tagging":True,
             "usage_history":True,
             "user_modules_setup":True,
             "billing_view":True,
             "call_reload_source_integration":True,
             "enable_free_gpt_rule":True,
             "continuous_recordings":True
        }

        assert get_access_rights.status_code == 200
        assert get_access_rights.json() == access_rights

    with allure.step("Delete admin"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.api
@allure.title("test_check_default_access_rights_for_manager")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("/user/me/access_rights for manager")
def test_check_default_access_rights_for_manager():

    with allure.step("Create manager"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_MANAGER, PASSWORD)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("Get access rights list"):
        headers = {'Authorization': user_token}

        get_access_rights = r.get(url=API_URL + "/user/me/access_rights", headers=headers)

    with allure.step("Check status code == 200 and list correct"):
        access_rights = {
            "search": True,
            "audio": True,
            "video": True,
            "gpt": True,
            "stt": True,
            "upload": True,
            "report": True,
            "report_manage": True,
            "operators_report": False,
            "dictionary": True,
            "tagging": True,
            "notify": True,
            "address_book": True,
            "phone_number": True,
            "tags": True,
            "export": True,
            "calls_actions": True,
            "retag": True,
            "deals": False,
            "restt": False,
            "delete_call": True,
            "delete_user": False,
            "set_filter_user": True,
            "add_user": False,
            "add_operator": True,
            "delete_operator": True,
            "set_default_engine": False,
            "quota_view": True,
            "quota_edit": False,
            "admin": False,
            "edit_admin_rights": False,
            "choose_gpt_engine": True,
            "fill_gpt_template": False,
            "checklist": True,
            "checklist_view": True,
            "checklist_update": True,
            "import_foreign_rules": True,
            "integration_view": True,
            "integration_edit": True,
            "edit_operator": True,
            "edit_user": True,
            "industry": True,
            "generate_public_link": True,
            "public_link_age": True,
            "edit_manager": False,
            "edit_admin": False,
            "edit_user_login": False,
            "call_info_tech_data": False,
            "call_info_processing": True,
            "gpt_quota": False,
            "manual_tagging": True,
            "usage_history": True,
            "user_modules_setup": False,
            "billing_view": True,
            "call_reload_source_integration": True,
            "enable_free_gpt_rule": False,
            "continuous_recordings": True
        }

        assert get_access_rights.status_code == 200
        assert get_access_rights.json() == access_rights

    with allure.step("Delete manager"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.api
@allure.title("test_check_default_access_rights_for_user")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("/user/me/access_rights for user")
def test_check_default_access_rights_for_user():

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Get token for user"):
        user_token = get_token(API_URL, LOGIN, PASSWORD)

    with allure.step("Get access rights list"):
        headers = {'Authorization': user_token}

        get_access_rights = r.get(url=API_URL + "/user/me/access_rights", headers=headers)

    with allure.step("Check status code == 200 and list correct"):
        access_rights = {
            "search": True,
            "audio": True,
            "video": True,
            "gpt": True,
            "stt": True,
            "upload": True,
            "report": True,
            "report_manage": True,
            "operators_report": False,
            "dictionary": True,
            "tagging": True,
            "notify": True,
            "address_book": True,
            "phone_number": True,
            "tags": True,
            "export": True,
            "calls_actions": True,
            "retag": True,
            "deals": False,
            "restt": False,
            "delete_call": False,
            "delete_user": True,
            "set_filter_user": False,
            "add_user": False,
            "add_operator": True,
            "delete_operator": True,
            "set_default_engine": False,
            "quota_view": True,
            "quota_edit": False,
            "admin": False,
            "edit_admin_rights": False,
            "choose_gpt_engine": True,
            "fill_gpt_template": False,
            "checklist": True,
            "checklist_view": True,
            "checklist_update": True,
            "import_foreign_rules": False,
            "integration_view": True,
            "integration_edit": True,
            "edit_operator": True,
            "edit_user": False,
            "industry": False,
            "generate_public_link": True,
            "public_link_age": True,
            "edit_manager": False,
            "edit_admin": False,
            "edit_user_login": False,
            "call_info_tech_data": False,
            "call_info_processing": False,
            "gpt_quota": False,
            "manual_tagging": True,
            "usage_history": True,
            "user_modules_setup": False,
            "billing_view": True,
            "call_reload_source_integration": True,
            "enable_free_gpt_rule": False,
            "continuous_recordings": True
        }

        assert get_access_rights.status_code == 200
        assert get_access_rights.json() == access_rights

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.api
@allure.title("test_check_default_access_rights_for_operator")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("/user/me/access_rights for operator")
def test_check_default_access_rights_for_operator():

    with allure.step("Create user"):
        USER_ID_USER, TOKEN_USER, LOGIN_USER = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Create operator"):
        USER_ID_OPERATOR, TOKEN_OPERATOR, LOGIN_OPERATOR = create_operator(API_URL, USER_ID_USER, PASSWORD)

    with allure.step("Get token for operator"):
        user_token = get_token(API_URL, LOGIN_OPERATOR, PASSWORD)

    with allure.step("Get access rights list"):
        headers = {'Authorization': user_token}

        get_access_rights = r.get(url=API_URL + "/user/me/access_rights", headers=headers)

    with allure.step("Check status code == 200 and list correct"):
        access_rights = {
            "search": True,
            "audio": True,
            "video": False,
            "gpt": False,
            "stt": True,
            "upload": False,
            "report": True,
            "report_manage": False,
            "operators_report": False,
            "dictionary": False,
            "tagging": False,
            "notify": False,
            "address_book": False,
            "phone_number": False,
            "tags": True,
            "export": False,
            "calls_actions": False,
            "retag": False,
            "deals": False,
            "restt": False,
            "delete_call": False,
            "delete_user": False,
            "set_filter_user": False,
            "add_user": False,
            "add_operator": False,
            "delete_operator": False,
            "set_default_engine": False,
            "quota_view": False,
            "quota_edit": False,
            "admin": False,
            "edit_admin_rights": False,
            "choose_gpt_engine": True,
            "fill_gpt_template": False,
            "checklist": False,
            "checklist_view": True,
            "checklist_update": False,
            "import_foreign_rules": False,
            "integration_view": False,
            "integration_edit": False,
            "edit_operator": False,
            "edit_user": False,
            "industry": False,
            "generate_public_link": False,
            "public_link_age": False,
            "edit_manager": False,
            "edit_admin": False,
            "edit_user_login": False,
            "call_info_tech_data": False,
            "call_info_processing": False,
            "gpt_quota": False,
            "manual_tagging": False,
            "usage_history": False,
            "user_modules_setup": False,
            "billing_view": False,
            "call_reload_source_integration": False,
            "enable_free_gpt_rule": False,
            "continuous_recordings": False
        }

        assert get_access_rights.status_code == 200
        assert get_access_rights.json() == access_rights

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN_USER, USER_ID_USER)

    with allure.step("Delete operator"):
        delete_user(API_URL, TOKEN_OPERATOR, USER_ID_OPERATOR)