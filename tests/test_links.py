#from playwright.sync_api import Page, expect
from utils.variables import *
from pages.links import *
import pytest
from utils.create_delete_user import create_user, delete_user
import allure


@pytest.mark.e2e
@pytest.mark.links
@allure.title("test_send_link_to_admin_not_logged")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("Sending link to admin, that not logged in system")
def test_send_link_to_admin_not_logged(base_url, page) -> None:
    links = Links(page)
    #link = "http://192.168.10.101/feature-dev-2976/ru/6204e7cb599aff4f43f5d3a0/settings/profile"
    link = "https://app.stand.imot.io/ru/6204e7cb599aff4f43f5d3a0/settings/profile"

    with allure.step("Create admin"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Go to link and get auth page"):
        links.navigate(link)

    with allure.step("Login with admin"):
        links.auth(LOGIN, PASSWORD)

    with allure.step("Check that after login we going directly to link"):
        links.assert_url(link)

    with allure.step("Delete admin"):
        delete_user(API_URL, TOKEN, USER_ID)


# need same test for user , manager and operator, but later.
# For now we dont care what will happen https://task.imot.io/browse/DEV-3331




#  https://task.imot.io/browse/DEV-3606


@pytest.mark.e2e
@pytest.mark.links
@allure.title("test_login_from_public_link_by_user")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("In this case we're sending public link to not logged user, "
                    "than we're logging like user and check link."
                    "Call owner is ecotelecom.")
def est_login_from_public_link_by_user(base_url, page) -> None:
    links = Links(page)

    link = ("https://app.stand.imot.io/ru/6204e7cb599aff4f43f5d3a0/"
            "call?id=62050BEC113619D283D9D584&"
            "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjYWxsX2lkIjoiNjIwNTBiZWMxMTM2MTlkMjgzZDlkNTg0IiwiZXhwIjoxNzQ5MjkwMTEzfQ.bQnslMyb5KpMylakKJK5S5Ek2i7Vm9AySifJjNBLxmY&public=true")


    with allure.step("Go to link and get auth page"):
        links.navigate(link)

    with allure.step("Click to imot.io"):
        links.click_imot_io()

    with allure.step("Login with admin"):
        links.auth(ECOTELECOM, ECOPASS)

    with allure.step("Check that after login we going directly to link"):
        links.assert_url(link)


@pytest.mark.e2e
@pytest.mark.links
@allure.title("test_login_from_public_link_by_admin")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("Sending public link to admin, that not logged in system, than logging by admin and check link. "
                    "Call owner is ecotelecom.")
def est_login_from_public_link_by_admin(base_url, page) -> None:
    links = Links(page)

    link = ("https://app.stand.imot.io/ru/6204e7cb599aff4f43f5d3a0/"
            "call?id=62050BEC113619D283D9D584&"
            "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjYWxsX2lkIjoiNjIwNTBiZWMxMTM2MTlkMjgzZDlkNTg0IiwiZXhwIjoxNzQ5MjkwMTEzfQ.bQnslMyb5KpMylakKJK5S5Ek2i7Vm9AySifJjNBLxmY&public=true")

    with allure.step("Create admin"):
        USER_ID, TOKEN, LOGIN = create_user(API_URL, ROLE_ADMIN, PASSWORD)

    with allure.step("Go to link and get auth page"):
        links.navigate(link)

    with allure.step("Click to imot.io"):
        links.click_imot_io()

    with allure.step("Login with admin"):
        links.auth(LOGIN, PASSWORD)

    with allure.step("Check that after login we going directly to link"):
        links.assert_url(link)
        expect(page.locator("#react-select-2-input")).to_have_text("Экотелеком")

    with allure.step("Delete admin"):
        delete_user(API_URL, TOKEN, USER_ID)