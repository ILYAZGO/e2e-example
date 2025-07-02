from playwright.sync_api import Page, expect, Route
from utils.variables import *
from utils.dates import first_day_week_ago
from pages.integration import *
from utils.create_delete_user import create_user, delete_user
import pytest
import allure
import re


@pytest.mark.e2e
@pytest.mark.integration
@allure.title("test_usedesk")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("User making integration with usedesk")
def test_usedesk(base_url, page: Page) -> None:
    integrations = Integrations(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        integrations.navigate(base_url)

    with allure.step("Auth"):
        integrations.auth(LOGIN, PASSWORD)

    with allure.step("Go to settings"):
        integrations.click_settings()

    with allure.step("Go to integrations"):
        integrations.press_integrations_in_menu()

    with allure.step("Press (Connect)"):
        integrations.press_connect()

    with allure.step("Choose Usedesk"):
        integrations.choose_integration("usedesk")

    with allure.step("Input API token"):
        integrations.input_api_token()

    with allure.step("Press (Save)"):
        integrations.press_save()

    with allure.step("Check alert"):
        integrations.check_alert("Данные сохранены")

    with allure.step("Check integration status"):
        expect(page.locator('[class*="styles_statusTitleDisconnected_"]')).to_have_count(1)

    with allure.step("Make integration Active"):
        page.locator(CHECKBOX).click()

    with allure.step("Check alert"):
        integrations.check_alert("Данные сохранены")

    with allure.step("Check integration status"):
        expect(page.locator('[class*="styles_statusTitleConnected"]')).to_have_count(1)

    with allure.step("Reload page"):
        integrations.reload_page()

    with allure.step("Check integration status"):
        expect(page.locator('[class*="styles_statusTitleConnected"]')).to_have_count(1)

    with allure.step("Go to integrations"):
        page.locator(BUTTON_INTEGRACII).click()

    with allure.step("Press to (Play) button"):
        integrations.press_play()

    with allure.step("Set period (first_day_week_ago)"):
        integrations.set_date(first_day_week_ago)

    with allure.step("Set calls limit (2)"):
        integrations.set_calls_limit("2")

    with allure.step("Press button create"):
        integrations.press_create()

    with allure.step("Check alert"):
        integrations.check_alert("Задача создана")

    with allure.step("Wait 35 seconds"):
        page.wait_for_timeout(35000)

    with allure.step("Reload page"):
        integrations.reload_page()

    with allure.step("Check that 2 communications downloaded"):
        page.wait_for_selector('[class*=headerRow]')
        expect(page.locator('[role="rowgroup"]').locator('[role="cell"]').nth(4)).to_have_text('2')

    with allure.step("Go to integration history"):
        page.locator('[aria-label="История"]').locator('[type="button"]').click()

    with allure.step("Check that integration have logs"):
        expect(page.locator('[aria-label="Логи интеграции"]')).to_have_count(1)

    with allure.step("Go to logs"):
        page.locator('[aria-label="Логи интеграции"]').locator('[type="button"]').click()

    with allure.step("Check that logs present"):
        page.wait_for_selector('[data-testid="TaskHistoryLogTable_dataTextarea"]', timeout=wait_until_visible)
        textarea = page.locator('[data-testid="TaskHistoryLogTable_dataTextarea"]')
        count = textarea.count()

        assert count > 1

    with allure.step("Go back to integrations list"):
        page.locator('[class*="styles_category"]').nth(0).click()

    with allure.step("Go to settings"):
        page.locator('[aria-label="Настройки"]').click()
        page.wait_for_selector('[href*="/parameters"]')

    with allure.step("Make integration inActive"):
        page.locator(CHECKBOX).click()

    with allure.step("Check alert"):
        integrations.check_alert("Данные сохранены")

    with allure.step("Check integration status"):
        expect(page.locator('[class*="styles_statusTitleDisconnected_"]')).to_have_count(1)

    with allure.step("Go to integrations"):
        page.locator(BUTTON_INTEGRACII).click()

    with allure.step("Delete integration"):
        integrations.delete_integration()

    with allure.step("Check that integration deleted"):
        expect(page.locator(BUTTON_CONNECT)).to_be_visible()

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.integration
@allure.title("test_search_string")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_search_string")
def test_search_string(base_url, page: Page) -> None:
    integrations = Integrations(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        integrations.navigate(base_url)

    with allure.step("Auth"):
        integrations.auth(LOGIN, PASSWORD)

    with allure.step("Go to settings"):
        integrations.click_settings()

    with allure.step("Go to integrations"):
        integrations.press_integrations_in_menu()

    with allure.step("Press (Connect)"):
        integrations.press_connect()

    with allure.step("Fill search string"):
        page.get_by_role("textbox", name="Поиск").type("za", delay=10)
        page.wait_for_timeout(500)

    with allure.step("Check that search string found something"):
        expect(page.locator('[class*="styles_listItem_"]')).to_have_count(1)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.integration
@allure.title("test_integration_parameters")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_integration_parameters. with ecotelecom")
def test_integration_parameters(base_url, page: Page) -> None:
    integrations = Integrations(page)

    with allure.step("Go to url"):
        integrations.navigate(base_url)

    with allure.step("Auth"):
        integrations.auth(ECOTELECOM, ECOPASS)

    with allure.step("Go to settings"):
        integrations.click_settings()

    with allure.step("Go to integrations"):
        integrations.press_integrations_in_menu()

    with allure.step("Go to settings"):
        page.locator('[aria-label="Настройки"]').click()
        page.wait_for_selector('[href*="/parameters"]')

    with allure.step("Go to parameters"):
        page.locator('[href*="/parameters"]').click()

    with allure.step("Check duration limit and skip empty calls are present"):
        expect(page.locator('[data-testid="duration_limit"]').locator('[type="text"]')).to_have_value("50")
        expect(page.locator('[data-testid="skip_empty_calls"]')).to_have_class(re.compile(r"Mui-checked"))


@pytest.mark.e2e
@pytest.mark.integration
@allure.title("test_integrations_api_token")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_integrations_api_token")
def test_integrations_api_token(base_url, page: Page) -> None:
    integrations = Integrations(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        integrations.navigate(base_url)

    with allure.step("Auth"):
        integrations.auth(LOGIN, PASSWORD)

    with allure.step("Go to settings"):
        integrations.click_settings()

    with allure.step("Go to integrations"):
        integrations.press_integrations_in_menu()

    with allure.step("Go to api tokens tab"):
        integrations.click_api_token_tab()

    with allure.step("Check alert about empty token list"):
        expect(page.locator(ALERT_MESSAGE)).to_contain_text("Вы еще не добавили ни одного токена")

    with allure.step("Press (add token)"):
        page.locator(BUTTON_ADD_TOKEN_OR_TRANSLATION).click()
        page.wait_for_selector('[data-row-key="0"]', timeout=wait_until_visible)

    with allure.step("Press (Delete api token)"):
        integrations.press_basket_in_api_tokens_and_tag_translations()

    with allure.step("Press (Cancel)"):
        page.locator('[data-testid="cancelDeleteToken"]').click()
        page.wait_for_selector(MODAL_WINDOW, state="hidden")

    with allure.step("Press (Delete api token)"):
        integrations.press_basket_in_api_tokens_and_tag_translations()

    with allure.step("Press (Delete)"):
        page.locator('[data-testid="confirmDeleteToken"]').click()
        page.wait_for_selector(MODAL_WINDOW, state="hidden")

    with allure.step("Check alert about empty token list"):
        expect(page.locator(ALERT_MESSAGE)).to_contain_text("Вы еще не добавили ни одного токена")

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.integration
@allure.title("test_integrations_api_token_list_if_500")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_integrations_api_token_list_if_500")
def test_integrations_api_token_list_if_500(base_url, page: Page) -> None:
    integrations = Integrations(page)

    error = "Возникла ошибка в процессе формирования таблицы"

    def handle_api_token_list(route: Route):
        route.fulfill(status=500, body="")

    # Intercept the route
    page.route("**/api_keys", handle_api_token_list)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Go to url"):
        integrations.navigate(base_url)

    with allure.step("Auth"):
        integrations.auth(LOGIN, PASSWORD)

    with allure.step("Go to settings"):
        integrations.click_settings()

    with allure.step("Go to integrations"):
        integrations.press_integrations_in_menu()

    with allure.step("Go to api tokens tab"):
        integrations.click_api_token_tab()

    with allure.step("Check alert"):
        integrations.check_alert("Ошибка 500: Внутренняя ошибка сервера")

    with allure.step("Check alert about empty token list"):
        expect(page.locator(ALERT_MESSAGE)).to_contain_text(error)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.integration
@allure.title("test_integrations_tag_translations")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_integrations_tag_translations")
def test_integrations_tag_translations(base_url, page: Page) -> None:
    integrations = Integrations(page)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD, upload_call=True)

    with allure.step("Go to url"):
        integrations.navigate(base_url)

    with allure.step("Auth"):
        integrations.auth(LOGIN, PASSWORD)

    with allure.step("Go to settings"):
        integrations.click_settings()

    with allure.step("Go to integrations"):
        integrations.press_integrations_in_menu()

    with allure.step("Go to tag translations tab"):
        page.locator('[href*="/translation-integrations-tags"]').click()

    with allure.step("Check alert about empty token list"):
        expect(page.locator(ALERT_MESSAGE)).to_contain_text("Вы еще не добавили ни одного перевода")

    with allure.step("Press (add token)"):
        page.wait_for_timeout(3000)
        page.locator(BUTTON_ADD_TOKEN_OR_TRANSLATION).click()
        page.wait_for_selector('[data-row-key="new-1"]', timeout=wait_until_visible)

    with allure.step("Add comment"):
        page.locator('[id="comment"]').clear()
        page.locator('[id="comment"]').type("comment", delay=20)

    with allure.step("Press green V"):
        page.wait_for_timeout(500)
        page.locator('[fill="#73D13D"]').click()
        page.wait_for_timeout(500)

    with allure.step("Check empty inputs alert"):
        expect(page.get_by_text("* Пожалуйста, выберите название", exact=True)).to_have_count(1)
        expect(page.get_by_text("* Пожалуйста, введите перевод", exact=True)).to_have_count(1)

    with allure.step("Choose tag"):
        page.locator('[class="ant-table-tbody"]').locator('[class*="-indicatorContainer"]').click()
        page.wait_for_selector(MENU)
        page.locator(MENU).get_by_text("auto_rule", exact=True).click()

    with allure.step("Add translation"):
        page.locator('[id="translatedName"]').clear()
        page.locator('[id="translatedName"]').type("tag", delay=20)

    with allure.step("Add comment"):
        page.locator('[id="comment"]').clear()
        page.locator('[id="comment"]').type("comment", delay=20)

    with allure.step("Press green V"):
        page.wait_for_timeout(500)
        page.locator('[fill="#73D13D"]').click()
        page.wait_for_timeout(500)

    with allure.step("Reload page"):
        integrations.reload_page()

    with allure.step("Check that tanslation saved"):
        expect(page.get_by_text("auto_rule", exact=True)).to_have_count(1)
        expect(page.get_by_text("tag", exact=True)).to_have_count(1)
        expect(page.get_by_text("comment", exact=True)).to_have_count(1)

    with allure.step("Press pencil"):
        page.locator('[class*="ant-btn"]').nth(0).click()

    with allure.step("Choose tag"):
        page.locator('[class="ant-table-tbody"]').locator('[class*="-indicatorContainer"]').click()
        page.wait_for_selector(MENU)
        page.locator(MENU).get_by_text("auto", exact=True).click()

    with allure.step("Add translation"):
        page.locator('[id="translatedName"]').clear()
        page.locator('[id="translatedName"]').type("gat", delay=20)

    with allure.step("Add comment"):
        page.locator('[id="comment"]').clear()
        page.locator('[id="comment"]').type("tnemmoc", delay=20)

    with allure.step("Press green V"):
        page.locator('[fill="#73D13D"]').click()
        page.wait_for_timeout(500)

    with allure.step("Reload page"):
        integrations.reload_page()

    with allure.step("Check that tanslation saved"):
        expect(page.get_by_text("auto", exact=True)).to_have_count(1)
        expect(page.get_by_text("gat", exact=True)).to_have_count(1)
        expect(page.get_by_text("tnemmoc", exact=True)).to_have_count(1)

    with allure.step("Press (Delete api token)"):
        page.locator('[class*="ant-btn"]').nth(1).click()

    with allure.step("Press (Cancel)"):
        page.get_by_text("Отмена", exact=True).click()
        page.wait_for_selector(MODAL_WINDOW, state="hidden")

    with allure.step("Press (Delete api token)"):
        page.locator('[class*="ant-btn"]').nth(1).click()

    with allure.step("Press (Delete)"):
        page.get_by_text("Удалить", exact=True).click()
        page.wait_for_selector(MODAL_WINDOW, state="hidden")

    with allure.step("Check alert about empty token list"):
        expect(page.locator(ALERT_MESSAGE)).to_contain_text("Вы еще не добавили ни одного перевода")

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.integration
@allure.title("test_integrations_tag_translation_list_if_500")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("test_integrations_tag_translation_list_if_500")
def test_integrations_tag_translation_list_if_500(base_url, page: Page) -> None:
    integrations = Integrations(page)

    error = "Возникла ошибка в процессе формирования таблицы"

    def handle_api_token_list(route: Route):
        route.fulfill(status=500, body="")

    # Intercept the route
    page.route("**/tag_translations/user", handle_api_token_list)

    with allure.step("Create user"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD, upload_call=False)

    with allure.step("Go to url"):
        integrations.navigate(base_url)

    with allure.step("Auth"):
        integrations.auth(LOGIN, PASSWORD)

    with allure.step("Go to settings"):
        integrations.click_settings()

    with allure.step("Go to integrations"):
        integrations.press_integrations_in_menu()

    with allure.step("Go to api tokens tab"):
        page.locator('[href*="/translation-integrations-tags"]').click()

    with allure.step("Check alert"):
        integrations.check_alert("Ошибка 500: Внутренняя ошибка сервера")

    with allure.step("Check alert about empty token list"):
        expect(page.locator(ALERT_MESSAGE)).to_contain_text(error)

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN, USER_ID)