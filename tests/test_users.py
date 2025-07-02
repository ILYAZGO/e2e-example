#from playwright.sync_api import Page, expect
from utils.variables import *
from pages.users import *
from datetime import datetime
from utils.create_delete_user import create_user, delete_user, give_manager_all_rights
import pytest
import allure
import random


@pytest.mark.e2e
@pytest.mark.users
@allure.title("test_add_delete_admin_by_admin")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_delete_admin_by_admin(base_url, page: Page) -> None:
    users = Users(page)

    NEW_NAME = NEW_LOGIN = f"auto_test_user_{datetime.now().strftime('%m%d%H%M')}{datetime.now().microsecond}"
    EMAIL = f"email_{datetime.now().microsecond}{random.randint(100, 200)}@mail.ru"
    PHONE = str(random.randint(10000000000, 99999999999))

    with allure.step("Create admin 1"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Go to url"):
        users.navigate(base_url)

    with allure.step("Auth with admin 1"):
        users.auth(LOGIN, PASSWORD)

    with allure.step("Go to users"):
        users.go_to_users_list()

    with allure.step("Press button (Add User)"):
        users.press_button_add_user()

    with allure.step("Set admin 2 info"):
        users.set_user(
            NEW_NAME,
            NEW_LOGIN,
            PASSWORD,
            EMAIL,
            PHONE,
            "PT",
            "someComment",
            "Администратор"
        )

    with allure.step("Press button (Add) in modal window"):
        users.press_button_add_in_modal()

    with allure.step("Check"):
        expect(users.input_name).to_have_value(NEW_NAME, timeout=users.timeout)
        expect(users.input_login).to_have_value(NEW_LOGIN, timeout=users.timeout)
        expect(users.input_email).to_have_value(EMAIL, timeout=users.timeout)
        expect(page.locator(SELECT_USER_LANG)).to_have_text("PT", timeout=users.timeout)
        expect(users.input_comment).to_have_text("someComment", timeout=users.timeout)
        expect(page.locator(SELECT_ROLE)).to_have_text("Администратор", timeout=users.timeout)
        page.wait_for_timeout(500)
        expect(users.input_phone).to_have_value(PHONE, timeout=users.timeout)
        expect(users.input_new_password).to_be_visible(timeout=users.timeout)
        expect(users.input_new_password_repeat).to_be_visible(timeout=users.timeout)

    with allure.step("Delete admin 2"):
        page.wait_for_timeout(3000)
        users.delete_added_user()

    with allure.step("Wait for alert and check alert message"):
        users.check_alert("Пользователь был удален")

    with allure.step("Check that admin 2 deleted"):
        expect(users.input_login).to_have_value(LOGIN, timeout=users.timeout)

    with allure.step("Delete admin 1"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.users
@allure.title("test_add_delete_manager_by_admin")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_delete_manager_by_admin(base_url, page: Page) -> None:
    users = Users(page)

    NEW_NAME = NEW_LOGIN = f"auto_test_user_{datetime.now().strftime('%m%d%H%M')}{datetime.now().microsecond}"
    EMAIL = f"email_{datetime.now().microsecond}{random.randint(100, 200)}@mail.ru"
    PHONE = str(random.randint(10000000000, 99999999999))

    with allure.step("Create admin"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Go to url"):
        users.navigate(base_url)

    with allure.step("Auth with admin"):
        users.auth(LOGIN, PASSWORD)

    with allure.step("Go to users"):
        users.go_to_users_list()

    with allure.step("Press button (Add User)"):
        users.press_button_add_user()

    with allure.step("Set manager info"):
        users.set_user(
            NEW_NAME,
            NEW_LOGIN,
            PASSWORD,
            EMAIL,
            PHONE,
            "PT",
            "someComment",
            "Интегратор"
            )

    with allure.step("Press button (Add) in modal window"):
        users.press_button_add_in_modal()

    with allure.step("Check"):
        expect(users.input_login).to_have_value(NEW_LOGIN, timeout=users.timeout)
        expect(users.input_name).to_have_value(NEW_NAME, timeout=users.timeout)
        expect(users.input_email).to_have_value(EMAIL, timeout=users.timeout)
        expect(page.locator(SELECT_USER_LANG)).to_have_text("PT", timeout=users.timeout)
        expect(users.input_comment).to_have_text("someComment", timeout=users.timeout)
        expect(page.locator(SELECT_ROLE)).to_have_text("Интегратор", timeout=users.timeout)
        expect(users.input_phone).to_have_value(PHONE)
        expect(users.input_new_password).to_be_visible(timeout=users.timeout)
        expect(users.input_new_password_repeat).to_be_visible(timeout=users.timeout)

    with allure.step("Delete added manager"):
        page.wait_for_timeout(3000)
        users.delete_added_user()

    with allure.step("Wait for alert and check alert message"):
        users.check_alert("Пользователь был удален")

    with allure.step("Check that manager deleted"):
        expect(users.input_login).to_have_value(LOGIN, timeout=users.timeout)

    with allure.step("Delete admin"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.users
@allure.title("test_add_delete_user_by_admin")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_delete_user_by_admin(base_url, page: Page) -> None:
    users = Users(page)

    NEW_NAME = NEW_LOGIN = f"auto_test_user_{datetime.now().strftime('%m%d%H%M')}{datetime.now().microsecond}"
    EMAIL = f"email_{datetime.now().microsecond}{random.randint(100, 200)}@mail.ru"
    PHONE = str(random.randint(10000000000, 99999999999))

    with allure.step("Create admin"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Go to url"):
        users.navigate(base_url)

    with allure.step("Auth with admin"):
        users.auth(LOGIN, PASSWORD)

    with allure.step("Go to users"):
        users.go_to_users_list()
    #
    with allure.step("Press button (Add User)"):
        users.press_button_add_user()

    with allure.step("Cancel by button CANCEL"):
        page.locator(BUTTON_OTMENA).click()

    with allure.step("Check"):
        expect(users.input_password).not_to_be_visible()

    with allure.step("Press button (Add User)"):
        users.press_button_add_user()

    with allure.step("Cancel by button KRESTIK"):
        users.close_modal_window()

    with allure.step("Check"):
        expect(users.input_password).not_to_be_visible()
    #
    with allure.step("Press button (Add User)"):
        users.press_button_add_user()

    with allure.step("Set user info"):
        users.set_user(
            NEW_NAME,
            NEW_LOGIN,
            PASSWORD,
            EMAIL,
            PHONE,
            "PT",
            "someComment",
            "Компания"
        )

    with allure.step("Set industry and partner for user"):
        users.set_industry_and_partner("Недвижимость","managerIM")

    with allure.step("Set STT for user"):
        users.set_stt("Русский","Deepgram","whisper")

    with allure.step("Press button (Add) in modal window"):
        users.press_button_add_in_modal()

    with allure.step("Check"):
        expect(users.input_login).to_have_value(NEW_LOGIN, timeout=users.timeout)
        expect(users.input_name).to_have_value(NEW_NAME, timeout=users.timeout)
        expect(users.input_email).to_have_value(EMAIL, timeout=users.timeout)
        expect(page.locator(SELECT_USER_LANG)).to_have_text("PT", timeout=users.timeout)
        expect(users.input_comment).to_have_text("someComment", timeout=users.timeout)
        expect(page.locator(SELECT_ROLE)).to_have_text("Компания", timeout=users.timeout)
        expect(users.select_industry).to_have_text("Недвижимость", timeout=users.timeout)
        expect(users.select_partner).to_have_text("managerIM", timeout=users.timeout)
        expect(users.input_phone).to_have_value(PHONE)
        expect(users.input_new_password).to_be_visible(timeout=users.timeout)
        expect(users.input_new_password_repeat).to_be_visible(timeout=users.timeout)

    with allure.step("Delete added user"):
        page.wait_for_timeout(3000)
        users.delete_added_user()

    with allure.step("Wait for alert and check alert message"):
        users.check_alert("Пользователь был удален")

    with allure.step("Check that user deleted"):
        expect(users.input_login).to_have_value(LOGIN, timeout=users.timeout)

    with allure.step("Delete admin"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.users
@allure.title("test_add_user_disabled_for_manager_without_right")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_add_user_disabled_for_manager_without_right")
def test_add_user_disabled_for_manager_without_right(base_url, page: Page) -> None:
    users = Users(page)

    with allure.step("Create manager without right to add"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_MANAGER, PASSWORD)

    with allure.step("Go to url"):
        users.navigate(base_url)

    with allure.step("Auth with admin"):
        users.auth(LOGIN, PASSWORD)

    with allure.step("Go to users"):
        users.go_to_users_list()

    with allure.step("Check"):
        expect(users.button_add_user).to_be_disabled()
        expect(page.locator('[class="rs-table-body-info"]')).to_contain_text("Информация отсутствует")

    with allure.step("Delete manager"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.users
@allure.title("test_add_delete_user_by_manager")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Precondition : manager should have access_rights for create and delete user")
def test_add_delete_user_by_manager(base_url, page: Page) -> None:
    users = Users(page)

    NEW_NAME = NEW_LOGIN = f"auto_test_user_{datetime.now().strftime('%m%d%H%M')}{datetime.now().microsecond}"
    EMAIL = f"email_{datetime.now().microsecond}{random.randint(100, 200)}@mail.ru"
    PHONE = str(random.randint(10000000000, 99999999999))

    with allure.step("Create manager without right to add"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_MANAGER, PASSWORD)

    with allure.step("Give created manager all rights"):
        give_manager_all_rights(API_URL, USER_ID, TOKEN)

    with allure.step("Go to url"):
        users.navigate(base_url)

    with allure.step("Auth with manager"):
        users.auth(LOGIN, PASSWORD)

    with allure.step("Go to users"):
        users.go_to_users_list()

    with allure.step("Press button (Add User)"):
        users.press_button_add_user()

    with allure.step("Set user info"):
        users.set_user(
            NEW_NAME,
            NEW_LOGIN,
            PASSWORD,
            EMAIL,
            PHONE,
            "PT",
            "someComment",
            "Компания"
        )

    with allure.step("Check that select partner not available"):
        expect(users.select_partner).not_to_be_visible(timeout=users.timeout)

    with allure.step("Set industry"):
        users.set_industry("Недвижимость")

    with allure.step("Set STT"):
        users.set_stt("Русский","IMOT.IO","Стандарт")

    with allure.step("Press button (Add) in modal window"):
        users.press_button_add_in_modal()

    with allure.step("Check"):
        expect(users.input_login).to_have_value(NEW_LOGIN, timeout=users.timeout)
        expect(users.input_name).to_have_value(NEW_NAME, timeout=users.timeout)
        expect(users.input_email).to_have_value(EMAIL, timeout=users.timeout)
        page.wait_for_timeout(3400)
        expect(page.locator(SELECT_USER_LANG)).to_have_text("PT", timeout=users.timeout)
        expect(page.get_by_text("Компания")).to_have_count(1, timeout=users.timeout)
        expect(page.get_by_text("Недвижимость")).to_have_count(1, timeout=users.timeout)
        expect(users.input_phone).to_have_value(PHONE)
        expect(users.input_new_password).to_be_visible(timeout=users.timeout)
        expect(users.input_new_password_repeat).to_be_visible(timeout=users.timeout)

    with allure.step("Delete added user"):
        users.delete_added_user()

    with allure.step("Wait for alert and check alert message"):
        users.check_alert("Пользователь был удален")

    with allure.step("Check that user deleted"):
        expect(users.input_login).to_have_value(LOGIN, timeout=users.timeout)

    with allure.step("Delete manager"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.users
@allure.title("test_add_delete_operator_by_user")
@allure.severity(allure.severity_level.NORMAL)
def test_add_delete_operator_by_user(base_url, page: Page) -> None:
    users = Users(page)

    NEW_OPERATOR_NAME = NEW_OPERATOR_LOGIN = f"auto_test_operator_{datetime.now().strftime('%m%d%H%M')}_{datetime.now().microsecond}"
    EMAIL = f"email_{datetime.now().microsecond}{random.randint(100, 200)}@mail.ru"
    PHONE = str(random.randint(10000000000, 99999999999))

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        users.navigate(base_url)

    with allure.step("Auth with user"):
        users.auth(LOGIN, PASSWORD)

    with allure.step("Go to settings"):
        users.click_settings()

    with allure.step("Go to employees"):
        users.click_employees()

    with allure.step("Press button (Add employee)"):
        users.press_button_add_user()

    with allure.step("Set operator info"):
        users.set_operator(
            NEW_OPERATOR_NAME,
            NEW_OPERATOR_LOGIN,
            PASSWORD,
            PHONE,
            EMAIL,
            EMAIL,
            "PT"
        )

    with allure.step("Press button (Add) in modal window"):
        users.press_button_add_in_modal()

    with allure.step("Wait for alert and check alert message"):
        users.check_alert("Сотрудник успешно добавлен")

    with allure.step("Check"):
        expect(users.input_name).to_have_value(NEW_OPERATOR_NAME, timeout=users.timeout)
        expect(users.input_login).to_have_value(NEW_OPERATOR_LOGIN, timeout=users.timeout)
        expect(users.input_phone).to_have_value(PHONE, timeout=users.timeout)
        expect(users.input_email).to_have_value(EMAIL, timeout=users.timeout)
        expect(page.locator(SELECT_USER_LANG)).to_have_text("PT", timeout=users.timeout)
        #expect(page.locator(INPUT_COMMENT)).to_have_text(EMAIL7, timeout=wait_until_visible)
        expect(users.input_phone).to_be_visible(timeout=users.timeout)
        expect(users.input_new_password).to_be_visible(timeout=users.timeout)
        expect(users.input_new_password_repeat).to_be_visible(timeout=users.timeout)

    with allure.step("Delete added employee"):
        users.delete_added_user()

    # with allure.step("Wait for alert and check alert message"):
    #     page.locator(SNACKBAR).wait_for(state="visible", timeout=wait_until_visible)
    #     expect(page.locator(SNACKBAR)).to_contain_text("Пользователь был удален")
    #     page.locator(SNACKBAR).wait_for(state="hidden", timeout=wait_until_visible)

    with allure.step("Check that employee deleted"):
        expect(users.button_add_user).to_be_visible(timeout=users.timeout)
        expect(page.locator(USER_LOGIN_IN_LEFT_MENU)).to_have_text(LOGIN, timeout=users.timeout)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.users
@allure.title("test_check_search")
@allure.severity(allure.severity_level.NORMAL)
def test_check_search(base_url, page: Page) -> None:
    users = Users(page)

    with allure.step("Create admin"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Go to url"):
        users.navigate(base_url)

    with allure.step("Auth with admin"):
        users.auth(LOGIN, PASSWORD)

    with allure.step("Go to users"):
        users.go_to_users_list()

    with allure.step("Fill searchString"):
        page.locator(INPUT_SEARCH).fill("ecot")

    with allure.step("Check ecotelecom visible and 1userIM not visible"):
        expect(page.get_by_text("ecotelecom", exact=True)).to_be_visible(timeout=users.timeout)
        expect(page.get_by_text("1userIM")).not_to_be_visible(timeout=users.timeout)

    with allure.step("Delete admin"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.users
@allure.title("test_check_stt_parameters_when_adding_user")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Admin checking all stt parameters while adding new user ")
def test_check_stt_parameters_when_adding_user(base_url, page: Page) -> None:
    users = Users(page)

    NEW_NAME = NEW_LOGIN = f"auto_test_user_{datetime.now().strftime('%m%d%H%M')}{datetime.now().microsecond}"
    EMAIL = f"email_{datetime.now().microsecond}{random.randint(100, 200)}@mail.ru"
    PHONE = str(random.randint(10000000000, 99999999999))

    # expected_languages = ("Английский (Великобритания)Английский (США)Испанский (Латинская Америка, Карибский регион, "
    #                       "код региона UN M49)Испанский (Испания)Французский (Франция)Португальский "
    #                       "(Бразилия)Португальский (Португалия)РусскийТурецкий (Турция)УкраинскийУзбекскийАвто")

    # expected_engines = "DeepgramGigaAMHappyscribeNLab SpeechIMOT.IOwhisperЯндексЯндекс v3"
    # expected_engines = "DeepgramgigaamHappyscribenexaraNLab SpeechIMOT.IOwhisperЯндексyandex_v3"

    alert_merge = "Опция 'Объединить дорожки в один файл' не может быть выбрана одновременно с любой из диаризаций"

    alert_diarization = "Выберите только одну диаризацию среди опций"

    action_started = "Пользователь успешно добавлен"

    with allure.step("Create admin"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Go to url"):
        users.navigate(base_url)

    with allure.step("Auth with admin"):
        users.auth(LOGIN, PASSWORD)

    with allure.step("Go to users"):
        users.go_to_users_list()

    with allure.step("Press button (Add User)"):
        users.press_button_add_user()

    with allure.step("Set user info"):
        users.set_user(
            NEW_NAME,
            NEW_LOGIN,
            PASSWORD,
            EMAIL,
            PHONE,
            "PT",
            "someComment",
            "Компания"
        )

    #  check all combinations of engines and models

    with allure.step("Click to language"):
        users.select_language.click()
        page.wait_for_selector(MENU)

    with allure.step("Check language list"):
        expect(users.menu).to_contain_text(fucking_stupidity)

    with allure.step("Choose russian language"):
        users.choose_option(132)

    with allure.step("Click to engine"):
        users.click_engine_select()

    with allure.step("Check engine list"):
        expect(users.menu).to_contain_text(expected_engines)

    # with allure.step("Click to engine"):
    #     users.click_engine_select()

    with allure.step("Choose Deepgram"):
        users.choose_option(1)

    with allure.step("Click to model"):
        users.click_model_select()

    with allure.step("Check model list"):
        expect(users.menu).to_contain_text("Обобщённаяwhisper")

    with allure.step("Select model Обобщённая"):
        users.choose_option(0)

    with allure.step("Click to model"):
        users.click_model_select()

    with allure.step("Select model whisper"):
        users.choose_option(1)

    with allure.step("Check engine parameters"):
        expect(users.select_engine).to_contain_text("Deepgram")
        expect(users.select_model).to_contain_text("whisper")
        expect(page.locator(CHECKBOX_MERGE_ALL_TO_ONE)).not_to_be_checked()
        expect(page.locator(RECOGNITION_PRIORITY).locator('[type="number"]')).to_have_value("1")
        expect(page.locator(CHECKBOX_DIARIZATION)).not_to_be_checked()
        expect(page.locator(CHECKBOX_ECONOMIZE)).not_to_be_checked()
        expect(page.locator(CHECKBOX)).to_have_count(3)

    with allure.step("Click to engine"):
        users.click_engine_select()

    with allure.step("Choose Happyscribe"):
        users.choose_option(3)

    with allure.step("Click to model"):
        users.click_model_select()

    with allure.step("Check model list"):
        expect(users.menu).to_contain_text("Стандарт")

    with allure.step("Select model Стандарт"):
        users.choose_option(0)

    with allure.step("Check engine parameters"):
        expect(users.select_engine).to_contain_text("Happyscribe")
        expect(users.select_model).to_contain_text("Стандарт")
        expect(page.locator(CHECKBOX_MERGE_ALL_TO_ONE)).not_to_be_checked()
        expect(page.locator(RECOGNITION_PRIORITY).locator('[type="number"]')).to_have_value("1")
        expect(page.locator(CHECKBOX_DIARIZATION)).not_to_be_checked()
        expect(page.locator(CHECKBOX_ECONOMIZE)).not_to_be_checked()
        expect(page.locator(CHECKBOX)).to_have_count(3)

    with allure.step("Click to engine"):
        users.click_engine_select()

    with allure.step("Choose NLab Speech"):
        users.choose_option(4)

    with allure.step("Click to model"):
        users.click_model_select()

    with allure.step("Check model list"):
        expect(users.menu).to_contain_text("ОбобщённаяЖадный")

    with allure.step("Select model Обобщённая"):
        users.choose_option(0)

    with allure.step("Click to model"):
        users.click_model_select()

    with allure.step("Select model Жадный"):
        users.choose_option(1)

    with allure.step("Check engine parameters"):
        expect(users.select_engine).to_contain_text("NLab Speech")
        expect(users.select_model).to_contain_text("Жадный")
        expect(page.locator(CHECKBOX_MERGE_ALL_TO_ONE)).not_to_be_checked()
        expect(page.locator(RECOGNITION_PRIORITY).locator('[type="number"]')).to_have_value("1")
        expect(page.locator(CHECKBOX_DIARIZATION)).not_to_be_checked()
        expect(page.locator(CHECKBOX_ECONOMIZE)).not_to_be_checked()
        expect(page.locator(CHECKBOX)).to_have_count(3)

    with allure.step("Click to engine"):
        users.click_engine_select()

    with allure.step("Choose IMOT.IO"):
        users.choose_option(5)

    with allure.step("Click to model"):
        users.click_model_select()

    with allure.step("Check model list"):
        expect(users.menu).to_contain_text("Стандарт")

    with allure.step("Select model Стандарт"):
        users.choose_option(0)

    with allure.step("Check engine parameters"):
        expect(users.select_engine).to_contain_text("IMOT.IO")
        expect(users.select_model).to_contain_text("Стандарт")
        expect(page.locator(CHECKBOX_MERGE_ALL_TO_ONE)).not_to_be_checked()
        expect(page.locator(RECOGNITION_PRIORITY).locator('[type="number"]')).to_have_value("1")
        expect(page.locator(CHECKBOX_DIARIZATION)).not_to_be_checked()
        expect(page.locator(CHECKBOX_ECONOMIZE)).not_to_be_checked()
        expect(page.locator(CHECKBOX)).to_have_count(3)

    with allure.step("Click to engine"):
        users.click_engine_select()

    with allure.step("Choose whisper"):
        users.choose_option(6)

    with allure.step("Click to model"):
        users.click_model_select()

    with allure.step("Check model list"):
        expect(users.menu).to_contain_text("Стандарт")

    with allure.step("Select model Стандарт"):
        users.choose_option(0)

    with allure.step("Check engine parameters"):
        expect(users.select_engine).to_contain_text("whisper")
        expect(users.select_model).to_contain_text("Стандарт")
        expect(page.locator(CHECKBOX_MERGE_ALL_TO_ONE)).not_to_be_checked()
        expect(page.locator(RECOGNITION_PRIORITY).locator('[type="number"]')).to_have_value("1")
        expect(page.locator(CHECKBOX_DIARIZATION)).not_to_be_checked()
        expect(page.locator(CHECKBOX_ECONOMIZE)).not_to_be_checked()
        expect(page.locator(CHECKBOX)).to_have_count(5)

    with allure.step("Click to engine"):
        users.click_engine_select()

    with allure.step("Choose Яндекс"):
        users.choose_option(7)

    with allure.step("Click to model"):
        users.click_model_select()

    with allure.step("Check model list"):
        expect(users.menu).to_contain_text("Отложенная обобщённаяОбобщённая")

    with allure.step("Select model Отложенная обобщённая"):
        users.choose_option(0)

    with allure.step("Click to model"):
        users.click_model_select()

    with allure.step("Select model Обобщённая"):
        users.choose_option(1)

    with allure.step("Check engine parameters"):
        expect(users.select_engine).to_contain_text("Яндекс")
        expect(users.select_model).to_contain_text("Обобщённая")
        expect(page.locator(CHECKBOX_MERGE_ALL_TO_ONE)).to_be_checked()
        expect(page.locator(RECOGNITION_PRIORITY).locator('[type="number"]')).to_have_value("1")
        expect(page.locator(CHECKBOX_DIARIZATION)).not_to_be_checked()
        expect(page.locator(CHECKBOX_ECONOMIZE)).not_to_be_checked()
        expect(page.locator(CHECKBOX)).to_have_count(3)

    with allure.step("Click to engine"):
        users.click_engine_select()

    with allure.step("Choose yandex_v3"):
        users.choose_option(8)

    with allure.step("Click to model"):
        users.click_model_select()

    with allure.step("Check model list"):
        expect(users.menu).to_contain_text("Отложенная обобщённаяОбобщённая")

    with allure.step("Select model Отложенная обобщённая"):
        users.choose_option(0)

    with allure.step("Click to model"):
        users.click_model_select()

    with allure.step("Select model Обобщённая"):
        users.choose_option(1)

    with allure.step("Check engine parameters"):
        expect(users.select_engine).to_contain_text("Яндекс v3")
        expect(users.select_model).to_contain_text("Обобщённая")
        expect(page.locator(CHECKBOX_MERGE_ALL_TO_ONE)).to_be_checked()
        expect(page.locator(RECOGNITION_PRIORITY).locator('[type="number"]')).to_have_value("1")
        expect(page.locator(CHECKBOX_DIARIZATION)).not_to_be_checked()
        expect(page.locator(CHECKBOX_ENGINE_DIARIZATION)).to_be_checked()
        expect(page.locator(CHECKBOX_ECONOMIZE)).not_to_be_checked()
        expect(page.locator(CHECKBOX_NORMALIZATION)).not_to_be_checked()
        expect(page.locator(CHECKBOX_PROFANITY_FILTER)).not_to_be_checked()
        expect(page.locator(CHECKBOX_LITERATURE_STYLE)).not_to_be_checked()
        expect(page.locator(CHECKBOX_PHONE_FORMATTING)).to_be_checked()
        expect(page.locator(CHECKBOX)).to_have_count(8)

    #  check save combinations

    with allure.step("Click to engine"):
        users.click_engine_select()

    with allure.step("Choose assembly_ai"):
        users.choose_option(8)

    with allure.step("Click to model"):
        users.click_model_select()

    with allure.step("Select model best"):
        users.choose_option(0)

    with allure.step("Check merge all to one checkbox"):
        page.locator(CHECKBOX_MERGE_ALL_TO_ONE).set_checked(checked=True)

    with allure.step("Try to save"):
        users.button_accept.click()

    with allure.step("Wait for alert and check alert message"):
        users.check_alert(alert_merge)

    with allure.step("Uncheck merge all to one checkbox"):
        page.locator(CHECKBOX_MERGE_ALL_TO_ONE).uncheck()

    with allure.step("Check diarization checkbox"):
        page.locator(CHECKBOX_DIARIZATION).set_checked(checked=True)

    with allure.step("Try to save"):
        users.button_accept.click()

    with allure.step("Wait for alert and check alert message"):
        users.check_alert(alert_diarization)

    with allure.step("Uncheck diarization checkbox"):
        page.locator(CHECKBOX_DIARIZATION).uncheck()

    with allure.step("Change parameters"):
        page.locator(RECOGNITION_PRIORITY).locator('[type="number"]').fill("10")
        page.locator(CHECKBOX_ECONOMIZE).set_checked(checked=True)
        #page.locator(CHECKBOX_USE_WEBHOOK).set_checked(checked=True)

    with allure.step("Press (Save)"):
        users.button_accept.click()

    with allure.step("Wait for alert and check alert message"):
        users.check_alert(action_started)

    with allure.step("Check"):
        expect(users.input_login).to_have_value(NEW_LOGIN, timeout=users.timeout)
        expect(users.input_name).to_have_value(NEW_NAME, timeout=users.timeout)
        expect(users.input_email).to_have_value(EMAIL, timeout=users.timeout)
        expect(users.input_comment).to_have_text("someComment", timeout=users.timeout)
        expect(page.locator(SELECT_USER_LANG)).to_have_text("PT", timeout=users.timeout)
        expect(users.input_phone).to_have_value(PHONE)
        expect(users.input_new_password).to_be_visible(timeout=users.timeout)
        expect(users.input_new_password_repeat).to_be_visible(timeout=users.timeout)

    with allure.step("Delete added user"):
        users.delete_added_user()

    with allure.step("Check that user deleted"):
        expect(users.input_login).to_have_value(LOGIN, timeout=users.timeout)

    with allure.step("Delete admin"):
        delete_user(API_URL, TOKEN, USER_ID)
