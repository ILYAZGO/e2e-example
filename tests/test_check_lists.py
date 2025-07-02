#from playwright.sync_api import Page, expect
from utils.variables import *
from pages.check_lists import *
from utils.create_delete_user import create_user, delete_user, give_users_to_manager, create_operator
import pytest
import allure


@pytest.mark.e2e
@pytest.mark.check_list
@allure.title("test_create_rename_update_delete_check_list")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("create,rename, update,delete check-list")
def test_create_update_delete_check_list(base_url, page: Page) -> None:
    checklists = Checklists(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        checklists.navigate(base_url)

    with allure.step("Auth"):
        checklists.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        checklists.click_markup()

    with allure.step("Go to check-lists"):
        checklists.click_check_lists()

    with allure.step("Create check-list with 2 questions and 2 answers"):
        checklists.create_check_list_with_questions_and_answers("12345", "Question1", "Question2")

    with allure.step("Fill filter"):
        checklists.add_filter_by_tags("auto_rule")

    with allure.step("Check sort order = 0"):
        expect(page.locator(INPUT_SORT_ORDER)).to_have_value("0")

    with allure.step("Change sort order"):
        checklists.change_sort_order_to("1000")

    with allure.step("Press button (Save)"):
        checklists.press_button_save()

    with allure.step("Check alert"):
        checklists.check_alert("Чек-лист добавлен")

    with allure.step("Check created"):
        expect(page.get_by_text("12345")).to_be_visible(timeout=wait_until_visible)
        expect(page.locator('[aria-label="Remove auto_rule"]')).to_have_count(1)
        expect(page.locator(INPUT_SORT_ORDER)).to_have_value("1000")

    with allure.step("Change title"):
        page.get_by_text("12345").click()
        page.locator(INPUT_CHECK_LIST_NAME).clear()
        page.locator(INPUT_CHECK_LIST_NAME).fill("654321")
        page.wait_for_timeout(500)

    with allure.step("Press button (Save)"):
        checklists.press_button_save()

    with allure.step("Check alert"):
        checklists.check_alert("Чек-лист обновлен")

    with allure.step("Check that title changed"):
        expect(page.locator(INPUT_CHECK_LIST_NAME)).to_have_value("654321")

    with allure.step("Rename from left list (Pencil)"):
        page.wait_for_selector(BUTTON_PENCIL)
        page.locator(BUTTON_PENCIL).nth(1).click()
        page.wait_for_timeout(1000)
        page.locator('[class*="styles_titleBlock"]').locator(INPUT_LEFT_CHECK_LIST_NAME).clear()
        page.locator('[class*="styles_titleBlock"]').locator(INPUT_LEFT_CHECK_LIST_NAME).fill("98765")
        page.wait_for_timeout(300)
        page.locator(BUTTON_SAVE_EDITED_NAME).click()
        page.wait_for_timeout(300)

    with allure.step("Check rename was successful"):
        expect(page.get_by_text("98765")).to_be_visible(timeout=wait_until_visible)

    with allure.step("Update check-list (change first question)"):
        page.get_by_text("98765").click()
        page.locator(INPUT_FIRST_QUESTION).clear()
        page.locator(INPUT_FIRST_QUESTION).fill("654321")
        page.wait_for_timeout(500)

    with allure.step("Uncheck autogerenate report checkbox"):
        page.locator('[id="checklistGenerateReport"]').click()

    with allure.step("Press button (Save)"):
        checklists.press_button_save()

    with allure.step("Check alert"):
        checklists.check_alert("Чек-лист обновлен")

    with allure.step("Reload page and check that update saved"):
        page.reload()
        page.wait_for_selector(INPUT_FIRST_QUESTION)
        expect(page.locator(INPUT_FIRST_QUESTION)).to_have_value("654321")
        expect(page.locator(CHECK_BOX_AUTOGENEREATE_REPORT)).not_to_be_checked()
        expect(page.locator('[aria-label="Remove auto_rule"]')).to_have_count(1)

    with allure.step("Create appriser"):
        checklists.create_appriser("Appriser", "5")

    with allure.step("Check autogerenate report checkbox"):
        page.locator(CHECK_BOX_AUTOGENEREATE_REPORT).click()

    with allure.step("Press button (Save)"):
        checklists.press_button_save()

    with allure.step("Check alert"):
        checklists.check_alert("Чек-лист обновлен")

    with allure.step("Check that appriser created"):
        page.reload()
        page.wait_for_selector('[name="appraisers.0.title"]')
        expect(page.locator('[name="appraisers.0.title"]')).to_have_value("Appriser")
        expect(page.locator(CHECK_BOX_AUTOGENEREATE_REPORT)).to_be_checked()

    with allure.step("Delete appriser"):
        checklists.delete_appriser()

    with allure.step("Press button (Save)"):
        checklists.press_button_save()

    with allure.step("Check alert"):
        checklists.check_alert("Чек-лист обновлен")

    with allure.step("Check that appriser deleted"):
        page.reload()
        page.wait_for_selector(INPUT_CHECK_LIST_NAME, timeout=wait_until_visible)
        expect(page.locator('[name="appraisers.0.title"]')).not_to_be_visible()

    with allure.step("Delete created check-list"):
        checklists.delete_check_list()

    with allure.step("Wait for alert and check alert message"):
        checklists.check_alert("Чек-лист удален")

    with allure.step("Delete created check-list"):
        checklists.delete_check_list()

    with allure.step("Wait for alert and check alert message"):
        checklists.check_alert("Чек-лист удален")

    with allure.step("Check that deleted"):
        page.wait_for_selector(NI4EGO_NE_NAYDENO, timeout=wait_until_visible)
        expect(page.locator(NI4EGO_NE_NAYDENO)).to_be_visible(timeout=wait_until_visible)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.check_list
@allure.title("test_check_old_check_list")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Check old checklist from ecotelecom")
def test_check_old_check_list(base_url, page: Page) -> None:
    checklists = Checklists(page)

    with allure.step("Go to url"):
        checklists.navigate(base_url)

    with allure.step("Auth like Ecotelecom"):
        checklists.auth(ECOTELECOM, ECOPASS)

    with allure.step("Go to markup"):
        checklists.click_markup()

    with allure.step("Go to check-lists"):
        checklists.click_check_lists()

    with allure.step("Select first available check-list"):
        page.locator('[class*=groupItem]').first.click()
        page.wait_for_selector(INPUT_CHECK_LIST_NAME, timeout=wait_until_visible)

    with allure.step("Check that first available check-list have appriser (seems strange, but works)"):
        expect(page.locator('[name="appraisers.0.title"]')).to_be_visible()


@pytest.mark.e2e
@pytest.mark.check_list
@allure.title("test_import_check_list_by_admin")
@allure.severity(allure.severity_level.CRITICAL)
def test_import_check_list_by_admin(base_url, page: Page) -> None:
    checklists = Checklists(page)

    with allure.step("Create admin"):
        USER_ID_ADMIN, TOKEN_ADMIN, LOGIN_ADMIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Create user"):
        USER_ID_USER, TOKEN_USER, LOGIN_USER = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        checklists.navigate(base_url)

    with allure.step("Auth"):
        checklists.auth(LOGIN_ADMIN, PASSWORD)

    with allure.step("Go to user import to"):
        checklists.go_to_user(LOGIN_USER)

    with allure.step("Go to markup"):
        checklists.click_markup()

    with allure.step("Go to check-lists"):
        checklists.click_check_lists()

    with allure.step("Press import button"):
        checklists.press_import_checklists()

    with allure.step("Choose user for import"):
        checklists.choose_user_import_from("importFrom")

    with allure.step("Import first"):
        page.wait_for_timeout(1000)
        page.locator(MODAL_WINDOW).locator(CHECKBOX).nth(0).check()
        page.wait_for_timeout(1000)

    with allure.step("Press (Go on)"):
        page.get_by_role("button", name="Продолжить").click()
        page.wait_for_timeout(1000)

    with allure.step("Import second"):
        page.locator(MODAL_WINDOW).locator(CHECKBOX).nth(1).check()
        page.wait_for_timeout(1000)

    with allure.step("Go to new check-lists"):
        page.get_by_role("button", name="К новым чек-листам").click()
        page.wait_for_selector(MODAL_WINDOW, state="hidden")

    with allure.step("Check that check-lists imported"):
        expect(page.get_by_text("12345")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("98765")).to_be_visible(timeout=wait_until_visible)

    with allure.step("Delete first check-list"):
        checklists.delete_check_list()

    with allure.step("Wait for alert and check alert message"):
        checklists.check_alert("Чек-лист удален")

    with allure.step("Delete second check-list"):
        checklists.delete_check_list()

    with allure.step("Wait for alert and check alert message"):
        checklists.check_alert("Чек-лист удален")

    with allure.step("Delete third check-list"):
        checklists.delete_check_list()

    with allure.step("Wait for alert and check alert message"):
        checklists.check_alert("Чек-лист удален")

    with allure.step("Check that deleted"):
        expect(page.get_by_text("auto_call_ch_list")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("12345")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("98765")).not_to_be_visible(timeout=wait_until_visible)

    with allure.step("Delete admin"):
        delete_user(API_URL, TOKEN_ADMIN, USER_ID_ADMIN)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN_USER, USER_ID_USER)


@pytest.mark.e2e
@pytest.mark.check_list
@allure.title("test_import_check_list_by_manager")
@allure.severity(allure.severity_level.CRITICAL)
def test_import_check_list_by_manager(base_url, page: Page) -> None:
    checklists = Checklists(page)

    with allure.step("Create manager"):
        USER_ID_MANAGER, TOKEN_MANAGER, LOGIN_MANAGER = create_user(API_URL, ROLE_MANAGER, PASSWORD)

    with allure.step("Create user for import"):
        USER_ID_USER, TOKEN_USER, LOGIN_USER = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Give user for import to manager"):
        give_users_to_manager(API_URL, USER_ID_MANAGER, [USER_ID_USER, importFrom_user_id], TOKEN_MANAGER)

    with allure.step("Go to url"):
        checklists.navigate(base_url)

    with allure.step("Auth"):
        checklists.auth(LOGIN_MANAGER, PASSWORD)

    with allure.step("Go to user import to"):
        checklists.go_to_user(LOGIN_USER)

    with allure.step("Go to markup"):
        checklists.click_markup()

    with allure.step("Go to check-lists"):
        checklists.click_check_lists()

    with allure.step("Press import button"):
        checklists.press_import_checklists()

    with allure.step("Choose user for import"):
        checklists.choose_user_import_from("importFrom")

    with allure.step("Import first"):
        page.wait_for_timeout(1000)
        page.locator(MODAL_WINDOW).locator(CHECKBOX).nth(0).check()
        page.wait_for_timeout(1000)

    with allure.step("Press (Go on)"):
        page.get_by_role("button", name="Продолжить").click()
        page.wait_for_timeout(1000)

    with allure.step("Import second"):
        page.locator(MODAL_WINDOW).locator(CHECKBOX).nth(1).check()
        page.wait_for_timeout(1000)

    with allure.step("Go to new chec-lists"):
        page.get_by_role("button", name="К новым чек-листам").click()
        page.wait_for_selector(MODAL_WINDOW, state="hidden")

    with allure.step("Check that check-lists imported"):
        expect(page.get_by_text("12345")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("98765")).to_be_visible(timeout=wait_until_visible)

    with allure.step("Delete first check-list"):
        checklists.delete_check_list()

    with allure.step("Wait for alert and check alert message"):
        checklists.check_alert("Чек-лист удален")

    with allure.step("Delete second check-list"):
        checklists.delete_check_list()

    with allure.step("Wait for alert and check alert message"):
        checklists.check_alert("Чек-лист удален")

    with allure.step("Delete third check-list"):
        checklists.delete_check_list()

    with allure.step("Wait for alert and check alert message"):
        checklists.check_alert("Чек-лист удален")

    with allure.step("Check that deleted"):
        expect(page.get_by_text("auto_call_ch_list")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("12345")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("98765")).not_to_be_visible(timeout=wait_until_visible)

    with allure.step("Delete manager"):
        delete_user(API_URL, TOKEN_MANAGER, USER_ID_MANAGER)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN_USER, USER_ID_USER)


@pytest.mark.e2e
@pytest.mark.check_list
@allure.title("test_import_check_list_disabled_for_user")
@allure.severity(allure.severity_level.NORMAL)
def test_import_check_list_disabled_for_user(base_url, page: Page) -> None:
    checklists = Checklists(page)

    with allure.step("Create user"):
        USER_ID_USER, TOKEN_USER, LOGIN_USER = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        checklists.navigate(base_url)

    with allure.step("Auth"):
        checklists.auth(LOGIN_USER, PASSWORD)

    with allure.step("Go to markup"):
        checklists.click_markup()

    with allure.step("Go to check-lists"):
        checklists.click_check_lists()

    with allure.step("Check that for user check-list import disabled"):
        expect(page.locator(BUTTON_IMPORT_CHECK_LIST)).not_to_be_visible()

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN_USER, USER_ID_USER)


@pytest.mark.e2e
@pytest.mark.check_list
@allure.title("test_compare_check_lists_by_user")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("User has two check lists with different parameters. when he switch between them, all parameters changing")
def test_compare_check_lists_by_user(base_url, page: Page) -> None:
    checklists = Checklists(page)

    with allure.step("Go to url"):
        checklists.navigate(base_url)

    with allure.step("Auth with user for check comparelogin"):
        checklists.auth(USER_FOR_CHECK, PASSWORD)

    with allure.step("Go to markup"):
        checklists.click_markup()

    with allure.step("Go to check-lists"):
        checklists.click_check_lists()

    with allure.step("Select first available check-list"):
        page.locator('[class*="styles_dpBothBox_"]').get_by_text("firstchecklist").click()
        page.wait_for_selector(INPUT_CHECK_LIST_NAME, timeout=wait_until_visible)

    with allure.step("Check parameters for first check list"):
        expect(page.locator(INPUT_CHECK_LIST_NAME)).to_have_value("firstchecklist")
        expect(page.locator('[value="CALL"]')).to_have_count(1)
        expect(page.locator('[aria-label="Remove firstrule"]')).to_have_count(1)
        expect(page.locator('[aria-label="Remove secondrule"]')).to_have_count(2)
        expect(page.locator('[name="appraisers.0.title"]')).to_have_value("mark1")
        expect(page.locator('[name="appraisers.0.points"]')).to_have_value("1")
        expect(page.locator('[name="questions.0.title"]')).to_have_value("question1")
        expect(page.locator('[name="questions.0.answers.0.answer"]')).to_have_value("answer1")
        expect(page.locator('[name="questions.0.answers.0.point"]')).to_have_value("2")

    with allure.step("Switch to second check-list"):
        page.locator('[class*="styles_dpBothBox_"]').get_by_text("secondchecklist").click()
        page.wait_for_timeout(1000)

    with allure.step("Check that parameters changed"):
        expect(page.locator(INPUT_CHECK_LIST_NAME)).to_have_value("secondchecklist")
        expect(page.locator('[value="DEAL"]')).to_have_count(1)
        expect(page.locator('[aria-label="Remove firstrule"]')).to_have_count(2)
        expect(page.locator('[aria-label="Remove >100"]')).to_have_count(1)
        expect(page.locator('[name="appraisers.0.title"]')).to_have_value("mark2")
        expect(page.locator('[name="appraisers.0.points"]')).to_have_value("7")
        expect(page.locator('[name="questions.0.title"]')).to_have_value("question2")
        expect(page.locator('[name="questions.0.answers.0.answer"]')).to_have_value("answer2")
        expect(page.locator('[name="questions.0.answers.0.point"]')).to_have_value("9")


@pytest.mark.e2e
@pytest.mark.check_list
@allure.title("test_copy_check_list_by_user")
@allure.severity(allure.severity_level.NORMAL)
def test_copy_check_list_by_user(base_url, page: Page) -> None:
    checklists = Checklists(page)

    with allure.step("Create user"):
        USER_ID_USER, TOKEN_USER, LOGIN_USER = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        checklists.navigate(base_url)

    with allure.step("Auth"):
        checklists.auth(LOGIN_USER, PASSWORD)

    with allure.step("Go to markup"):
        checklists.click_markup()

    with allure.step("Go to check-lists"):
        checklists.click_check_lists()

    with allure.step("Create check-list"):
        checklists.create_check_list_with_questions_and_answers("Original", "first", "second")

    with allure.step("Add filter"):
        checklists.add_filter_by_tags("auto_rule")

    with allure.step("Check sort order = 0"):
        expect(page.locator(INPUT_SORT_ORDER)).to_have_value("0")

    with allure.step("Change sort order"):
        checklists.change_sort_order_to("1000")

    with allure.step("Create appriser"):
        checklists.create_appriser("App", "5")

    with allure.step("Save checkList"):
        checklists.press_button_save()

    with allure.step("Check alert"):
        checklists.check_alert("Чек-лист добавлен")

    with allure.step("Press (copy)"):
        checklists.press_button_copy()

    with allure.step("Check copy modal"):
        expect(page.locator(MODAL_WINDOW).get_by_text("Original")).to_have_count(1)
        expect(page.locator(MODAL_WINDOW).locator(BUTTON_ACCEPT)).to_be_disabled()
        expect(page.locator(MODAL_WINDOW).locator(BUTTON_OTMENA)).to_be_enabled()

    with allure.step("Change name for copy"):
        checklists.change_name_for_copy("Copy")

    with allure.step("Press (create)"):
        checklists.button_accept.click()

    with allure.step("Check alert"):
        checklists.check_alert("Чек-лист добавлен")

    with allure.step("Check copy"):
        expect(page.get_by_text("Copy")).to_have_count(1)
        expect(page.locator(INPUT_FIRST_QUESTION)).to_have_value("first")
        expect(page.locator('[name="questions.0.answers.0.point"]')).to_have_value("1")
        expect(page.locator('[name="questions.0.answers.1.point"]')).to_have_value("2")
        expect(page.get_by_text("auto_rule")).to_have_count(1)
        expect(page.locator('[name="appraisers.0.title"]')).to_have_value("App")
        expect(page.locator('[name="appraisers.0.points"]')).to_have_value("5")
        expect(page.locator(INPUT_SORT_ORDER)).to_have_value("1000")

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN_USER, USER_ID_USER)