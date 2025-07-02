#from playwright.sync_api import Page, expect
from utils.variables import *
from pages.dicts import *
from utils.create_delete_user import create_user, delete_user, give_users_to_manager
import pytest
import allure


@pytest.mark.e2e
@pytest.mark.dictionaries
@allure.title("test_add_dict_inside_group")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Create dict inside group by user")
def test_add_dict_inside_group(base_url, page: Page) -> None:
    dicts = Dicts(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        dicts.navigate(base_url)

    with allure.step("Auth with user"):
        dicts.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        dicts.click_markup()

    with allure.step("Go to dicts"):
        dicts.click_to_dicts()

    with allure.step("Press (Create group)"):
        dicts.press_create_group()

    with allure.step("Check that (Add) button disabled"):
        expect(dicts.button_accept).to_be_disabled()

    with allure.step("Add group name"):
        dicts.input_new_group_name("12345")

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Группа добавлена")

    with allure.step("Click on group"):
        page.locator(CLICK_ON_GROUP).click()

    with allure.step("Create dict"):
        dicts.create_dict("98765", "random_text")

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Словарь добавлен")

    with allure.step("Save created dict"):
        page.get_by_role("button", name="Сохранить").click()

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Словарь был обновлен")

    with allure.step("Check that dict created"):
        expect(page.locator(NAZVANIE_SLOVARYA)).to_have_value("98765")

    with allure.step("Check that dict belongs to parent group"):
        expect(page.get_by_text("12345").nth(1)).to_have_text("12345")
        page.wait_for_timeout(300)

    with allure.step("Rename dict"):
        page.locator(NAZVANIE_SLOVARYA).clear()
        page.locator(NAZVANIE_SLOVARYA).fill("newName")
        page.get_by_role("button", name="Сохранить").click()

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Словарь был обновлен")

    with allure.step("Check that name changed"):
        expect(page.locator(NAZVANIE_SLOVARYA)).to_have_value("newName")
        expect(page.locator('[data-testid="test"]')).to_have_text("newName")

    with allure.step("Delete rule"):
        delete_rule_or_dict(page)

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Словарь удалён")

    with allure.step("Delete group"):
        delete_group(page)

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Группа удалена")

    with allure.step("Check that group deleted (group will not be delete if you didnt delete dict)"):
        expect(page.get_by_text("12345")).not_to_be_visible()

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.dictionaries
@allure.title("test_add_dict_outside_group_disabled")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_add_dict_outside_group_disabled")
def test_add_dict_outside_group_disabled(base_url, page: Page) -> None:
    dicts = Dicts(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        dicts.navigate(base_url)

    with allure.step("Auth with user"):
        dicts.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        dicts.click_markup()

    with allure.step("Go to dicts"):
        dicts.click_to_dicts()

    with allure.step("Check that disabled"):
        expect(page.locator(TOOLTIP_BUTTON_DOBAVIT_SLOVAR)).to_have_count(1)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.dictionaries
@allure.title("test_add_group_and_dict_with_same_name")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_add_group_and_dict_with_same_name. You cant do group and dict with same name (409 status code)")
def test_add_group_and_dict_with_same_name(base_url, page: Page) -> None:
    dicts = Dicts(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        dicts.navigate(base_url)

    with allure.step("Auth with user"):
        dicts.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        dicts.click_markup()

    with allure.step("Go to dicts"):
        dicts.click_to_dicts()

    with allure.step("Press (Create group)"):
        dicts.press_create_group()

    with allure.step("Check that (Add) button disabled"):
        expect(dicts.button_accept).to_be_disabled()

    with allure.step("Create group with same name"):
        dicts.input_new_group_name("auto_dict_group")

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Такая группа уже существует")

    with allure.step("Click at existed group"):
        page.locator(GROUP_LIST).get_by_text("auto_dict_group").click()
        page.wait_for_selector(TOOLTIP_BUTTON_DOBAVIT_SLOVAR, state='hidden')

    with allure.step("Try to create rule with same name"):
        dicts.create_dict_without_text("auto_dict")

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Такой словарь уже существует")

    with allure.step("Reload page"):
        dicts.reload_page()

    with allure.step("Check that tag with same name was not created"):
        expect(page.get_by_text("auto_dict_group", exact=True)).to_have_count(1, timeout=wait_until_visible)
        expect(page.get_by_text("auto_dict", exact=True)).to_have_count(1, timeout=wait_until_visible)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.dictionaries
@allure.title("test_add_dict_group_rename_delete")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_add_dict_group_rename_delete")
def test_add_dict_group_rename_delete(base_url, page: Page) -> None:
    dicts = Dicts(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        dicts.navigate(base_url)

    with allure.step("Auth with user"):
        dicts.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        dicts.click_markup()

    with allure.step("Go to dicts"):
        dicts.click_to_dicts()
    #
    with allure.step("Press (Add group)"):
        dicts.press_create_group()

    with allure.step("Press (Cancel)"):
        page.locator(BUTTON_OTMENA).click()

    with allure.step("Check canceled"):
        expect(page.locator(GROUP_ITEMS)).to_have_count(2)

    with allure.step("Press (Add group)"):
        dicts.press_create_group()

    with allure.step("Press (cross button)"):
        dicts.button_cross.click()

    with allure.step("Check canceled"):
        expect(page.locator(GROUP_ITEMS)).to_have_count(2)

    with allure.step("Press (Create group)"):
        dicts.press_create_group()

    with allure.step("Check that (Add) button disabled"):
        expect(dicts.button_accept).to_be_disabled()

    with allure.step("Add group name"):
        dicts.input_new_group_name("12345")

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Группа добавлена")

    with allure.step("Rename group"):
        page.wait_for_selector(BUTTON_PENCIL, timeout=wait_until_visible)
        page.locator(BUTTON_PENCIL).first.click()
        page.locator(INPUT_EDIT_GROUP_NAME).fill("54321")
        page.locator(BUTTON_SAVE_EDITED_NAME).get_by_role("button").first.click()

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Название группы изменено")

    with allure.step("Check group created and renamed"):
        expect(page.get_by_text("54321")).to_be_visible(timeout=wait_until_visible)

    with allure.step("Delete group"):
        dicts.button_korzina.first.click()

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Группа удалена")

    with allure.step("Check deleted"):
        expect(page.get_by_text("54321")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("auto_dict_group")).to_be_visible(timeout=wait_until_visible)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.dictionaries
@allure.title("test_check_dict_type")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_check_dict_type")
def test_check_dict_type(base_url, page: Page) -> None:
    dicts = Dicts(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        dicts.navigate(base_url)

    with allure.step("Auth with user"):
        dicts.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        dicts.click_markup()

    with allure.step("Go to dicts"):
        dicts.click_to_dicts()

    with allure.step("Press (Create group)"):
        dicts.press_create_group()

    with allure.step("Check that (Add) button disabled"):
        expect(dicts.button_accept).to_be_disabled()

    with allure.step("Add group name"):
        dicts.input_new_group_name("12345")

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Группа добавлена")

    with allure.step("Click on group"):
        page.locator(CLICK_ON_GROUP).click()

    with allure.step("Create dict"):
        dicts.create_dict("98765", "random_text")

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Словарь добавлен")

    with allure.step("Save created dict"):
        page.get_by_role("button", name="Сохранить").click()

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Словарь был обновлен")

    with allure.step("Check created dict name"):
        expect(page.locator(NAZVANIE_SLOVARYA)).to_have_value("98765")

    with allure.step("Check created dict parent group"):
        expect(page.get_by_text("12345").nth(1)).to_have_text("12345")
        page.wait_for_timeout(500)

    with allure.step("Change dict type"):
        dicts.change_dict_type("Обычный словарь", "Словарь автозамен")

    with allure.step("Press (Save)"):
        page.get_by_role("button", name="Сохранить").click()

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Словарь был обновлен")

    with allure.step("Reload page and go to dict"):
        dicts.reload_page()
        page.wait_for_timeout(2000)
        page.locator('[data-testid="test"]').click()
        page.wait_for_selector(INPUT_WORDS_LIST, timeout=wait_until_visible)

    with allure.step("Check that dict type changed and saved"):
        expect(page.get_by_text("Словарь автозамен")).to_have_count(1)

    with allure.step("Change dict type"):
        dicts.change_dict_type("Словарь автозамен", "Словарь грамматики")

    with allure.step("Press (Save)"):
        page.get_by_role("button", name="Сохранить").click()

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Словарь был обновлен")

    with allure.step("Reload page and go to dict"):
        dicts.reload_page()
        page.wait_for_timeout(1000)
        page.locator('[data-testid="test"]').click()
        page.wait_for_selector(INPUT_WORDS_LIST, timeout=wait_until_visible)

    with allure.step("Check that dict type changed and saved"):
        expect(page.get_by_text("Словарь грамматики")).to_have_count(1)

    with allure.step("Change dict type"):
        dicts.change_dict_type("Словарь грамматики", "Словарь правил грамматики")

    with allure.step("Press (Save)"):
        page.get_by_role("button", name="Сохранить").click()

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Словарь был обновлен")

    with allure.step("Reload page and go to dict"):
        dicts.reload_page()
        page.wait_for_timeout(1000)
        page.locator('[data-testid="test"]').click()
        page.wait_for_selector(INPUT_WORDS_LIST, timeout=wait_until_visible)

    with allure.step("Check that dict type changed and saved"):
        expect(page.get_by_text("Словарь правил грамматики")).to_have_count(1)

    with allure.step("Change dict type"):
        dicts.change_dict_type("Словарь правил грамматики", "Обычный словарь")

    with allure.step("Press (Save)"):
        page.get_by_role("button", name="Сохранить").click()

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Словарь был обновлен")

    with allure.step("Reload page and go to dict"):
        dicts.reload_page()
        page.wait_for_timeout(1000)
        page.locator('[data-testid="test"]').click()
        page.wait_for_selector(INPUT_WORDS_LIST, timeout=wait_until_visible)

    with allure.step("Check that dict type changed and saved"):
        expect(page.get_by_text("Обычный словарь")).to_have_count(1)

    with allure.step("Delete rule"):
        delete_rule_or_dict(page)

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Словарь удалён")

    with allure.step("Delete group"):
        delete_group(page)

    with allure.step("Wait and check snack bar"):
        dicts.check_alert("Группа удалена")

    with allure.step("Check that dict and group deleted"):
        expect(page.get_by_text("12345")).not_to_be_visible()

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.dictionaries
@allure.title("test_check_old_dict")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("https://task.imot.io/browse/DEV-1784   check old dict from ecotelecom")
def test_check_old_dict(base_url, page: Page) -> None:
    dicts = Dicts(page)

    with allure.step("Go to url"):
        dicts.navigate(base_url)

    with allure.step("Auth with ECOTELECOM"):
        dicts.auth(ECOTELECOM, ECOPASS)

    with allure.step("Go to markup"):
        dicts.click_markup()

    with allure.step("Go to dicts"):
        dicts.click_to_dicts()
        page.wait_for_selector('[href*="/tags?group"]', timeout=wait_until_visible)

    with allure.step("Click to first dict"):
        page.locator('[data-testid="test"]').first.click()
        page.wait_for_selector(NAZVANIE_SLOVARYA, timeout=wait_until_visible)

    with allure.step("Check that dict opened"):
        expect(page.locator(INPUT_WORDS_LIST)).to_be_visible(timeout=wait_until_visible)


@pytest.mark.e2e
@pytest.mark.dictionaries
@allure.title("test_import_dict_disabled_for_user")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_import_dict_disabled_for_user")
def test_import_dict_disabled_for_user(base_url, page: Page) -> None:
    dicts = Dicts(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        dicts.navigate(base_url)

    with allure.step("Auth with user"):
        dicts.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        dicts.click_markup()

    with allure.step("Go to dicts"):
        dicts.click_to_dicts()

    with allure.step("Check"):
        expect(dicts.button_import_dicts).not_to_be_visible()

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.dictionaries
@allure.title("test_import_group_and_dict_by_admin")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Precondition: user  importFrom with group 11111 rule 22222 inside, with rule 33333 without group")
def test_import_group_and_dict_by_admin(base_url, page: Page) -> None:
    dicts = Dicts(page)

    with allure.step("Create admin"):
        USER_ID_ADMIN, TOKEN_ADMIN, LOGIN_ADMIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Create user"):
        USER_ID_USER, TOKEN_USER, LOGIN_USER = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        dicts.navigate(base_url)

    with allure.step("Auth with admin"):
        dicts.auth(LOGIN_ADMIN, PASSWORD)

    with allure.step("Go to user"):
        dicts.go_to_user(LOGIN_USER)

    with allure.step("Go to markup"):
        dicts.click_markup()

    with allure.step("Go to dicts"):
        dicts.click_to_dicts()

    with allure.step("Press (Import dicts) button"):
        dicts.button_import_dicts.click()

    with allure.step("Select user ImportFrom in modal window"):
        dicts.choose_user_import_from("importFrom")

    with allure.step("Check that search string visible"):
        expect(page.locator('[data-testid="markup_importNav_tags"]')).not_to_be_visible()
        expect(page.locator('[data-testid="markup_importNav_dicts"]')).not_to_be_visible()
        expect(page.locator('[data-testid="markup_dicts_importSearch}"]')).to_be_visible()
        expect(page.locator('[data-testid="markup_importNav_gpt"]')).not_to_be_visible()

    with allure.step("Import dict and group with dict"):
        page.wait_for_timeout(1000)
        page.locator('[class*="CopyMode_copyModeView__popup_"]').locator(CHECKBOX).nth(1).click()
        page.get_by_role("button", name="Продолжить").click()
        page.wait_for_timeout(1000)
        page.locator('[class*="CopyMode_copyModeView__popup_"]').locator(CHECKBOX).nth(3).click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="К новым словарям").click()
        page.wait_for_timeout(2000)

    with allure.step("Check that import successful"):
        expect(page.locator("//p[normalize-space()='44444']")).to_be_visible(timeout=wait_until_visible)
        #expect(page.get_by_text("44444")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("55555")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("66666")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("Неотсортированные")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("1 словарь")).to_have_count(count=3, timeout=wait_until_visible)

    with allure.step("Click on rule"):
        page.get_by_text("55555").click()

    with allure.step("Delete rule"):
        delete_rule_or_dict(page)

    with allure.step("Wait for snackbar and check"):
        dicts.check_alert("Словарь удалён")

    with allure.step("Delete group"):
        dicts.button_korzina.nth(0).click()

    with allure.step("Wait for snackbar and check"):
        dicts.check_alert("Группа удалена")

    with allure.step("Click on rule"):
        page.get_by_text("66666").click()

    with allure.step("Delete rule"):
        delete_rule_or_dict(page)

    with allure.step("Wait for snackbar and check"):
        dicts.check_alert("Словарь удалён")

    with allure.step("Delete group"):
        dicts.button_korzina.nth(1).click()

    with allure.step("Wait for snackbar and check"):
        dicts.check_alert("Группа удалена")

    with allure.step("Check that deleted"):
        expect(page.locator("//p[normalize-space()='44444']")).not_to_be_visible(timeout=wait_until_visible)
        #expect(page.get_by_text("44444")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("55555")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("66666")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("Неотсортированные")).not_to_be_visible(timeout=wait_until_visible)

    with allure.step("Delete admin"):
        delete_user(API_URL, TOKEN_ADMIN, USER_ID_ADMIN)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN_USER, USER_ID_USER)


@pytest.mark.e2e
@pytest.mark.dictionaries
@allure.title("test_import_group_and_dict_by_manager")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Precondition: user  importFrom with group 11111 rule 22222 inside, with rule 33333 without group")
def test_import_group_and_dict_by_manager(base_url, page: Page) -> None:
    dicts = Dicts(page)

    with allure.step("Create user"):
        USER_ID_USER, TOKEN_USER, LOGIN_USER = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Create manager"):
        USER_ID_MANAGER, TOKEN_MANAGER, LOGIN_MANAGER = create_user(API_URL, ROLE_MANAGER, PASSWORD)

    with allure.step("give user to manager"):
        give_users_to_manager(API_URL, USER_ID_MANAGER, [USER_ID_USER, importFrom_user_id], TOKEN_MANAGER)

    with allure.step("Go to url"):
        dicts.navigate(base_url)

    with allure.step("Auth with manager"):
        dicts.auth(LOGIN_MANAGER, PASSWORD)

    with allure.step("Go to user"):
        dicts.go_to_user(LOGIN_USER)

    with allure.step("Go to markup"):
        dicts.click_markup()

    with allure.step("Go to dicts"):
        dicts.click_to_dicts()

    with allure.step("Press (Import dicts) button"):
        dicts.button_import_dicts.click()

    with allure.step("Select user ImportFrom in modal window"):
        dicts.choose_user_import_from("importFrom")

    with allure.step("Check that search string visible"):
        expect(page.locator('[data-testid="markup_importNav_tags"]')).not_to_be_visible()
        expect(page.locator('[data-testid="markup_importNav_dicts"]')).not_to_be_visible()
        expect(page.locator('[data-testid="markup_dicts_importSearch}"]')).to_be_visible()
        expect(page.locator('[data-testid="markup_importNav_gpt"]')).not_to_be_visible()

    with allure.step("Import dict and group with dict"):
        page.locator('[class*="CopyMode_copyModeView__popup_"]').locator(CHECKBOX).nth(1).click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Продолжить").click()
        page.wait_for_timeout(1000)
        page.locator('[class*="CopyMode_copyModeView__popup_"]').locator(CHECKBOX).nth(3).click()
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="К новым словарям").click()
        page.wait_for_timeout(2000)

    with allure.step("Check that import successful"):
        expect(page.locator("//p[normalize-space()='44444']")).to_be_visible(timeout=wait_until_visible)
        #expect(page.get_by_text("44444")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("55555")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("66666")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("Неотсортированные")).to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("1 словарь")).to_have_count(count=3, timeout=wait_until_visible)

    with allure.step("Click on rule"):
        page.get_by_text("55555").click()

    with allure.step("Delete rule"):
        delete_rule_or_dict(page)

    with allure.step("Wait for snackbar and check"):
        dicts.check_alert("Словарь удалён")

    with allure.step("Delete group"):
        dicts.button_korzina.nth(0).click()

    with allure.step("Wait for snackbar and check"):
        dicts.check_alert("Группа удалена")

    with allure.step("Click on rule"):
        page.get_by_text("66666").click()

    with allure.step("Delete rule"):
        delete_rule_or_dict(page)

    with allure.step("Wait for snackbar and check"):
        dicts.check_alert("Словарь удалён")

    with allure.step("Delete group"):
        dicts.button_korzina.nth(1).click()

    with allure.step("Wait for snackbar and check"):
        dicts.check_alert("Группа удалена")

    with allure.step("Check that deleted"):
        expect(page.locator("//p[normalize-space()='44444']")).not_to_be_visible(timeout=wait_until_visible)
        #expect(page.get_by_text("44444")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("55555")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("66666")).not_to_be_visible(timeout=wait_until_visible)
        expect(page.get_by_text("Неотсортированные")).not_to_be_visible(timeout=wait_until_visible)

    with allure.step("Delete manager"):
        delete_user(API_URL, TOKEN_MANAGER, USER_ID_MANAGER)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN_USER, USER_ID_USER)


@pytest.mark.e2e
@pytest.mark.dictionaries
@allure.title("test_compare_dicts_by_user")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("User has two dicts with different parameters. when he switch between them, all parameters changing")
def test_compare_dicts_by_user(base_url, page: Page) -> None:
    dicts = Dicts(page)

    with allure.step("Go to url"):
        dicts.navigate(base_url)

    with allure.step("Auth with user for check comparelogin"):
        dicts.auth(USER_FOR_CHECK, PASSWORD)

    with allure.step("Go to markup"):
        dicts.click_markup()

    with allure.step("Go to dicts"):
        dicts.click_to_dicts()

    with allure.step("Go to first rule"):
        page.get_by_text("firstdict").click()
        page.wait_for_selector(INPUT_WORDS_LIST, timeout=wait_until_visible)

    with allure.step("Check filters and other inside rule"):
        expect(page.locator(NAZVANIE_SLOVARYA)).to_have_value("firstdict")
        expect(page.locator(INPUT_WORDS_LIST)).to_have_text("few words")
        expect(page.get_by_text("Обычный словарь")).to_have_count(1)

    with allure.step("Change rule"):
        page.wait_for_timeout(500)
        page.get_by_text("seconddict").click()
        page.wait_for_timeout(2000)

    with allure.step("Check filters and other inside rule was changed"):
        expect(page.locator(NAZVANIE_SLOVARYA)).to_have_value("seconddict")
        expect(page.locator(INPUT_WORDS_LIST)).to_have_text("some text")
        expect(page.get_by_text("Словарь автозамен")).to_have_count(1)


@pytest.mark.e2e
@pytest.mark.dictionaries
@allure.title("test_check_dicts_search_and_sort")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_check_dicts_search_and_sort")
def test_check_dicts_search_and_sort(base_url, page: Page) -> None:
    dicts = Dicts(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD, create_many_dicts=True)

    with allure.step("Go to url"):
        dicts.navigate(base_url)

    with allure.step("Auth with user"):
        dicts.auth(LOGIN, PASSWORD)

    with allure.step("Go to markup"):
        dicts.click_markup()

    with allure.step("Go to dicts"):
        dicts.click_to_dicts()

    with allure.step("Filter rules by sort"):
        dicts.input_search.nth(1).type("test ", delay=5)

    with allure.step("Check that button for import not visible"):
        expect(dicts.input_search.nth(1)).to_have_value("test ")

    with allure.step("Filter rules by sort"):
        dicts.input_search.nth(1).type("AUTO", delay=5)

    with allure.step("Check that button for import not visible"):
        expect(page.get_by_text("auto_dict", exact=True)).to_be_visible()

    with allure.step("Clear search"):
        dicts.input_search.nth(1).clear()

    with allure.step("Filter rules by sort"):
        dicts.input_search.nth(1).type("many", delay=5)

    with allure.step("Check that button for import not visible"):
        expect(page.get_by_text("auto_dict", exact=True)).not_to_be_visible()

    with allure.step("Change sort"):
        dicts.change_sort("По алфавиту", "По алфавиту с конца")

    with allure.step("Check first rule name"):
        expect(page.locator('[data-testid="test"]').first).to_contain_text("AT_many_dicts5")

    with allure.step("Change sort"):
        dicts.change_sort("По алфавиту с конца", "Сначала новые")

    with allure.step("Check first rule name"):
        expect(page.locator('[data-testid="test"]').first).to_contain_text("AT_many_dicts5")

    with allure.step("Change sort"):
        dicts.change_sort("Сначала новые", "Сначала старые")

    with allure.step("Check first rule name"):
        expect(page.locator('[data-testid="test"]').first).to_contain_text("AT_many_dicts1")

    with allure.step("Change sort"):
        dicts.change_sort("Сначала старые", "Сначала обновленные")

    with allure.step("Check first rule name"):
        expect(page.locator('[data-testid="test"]').first).to_contain_text("AT_many_dicts5")

    with allure.step("Change sort"):
        dicts.change_sort("Сначала обновленные", "Сначала не обновленные")

    with allure.step("Check first rule name"):
        expect(page.locator('[data-testid="test"]').first).to_contain_text("AT_many_dicts1")

    with allure.step("Change sort"):
        dicts.change_sort("Сначала не обновленные", "По алфавиту")

    with allure.step("Check first rule name"):
        expect(page.locator('[data-testid="test"]').first).to_contain_text("AT_many_dicts1")

    page.locator('[data-testid="test"]').locator(CHECKBOX).first.click()
    page.wait_for_timeout(500)

    with allure.step("Check that button for import not visible"):
        expect(page.get_by_text("auto_dict", exact=True)).not_to_be_visible()
        expect(page.locator('[class*="Mui-checked"]')).to_have_count(6)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)