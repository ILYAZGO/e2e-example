from playwright.sync_api import Page, expect, Playwright
#from pytest_playwright.pytest_playwright import browser, device

from utils.variables import *
from pages.login import *
from utils.create_delete_user import create_user, delete_user, create_operator
import pytest
import allure


"""THIS TEST NOT USEFULL CHECK THIS IN OTHER TESTS"""
# @pytest.mark.independent
# @pytest.mark.login
# @allure.title("test_login_admin_positive")
# @allure.severity(allure.severity_level.CRITICAL)
# def test_login_admin_positive(base_url, page: Page) -> None:
#     login_page = LoginPage(page)
#
#     with allure.step("Create admin"):
#         USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)
#
#     with allure.step("Go to url"):
#         login_page.navigate(base_url)
#
#     with allure.step("Auth"):
#         login_page.auth(LOGIN, PASSWORD)
#
#     with allure.step("Quit from profile"):
#         login_page.quit_from_profile()
#
#     with allure.step("Check that quit was successful"):
#         login_page.assert_quited()
#
#     with allure.step("Delete admin"):
#         delete_user(API_URL, TOKEN, USER_ID)

"""THIS TEST NOT USEFULL CHECK THIS IN OTHER TESTS"""
# @pytest.mark.independent
# @pytest.mark.login
# @allure.title("test_login_manager_positive")
# @allure.severity(allure.severity_level.CRITICAL)
# def test_login_manager_positive(base_url, page: Page) -> None:
#     login_page = LoginPage(page)
#
#     with allure.step("Create manager"):
#         USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_MANAGER, PASSWORD)
#
#     with allure.step("Go to url"):
#         login_page.navigate(base_url)
#
#     with allure.step("Auth"):
#         login_page.auth(LOGIN, PASSWORD)
#
#     with allure.step("Quit from profile"):
#         login_page.quit_from_profile()
#
#     with allure.step("Check that quit was successful"):
#         login_page.assert_quited()
#
#     with allure.step("Delete manager"):
#         delete_user(API_URL, TOKEN, USER_ID)


"""THIS TEST NOT USEFULL CHECK THIS IN OTHER TESTS"""
# @pytest.mark.independent
# @pytest.mark.login
# @allure.title("test_login_user_positive")
# @allure.severity(allure.severity_level.CRITICAL)
# def test_login_user_positive(base_url, page: Page) -> None:
#     login_page = LoginPage(page)
#
#     with allure.step("Create user"):
#         USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_USER, PASSWORD)
#
#     with allure.step("Go to url"):
#         login_page.navigate(base_url)
#
#     with allure.step("Auth"):
#         login_page.auth(LOGIN, PASSWORD)
#
#     with allure.step("Quit from profile"):
#         login_page.quit_from_profile()
#
#     with allure.step("Check that quit was successful"):
#         login_page.assert_quited()
#
#     with allure.step("Delete user"):
#         delete_user(API_URL, TOKEN, USER_ID)


@pytest.mark.e2e
@pytest.mark.login
@allure.title("test_login_operator_positive")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_operator_positive(base_url, page: Page) -> None:
    login_page = LoginPage(page)

    with allure.step("Create user"):
        USER_ID_USER, TOKEN_USER, LOGIN_USER = create_user(API_URL, ROLE_USER, PASSWORD)

    with allure.step("Create operator"):
        USER_ID_OPERATOR, TOKEN_OPERATOR, LOGIN_OPERATOR = create_operator(API_URL, USER_ID_USER, PASSWORD)

    with allure.step("Go to url"):
        login_page.navigate(base_url)

    with allure.step("Check registration button not visible"):
        expect(page.get_by_text("Зарегистрироваться")).not_to_be_visible()

    with allure.step("Auth"):
        login_page.auth(LOGIN_OPERATOR, PASSWORD)

    with allure.step("Quit from profile"):
        login_page.quit_from_profile()

    with allure.step("Check that quit was successful"):
        login_page.assert_quited()

    with allure.step("Check registration button not visible"):
        expect(page.get_by_text("Зарегистрироваться")).not_to_be_visible()

    with allure.step("Delete user"):
        delete_user(API_URL, TOKEN_USER, USER_ID_USER)

    with allure.step("Delete operator"):
        delete_user(API_URL, TOKEN_OPERATOR, USER_ID_OPERATOR)


@pytest.mark.e2e
@pytest.mark.login
@allure.title("test_login_user_negotive")
@allure.severity(allure.severity_level.NORMAL)
def test_login_user_negotive(base_url, page: Page) -> None:
    wrong_login = "1userI"
    login_page = LoginPage(page)

    with allure.step("Go to url"):
        login_page.navigate(base_url)

    with allure.step("Auth"):
        login_page.auth(wrong_login, PASSWORD)

    with allure.step("Check that alert message visible"):
        login_page.assert_alert_visible("Wrong login or password")
        login_page.assert_button_enter_enabled()


@pytest.mark.e2e
@pytest.mark.login
@allure.title("test_password_user_negotive")
@allure.severity(allure.severity_level.NORMAL)
def test_password_user_negotive(base_url, page: Page) -> None:
    wrong_password = "Qaz123ws"
    login_page = LoginPage(page)

    with allure.step("Go to url"):
        login_page.navigate(base_url)

    with allure.step("Auth"):
        login_page.auth(ECOTELECOM, wrong_password)

    with allure.step("Check that alert message visible"):
        login_page.assert_alert_visible("Wrong login or password")
        login_page.assert_button_enter_enabled()


@pytest.mark.e2e
@pytest.mark.login
@allure.title("test_first_page_locale")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("test checks first page under 4 supported locale and 1 unsupported")
def test_first_page_locale(base_url, playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    # create a new incognito browser context.
    with allure.step("go first page RU locale"):
        context = browser.new_context(locale="ru-RU")
        # create a new page in a pristine context.
        page = context.new_page()
        page.goto(base_url)

    with allure.step("Check lang"):
        expect(page.locator('[placeholder="Логин"]')).to_have_count(1)
        expect(page.locator('[placeholder="Пароль"]')).to_have_count(1)
        expect(page.locator(BUTTON_SUBMIT)).to_have_text("Войти")
        expect(page.locator('[class*="styles_authGreetSide_"]')).to_have_text(
            "Добро пожаловатьВ речевую аналитикуВойдите чтобы получить доступ")

        context.close()
    with allure.step("go first page PT locale"):
        context = browser.new_context(locale="pt-PT")
        # create a new page in a pristine context.
        page = context.new_page()
        page.goto(base_url)

    with allure.step("Check lang"):
        expect(page.locator('[placeholder="Login"]')).to_have_count(1)
        expect(page.locator('[placeholder="Senha"]')).to_have_count(1)
        expect(page.locator(BUTTON_SUBMIT)).to_have_text("Entrar")
        expect(page.locator('[class*="styles_authGreetSide_"]')).to_have_text(
            "Bem-vindoÀ análise de falaEntre para ter acesso")

        context.close()

    with allure.step("go first page ES locale"):
        context = browser.new_context(locale="es-ES")
        # create a new page in a pristine context.
        page = context.new_page()
        page.goto(base_url)

    with allure.step("Check lang"):
        expect(page.locator('[placeholder="Inicio de sesión"]')).to_have_count(1)
        expect(page.locator('[placeholder="Contraseña"]')).to_have_count(1)
        expect(page.locator(BUTTON_SUBMIT)).to_have_text("Iniciar sesión")
        expect(page.locator('[class*="styles_authGreetSide_"]')).to_have_text(
            "BienvenidoA la analítica de vozInicie sesión para acceder")

        context.close()

    with allure.step("go first page EN locale"):
        context = browser.new_context(locale="en-EN")
        # create a new page in a pristine context.
        page = context.new_page()
        page.goto(base_url)

    with allure.step("Check lang"):
        expect(page.locator('[placeholder="Login"]')).to_have_count(1)
        expect(page.locator('[placeholder="Password"]')).to_have_count(1)
        expect(page.locator(BUTTON_SUBMIT)).to_have_text("Sign in")
        expect(page.locator('[class*="styles_authGreetSide_"]')).to_have_text(
            "Welcome toSpeech analyticsSign in to get access")

        context.close()

    with allure.step("go first page unsupported FR locale"):
        context = browser.new_context(locale="fr-FR")
        # create a new page in a pristine context.
        page = context.new_page()
        page.goto(base_url)

    with allure.step("Check lang"):
        expect(page.locator('[placeholder="Login"]')).to_have_count(1)
        expect(page.locator('[placeholder="Password"]')).to_have_count(1)
        expect(page.locator(BUTTON_SUBMIT)).to_have_text("Sign in")
        expect(page.locator('[class*="styles_authGreetSide_"]')).to_have_text(
            "Welcome toSpeech analyticsSign in to get access")

        context.close()
        browser.close()






