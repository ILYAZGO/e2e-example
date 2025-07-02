#from playwright.sync_api import Page, expect, BrowserContext, sync_playwright, Playwright
from utils.variables import *
from pages.page_requests import *
from utils.create_delete_user import create_user, delete_user
import pytest
import allure

@pytest.mark.page_requests
@pytest.mark.e2e
@allure.title("test_communications_requests_by_user")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_communications_requests_by_user")
def test_communications_requests_by_user(base_url, page: Page) -> None:
    page_requests = PageRequests(page)

    communications_requests = []

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        page_requests.navigate(base_url)
        page.wait_for_timeout(2000)

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            communications_requests.append({
                'url': request.url,
                'method': request.method,
                # 'headers': request.headers,
                # 'post_data': request.post_data
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Auth with user"):
        page_requests.auth(LOGIN, PASSWORD)

    with allure.step("Check requests list"):
        page.wait_for_timeout(8000)
        assert len(communications_requests) == 20
        assert sum('/token' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum('/user/me/access_rights' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum('/search_criterias/default_keys' in entry.get('url', '') for entry in communications_requests) == 2
        assert sum('/search_filters/' in entry.get('url', '') for entry in communications_requests) == 2
        assert sum('/user/me?with_quota=true' in entry.get('url', '') for entry in communications_requests) == 2
        assert sum('/reports' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum('/translation/get_all_languages' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum('/get_date_range_by_period?period=today' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum('/users/?with_childs=true' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum('/open_id/list' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum('/user/filter?with_quota=true' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum('/search_criterias/' in entry.get('url', '') for entry in communications_requests) == 4 # 2 here 2 with /default_keys
        assert sum('/search_calls/' in entry.get('url', '') for entry in communications_requests) == 2
        assert sum(f'/user/{USER_ID}?with_quota=true' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum(f'/set_filter_user?user_id={USER_ID}' in entry.get('url', '') for entry in communications_requests) == 1

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)

@pytest.mark.page_requests
@pytest.mark.e2e
@allure.title("test_communications_requests_by_admin")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_communications_requests_by_admin")
def test_communications_requests_by_admin(base_url, page: Page) -> None:
    page_requests = PageRequests(page)

    communications_requests = []

    with allure.step("Create admin"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Go to url"):
        page_requests.navigate(base_url)
        page.wait_for_timeout(2000)

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            communications_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Auth with admin"):
        page_requests.auth(LOGIN, PASSWORD)

    with allure.step("Check requests list"):
        page.wait_for_timeout(7000)
        assert len(communications_requests) == 11
        assert sum('/token' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum('/user/me/access_rights' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum('/user/me?with_quota=true' in entry.get('url', '') for entry in communications_requests) == 2
        assert sum('/translation/get_all_languages' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum('/users/?with_childs=true' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum('/users/?with_childs=false' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum('/open_id/list' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum('/user/filter?with_quota=true' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum(f'/user/{USER_ID}?with_quota=true' in entry.get('url', '') for entry in communications_requests) == 1
        assert sum(f'/set_filter_user?user_id={USER_ID}' in entry.get('url', '') for entry in communications_requests) == 1

    with allure.step("Delete admin"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.page_requests
@pytest.mark.e2e
@allure.title("test_markup_requests_by_user")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_markup_requests. rules, dicts, checklists, gpt")
def test_markup_requests_by_user(base_url, page: Page) -> None:
    page_requests = PageRequests(page)

    rules_requests = []
    dicts_requests = []
    checklists_requests = []
    gpt_requests = []

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        page_requests.navigate(base_url)

    with allure.step("Auth with user"):
        page_requests.auth(LOGIN, PASSWORD)
        page.wait_for_timeout(14000)

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            rules_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to markup"):
        page_requests.click_markup()

    with allure.step("Check requests list"):
        page.wait_for_timeout(10000)
        assert len(rules_requests) == 6
        assert sum('/users/?with_childs=false&filter_only_users=true' in entry.get('url', '') for entry in rules_requests) == 1
        assert sum('/search_criterias/' in entry.get('url', '') for entry in rules_requests) == 1
        assert sum('/tag_rule_groups/' in entry.get('url', '') for entry in rules_requests) == 1
        assert sum('/tag_rules/?sort=update_time&sort_desc=true&show_disabled=true' in entry.get('url', '') for entry in rules_requests) == 1
        assert sum('/active_dicts/' in entry.get('url', '') for entry in rules_requests) == 1
        assert sum('/tag_rules_dep_check/' in entry.get('url', '') for entry in rules_requests) == 1

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            dicts_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Click dicts"):
        page_requests.click_to_dicts()

    with allure.step("Check requests list"):
        page.wait_for_timeout(7000)
        assert len(dicts_requests) == 5
        assert sum('/users/?with_childs=false&filter_only_users=true' in entry.get('url', '') for entry in dicts_requests) == 1
        assert sum('/search_criterias/' in entry.get('url', '') for entry in dicts_requests) == 1
        assert sum('/dict_groups/' in entry.get('url', '') for entry in dicts_requests) == 1
        assert sum('/dicts/?sort=title&sort_desc=false&show_disabled=true' in entry.get('url', '') for entry in dicts_requests) == 1
        assert sum('/active_dicts/' in entry.get('url', '') for entry in dicts_requests) == 1


    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            checklists_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Click check lists"):
        page_requests.click_check_lists()

    with allure.step("Check requests list"):
        page.wait_for_timeout(7000)
        assert len(checklists_requests) == 4
        assert sum('/users/?with_childs=false&filter_only_users=true' in entry.get('url', '') for entry in checklists_requests) == 1
        assert sum('/search_criterias/' in entry.get('url', '') for entry in checklists_requests) == 1
        assert sum('/checklists/' in entry.get('url', '') for entry in checklists_requests) == 2

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            gpt_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Click gpt"):
        page_requests.click_gpt()

    with allure.step("Check requests list"):
        page.wait_for_timeout(7000)
        # if no any gpt rules
        assert len(gpt_requests) == 3
        assert sum('/users/?with_childs=false&filter_only_users=true' in entry.get('url', '') for entry in gpt_requests) == 1
        assert sum('/search_criterias/' in entry.get('url', '') for entry in gpt_requests) == 1
        assert sum('/gpt/' in entry.get('url', '') for entry in gpt_requests) == 1

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)

@pytest.mark.page_requests
@pytest.mark.e2e
@allure.title("test_markup_requests_by_admin")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_markup_requests. rules, dicts, checklists, gpt")
def test_markup_requests_by_admin(base_url, page: Page) -> None:
    page_requests = PageRequests(page)

    rules_requests = []
    dicts_requests = []
    checklists_requests = []
    gpt_requests = []

    with allure.step("Create admin"):
        USER_ID_ADMIN, TOKEN_ADMIN, LOGIN_ADMIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Create user"):
        USER_ID_USER, TOKEN_USER, LOGIN_USER = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        page_requests.navigate(base_url)

    with allure.step("Auth with admin"):
        page_requests.auth(LOGIN_ADMIN, PASSWORD)

    with allure.step("Go to user"):
        page_requests.go_to_user(LOGIN_USER)
        page.wait_for_timeout(10000)

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            rules_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to markup"):
        page_requests.click_markup()

    with allure.step("Check requests list"):
        page.wait_for_timeout(7000)
        assert len(rules_requests) == 6
        assert sum('/users/?with_childs=false&filter_only_users=true' in entry.get('url', '') for entry in rules_requests) == 1
        assert sum('/search_criterias/' in entry.get('url', '') for entry in rules_requests) == 1
        assert sum('/tag_rule_groups/' in entry.get('url', '') for entry in rules_requests) == 1
        assert sum('/tag_rules/?sort=update_time&sort_desc=true&show_disabled=true' in entry.get('url', '') for entry in rules_requests) == 1
        assert sum('/active_dicts/' in entry.get('url', '') for entry in rules_requests) == 1
        assert sum('/tag_rules_dep_check/' in entry.get('url', '') for entry in rules_requests) == 1

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            dicts_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Click dicts"):
        page_requests.click_to_dicts()

    with allure.step("Check requests list"):
        page.wait_for_timeout(7000)
        assert len(dicts_requests) == 5
        assert sum('/users/?with_childs=false&filter_only_users=true' in entry.get('url', '') for entry in dicts_requests) == 1
        assert sum('/search_criterias/' in entry.get('url', '') for entry in dicts_requests) == 1
        assert sum('/dict_groups/' in entry.get('url', '') for entry in dicts_requests) == 1
        assert sum('/dicts/?sort=title&sort_desc=false&show_disabled=true' in entry.get('url', '') for entry in dicts_requests) == 1
        assert sum('/active_dicts/' in entry.get('url', '') for entry in dicts_requests) == 1


    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            checklists_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Click check lists"):
        page_requests.click_check_lists()

    with allure.step("Check requests list"):
        page.wait_for_timeout(7000)
        assert len(checklists_requests) == 4
        assert sum('/users/?with_childs=false&filter_only_users=true' in entry.get('url', '') for entry in checklists_requests) == 1
        assert sum('/search_criterias/' in entry.get('url', '') for entry in checklists_requests) == 1
        assert sum('/checklists/' in entry.get('url', '') for entry in checklists_requests) == 2

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            gpt_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Click gpt"):
        page_requests.click_gpt()

    with allure.step("Check requests list"):
        page.wait_for_timeout(7000)
        # if no any gpt rules
        assert len(gpt_requests) == 3
        assert sum('/users/?with_childs=false&filter_only_users=true' in entry.get('url', '') for entry in gpt_requests) == 1
        assert sum('/search_criterias/' in entry.get('url', '') for entry in gpt_requests) == 1
        assert sum('/gpt/' in entry.get('url', '') for entry in gpt_requests) == 1

    with allure.step("Delete admin"):
        delete_user(API_URL, TOKEN_ADMIN, USER_ID_ADMIN)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN_USER, USER_ID_USER)


@pytest.mark.page_requests
@pytest.mark.e2e
@allure.title("test_notifications_requests_by_user")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_notifications_requests_by_user")
def test_notifications_requests_by_user(base_url, page: Page) -> None:
    page_requests = PageRequests(page)

    notifications_requests = []

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        page_requests.navigate(base_url)

    with allure.step("Auth with user"):
        page_requests.auth(LOGIN, PASSWORD)
        page.wait_for_timeout(14000)

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            notifications_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to notifications"):
        page_requests.click_notifications()

    with allure.step("Check requests list"):
        page.wait_for_timeout(7000)
        assert len(notifications_requests) == 6
        assert sum('/notify_rules/' in entry.get('url', '') for entry in notifications_requests) == 6 # 2 directly 4 in others
        assert sum('/notify_rules/available_directions' in entry.get('url', '') for entry in notifications_requests) == 1
        assert sum('/notify_rules/amo_fillable_custom_fields' in entry.get('url', '') for entry in notifications_requests) == 1
        assert sum('/notify_rules/bitrix_fillable_custom_fields' in entry.get('url', '') for entry in notifications_requests) == 1
        assert sum('/notify_rules/notify_rule_variables' in entry.get('url', '') for entry in notifications_requests) == 1

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.page_requests
@pytest.mark.e2e
@allure.title("test_notifications_requests_by_admin")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_notifications_requests_by_admin")
def test_notifications_requests_by_admin(base_url, page: Page) -> None:
    page_requests = PageRequests(page)

    notifications_requests = []

    with allure.step("Create admin"):
        USER_ID_ADMIN, TOKEN_ADMIN, LOGIN_ADMIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Create user"):
        USER_ID_USER, TOKEN_USER, LOGIN_USER = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        page_requests.navigate(base_url)

    with allure.step("Auth with admin"):
        page_requests.auth(LOGIN_ADMIN, PASSWORD)

    with allure.step("Go to user"):
        page_requests.go_to_user(LOGIN_USER)
        page.wait_for_timeout(10000)

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            notifications_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to notifications"):
        page_requests.click_notifications()

    with allure.step("Check requests list"):
        page.wait_for_timeout(10000)
        assert len(notifications_requests) == 6
        assert sum('/notify_rules/' in entry.get('url', '') for entry in notifications_requests) == 6 # 2 directly 4 in others
        assert sum('/notify_rules/available_directions' in entry.get('url', '') for entry in notifications_requests) == 1
        assert sum('/notify_rules/amo_fillable_custom_fields' in entry.get('url', '') for entry in notifications_requests) == 1
        assert sum('/notify_rules/bitrix_fillable_custom_fields' in entry.get('url', '') for entry in notifications_requests) == 1
        assert sum('/notify_rules/notify_rule_variables' in entry.get('url', '') for entry in notifications_requests) == 1

    with allure.step("Delete admin"):
        delete_user(API_URL, TOKEN_ADMIN, USER_ID_ADMIN)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN_USER, USER_ID_USER)


@pytest.mark.page_requests
@pytest.mark.e2e
@allure.title("test_settings_requests_by_user")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_settings_requests_by_user")
def test_settings_requests_by_user(base_url, page: Page) -> None:
    page_requests = PageRequests(page)

    personal_info_requests = []
    employees_requests = []
    actions_requests = []
    quota_requests = []
    consumption_requests = []
    tariffication_requests = []
    address_book_requests = []
    integrations_requests = []

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD, upload_call=False)

    with allure.step("Go to url"):
        page_requests.navigate(base_url)

    with allure.step("Auth with user"):
        page_requests.auth(LOGIN, PASSWORD)
        page.wait_for_timeout(10000)

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            personal_info_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page_requests.click_settings()

    with allure.step("Check requests list"):
        page.wait_for_timeout(7000)
        assert len(personal_info_requests) == 4
        assert sum('/industries' in entry.get('url', '') for entry in personal_info_requests) == 1  #403 {"detail":"Industry handling not allowed"}
        assert sum('/users/?filter_only_managers=true' in entry.get('url', '') for entry in personal_info_requests) == 1
        assert sum('/all_timezones' in entry.get('url', '') for entry in personal_info_requests) == 1
        assert sum(f'/user/{USER_ID}?with_quota=true' in entry.get('url', '') for entry in personal_info_requests) == 1

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            employees_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page_requests.click_employees()

    with allure.step("Check requests list"):
        page.wait_for_timeout(5000)
        assert len(employees_requests) == 1
        assert sum(f'/user/{USER_ID}/operators' in entry.get('url', '') for entry in employees_requests) == 1

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            actions_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page_requests.click_actions_with_calls()

    with allure.step("Check requests list"):
        page.wait_for_timeout(5000)
        assert len(actions_requests) == 1
        assert sum(f'/progress_tasks' in entry.get('url', '') for entry in actions_requests) == 1

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            quota_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page_requests.click_quota()

    with allure.step("Check requests list"):
        page.wait_for_timeout(5000)
        assert len(quota_requests) == 2
        assert sum(f'/user/{USER_ID}/quotas' in entry.get('url', '') for entry in quota_requests) == 2 #need fix

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            consumption_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page.locator(BUTTON_CONSUMPTION_HISTORY).click()

    with allure.step("Check requests list"):
        page.wait_for_timeout(5000)
        assert len(consumption_requests) == 1
        assert sum(f'/user/{USER_ID}/history/calls?' in entry.get('url', '') for entry in consumption_requests) == 1

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            tariffication_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page.locator(BUTTON_TARIFFICATION).click()

    with allure.step("Check requests list"):
        page.wait_for_timeout(5000)
        assert len(tariffication_requests) == 1
        assert sum(f'/billing/billing_info' in entry.get('url', '') for entry in tariffication_requests) == 1

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            address_book_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page_requests.click_address_book()

    with allure.step("Check requests list"):
        page.wait_for_timeout(5000)
        assert len(address_book_requests) == 1
        assert sum(f'/user/{USER_ID}/address_book/csv' in entry.get('url', '') for entry in address_book_requests) == 1

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            integrations_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page_requests.press_integrations_in_menu()

    with allure.step("Check requests list"):
        page.wait_for_timeout(5000)
        assert len(integrations_requests) == 2
        assert sum(f'/integrations/services?detail=true' in entry.get('url', '') for entry in integrations_requests) == 1
        assert sum(f'/integrations/{USER_ID}' in entry.get('url', '') for entry in integrations_requests) == 1

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.page_requests
@pytest.mark.e2e
@allure.title("test_settings_requests_by_admin")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_settings_requests_by_admin")
def test_settings_requests_by_admin(base_url, page: Page) -> None:
    page_requests = PageRequests(page)

    personal_info_requests = []
    rights_requests = []
    employees_requests = []
    actions_requests = []
    stt_requests = []
    quota_requests = []
    consumption_requests = []
    tariffication_requests = []
    address_book_requests = []
    integrations_requests = []

    with allure.step("Create admin"):
        USER_ID_ADMIN, TOKEN_ADMIN, LOGIN_ADMIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Create user"):
        USER_ID_USER, TOKEN_USER, LOGIN_USER = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        page_requests.navigate(base_url)

    with allure.step("Auth with admin"):
        page_requests.auth(LOGIN_ADMIN, PASSWORD)

    with allure.step("Go to user"):
        page_requests.go_to_user(LOGIN_USER)
        page.wait_for_timeout(10000)

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            rights_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page_requests.click_rights()

    with allure.step("Check requests list"):
        page.wait_for_timeout(5000)
        assert len(rights_requests) == 2
        assert sum(f'/user/{USER_ID_USER}/access_rights' in entry.get('url', '') for entry in rights_requests) == 1
        assert sum(f'/user/{USER_ID_USER}/access_rights_description' in entry.get('url', '') for entry in rights_requests) == 1

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            personal_info_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page_requests.click_settings()

    with allure.step("Check requests list"):
        page.wait_for_timeout(7000)
        assert len(personal_info_requests) == 4
        assert sum('/industries' in entry.get('url', '') for entry in personal_info_requests) == 1  #403 {"detail":"Industry handling not allowed"}
        assert sum('/users/?filter_only_managers=true' in entry.get('url', '') for entry in personal_info_requests) == 1
        assert sum('/all_timezones' in entry.get('url', '') for entry in personal_info_requests) == 1
        assert sum(f'/user/{USER_ID_USER}?with_quota=true' in entry.get('url', '') for entry in personal_info_requests) == 1

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            employees_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page_requests.click_employees()

    with allure.step("Check requests list"):
        page.wait_for_timeout(5000)
        assert len(employees_requests) == 1
        assert sum(f'/user/{USER_ID_USER}/operators' in entry.get('url', '') for entry in employees_requests) == 1

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            actions_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page_requests.click_actions_with_calls()

    with allure.step("Check requests list"):
        page.wait_for_timeout(5000)
        assert len(actions_requests) == 1
        assert sum(f'/progress_tasks' in entry.get('url', '') for entry in actions_requests) == 1

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            stt_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page_requests.click_word_processing()

    with allure.step("Check requests list"):
        page.wait_for_timeout(5000)
        assert len(stt_requests) == 5
        assert sum(f'/user/{USER_ID_USER}?with_quota=true' in entry.get('url', '') for entry in stt_requests) == 1
        assert sum(f'/stt/get_all_languages' in entry.get('url', '') for entry in stt_requests) == 1
        assert sum(f'/stt/ru-RU/engines' in entry.get('url', '') for entry in stt_requests) == 1
        assert sum(f'/stt/ru-RU/nlab_speech/models' in entry.get('url', '') for entry in stt_requests) == 1
        assert sum(f'/stt/nlab_speech/stt_options' in entry.get('url', '') for entry in stt_requests) == 1

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            quota_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page_requests.click_quota()

    with allure.step("Check requests list"):
        page.wait_for_timeout(5000)
        assert len(quota_requests) == 2
        assert sum(f'/user/{USER_ID_USER}/quotas' in entry.get('url', '') for entry in quota_requests) == 2 #need fix

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            consumption_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page.locator(BUTTON_CONSUMPTION_HISTORY).click()

    with allure.step("Check requests list"):
        page.wait_for_timeout(5000)
        assert len(consumption_requests) == 1
        assert sum(f'/user/{USER_ID_USER}/history/calls?' in entry.get('url', '') for entry in consumption_requests) == 1

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            tariffication_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page.locator(BUTTON_TARIFFICATION).click()

    with allure.step("Check requests list"):
        page.wait_for_timeout(5000)
        assert len(tariffication_requests) == 1
        assert sum(f'/billing/billing_info' in entry.get('url', '') for entry in tariffication_requests) == 1

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            address_book_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page_requests.click_address_book()

    with allure.step("Check requests list"):
        page.wait_for_timeout(5000)
        assert len(address_book_requests) == 1
        assert sum(f'/user/{USER_ID_USER}/address_book/csv' in entry.get('url', '') for entry in address_book_requests) == 1

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            integrations_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page_requests.press_integrations_in_menu()

    with allure.step("Check requests list"):
        page.wait_for_timeout(5000)
        assert len(integrations_requests) == 2
        assert sum(f'/integrations/services?detail=true' in entry.get('url', '') for entry in integrations_requests) == 1
        assert sum(f'/integrations/{USER_ID_USER}' in entry.get('url', '') for entry in integrations_requests) == 1

###
    #download communications. no any requests yet
###
    with allure.step("Delete admin"):
        delete_user(API_URL, TOKEN_ADMIN, USER_ID_ADMIN)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN_USER, USER_ID_USER)



@pytest.mark.page_requests
@pytest.mark.e2e
@allure.title("test_settings_requests_by_admin")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_settings_requests_by_admin")
def test_settings_requests_by_admin(base_url, page: Page) -> None:
    page_requests = PageRequests(page)

    settings_requests = []

    with allure.step("Create admin"):
        USER_ID_ADMIN, TOKEN_ADMIN, LOGIN_ADMIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Create user"):
        USER_ID_USER, TOKEN_USER, LOGIN_USER = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        page_requests.navigate(base_url)

    with allure.step("Auth with admin"):
        page_requests.auth(LOGIN_ADMIN, PASSWORD)

    with allure.step("Go to user"):
        page_requests.go_to_user(LOGIN_USER)
        page.wait_for_timeout(10000)

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            settings_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to settings"):
        page_requests.click_settings()

    with allure.step("Check requests list"):
        page.wait_for_timeout(7000)
        assert len(settings_requests) == 4
        assert sum('/industries' in entry.get('url', '') for entry in settings_requests) == 1
        assert sum('/users/?filter_only_managers=true' in entry.get('url', '') for entry in settings_requests) == 1
        assert sum('/all_timezones' in entry.get('url', '') for entry in settings_requests) == 1
        assert sum(f'/user/{USER_ID_USER}?with_quota=true' in entry.get('url', '') for entry in settings_requests) == 1

    with allure.step("Delete admin"):
        delete_user(API_URL, TOKEN_ADMIN, USER_ID_ADMIN)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN_USER, USER_ID_USER)


@pytest.mark.page_requests
@pytest.mark.e2e
@allure.title("test_users_list_requests_by_admin")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test_users_list_requests_by_admin")
def test_users_list_requests_by_admin(base_url, page: Page) -> None:
    page_requests = PageRequests(page)

    users_list_requests = []

    with allure.step("Create admin"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Go to url"):
        page_requests.navigate(base_url)

    with allure.step("Auth with admin"):
        page_requests.auth(LOGIN, PASSWORD)
        page.wait_for_timeout(10000)

    with allure.step("Request capture start"):
        page.on("request", lambda request: (
            users_list_requests.append({
                'url': request.url,
                'method': request.method
            }) if request.resource_type in ['xhr', 'fetch'] else None
        ))

    with allure.step("Go to users list"):
        page_requests.go_to_users_list()

    with allure.step("Check requests list"):
        page.wait_for_timeout(7000)
        assert len(users_list_requests) == 4
        assert sum('/industries' in entry.get('url', '') for entry in users_list_requests) == 1
        assert sum('/users/?filter_only_managers=true' in entry.get('url', '') for entry in users_list_requests) == 1
        assert sum('/stt/get_all_languages' in entry.get('url', '') for entry in users_list_requests) == 1
        assert sum('/users/?with_childs=true&with_quota=true' in entry.get('url', '') for entry in users_list_requests) == 1

    with allure.step("Delete admin"):
        delete_user(API_URL, TOKEN, USER_ID)