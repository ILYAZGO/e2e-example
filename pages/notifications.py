#from playwright.sync_api import Page, expect
from pages.base_class import *

BUTTON_IMPORT_RULES = '[class*="styles_importTagRules"]'
INPUT_NOTIFICATION_NAME = '[name="notifyTitle"]'
INPUT_LETTER_THEME = '[name="emailSubj"]'
INPUT_EMAIL = '[placeholder="example@mail.com"]'
INPUT_HEADERS = '[placeholder="Можно проставить авторизацию и content-type"]'
INPUT_URL = '[name="apiUrl"]'
INPUT_COMMENT = '[class="styles_textarea__+sldQ"]'

BLOCK_RULE_MAIN_AREA = '[class*="mainArea"]'
BLOCK_RULES_LIST = '[class*="sidebar"]'
BlOCK_API = '[class*="InputWithSelect_root"]'
BLOCK_ADD_NEW_RULE = '[class*="styles_addNewRule_"]'

SEARCH_IN_IMPORT_MODAL = '[data-testid="NotifyRuleCopyMode_search"]'
BLOCK_AFTER_IMPORT = '[class*="styles_btns"]'

class Notifications(BaseClass):
    def __init__(self, page: Page):
        super().__init__(page)
        self.notification_name = page.locator(INPUT_NOTIFICATION_NAME)
        self.button_add_new_rule = page.locator(BLOCK_ADD_NEW_RULE).locator('[type="button"]')
        self.block_main_area = page.locator(BLOCK_RULE_MAIN_AREA)
        self.block_api = page.locator(BlOCK_API)
        self.input_letter_theme = page.locator(INPUT_LETTER_THEME)
        self.input_email = page.locator(INPUT_EMAIL)
        self.input_comment = page.locator(INPUT_COMMENT)
        self.input_url = page.locator(INPUT_URL)
        self.input_headers = page.locator(INPUT_HEADERS)
        self.button_import_rules = page.locator(BUTTON_IMPORT_RULES).locator('[type="button"]')

    def choose_block(self, block_number: int):
        self.page.wait_for_selector(BUTTON_NOTIFICATIONS, timeout=self.timeout)
        self.page.wait_for_timeout(1000)
        self.page.locator(BUTTON_NOTIFICATIONS).click()
        self.page.wait_for_timeout(1000)
        self.page.locator('[class*="notifyList"]').locator(".styles_root__cx1Gi").nth(block_number).click()
        self.page.wait_for_selector(INPUT_NOTIFICATION_NAME, timeout=self.timeout)

    def set_notification_name(self, notification_name: str):
        self.notification_name.type(notification_name, delay=5)

    def add_notification(self, notification_type: str):
        self.page.wait_for_timeout(500)
        self.button_add_new_rule.click()
        self.page.wait_for_selector(INPUT_NOTIFICATION_NAME, timeout=self.timeout)
        self.block_main_area.locator('[class="css-8mmkcg"]').first.click()
        self.page.wait_for_timeout(500)
        self.block_main_area.locator(MENU).get_by_text(notification_type, exact=True).click()
        self.page.wait_for_timeout(500)

    def fill_attr_for_email(self, letter_theme, email):
        self.page.wait_for_selector(INPUT_LETTER_THEME, timeout=self.timeout)
        self.input_letter_theme.type(letter_theme, delay=10)
        self.page.wait_for_timeout(500)
        self.input_email.type(email, delay=10)

    def fill_message(self, text: str):
        self.input_comment.type(text, delay=10)
        self.page.wait_for_timeout(500)
        self.page.locator('[aria-label="ID звонка. Пример: 123456789012345678901234"]').click()

    def set_url_and_headers(self, url, headers):
        self.input_url.fill(url)
        self.page.wait_for_timeout(500)
        self.input_headers.fill(headers)

    def go_back_in_rule_after_save(self, notification_name: str):
        self.page.wait_for_selector('[class*=notifyList]', timeout=self.timeout)
        self.page.get_by_text(notification_name).click()
        self.page.wait_for_selector(INPUT_NOTIFICATION_NAME, timeout=self.timeout)

    def save_rule(self):
        self.page.get_by_role("button", name="Сохранить правило").click()
        self.page.wait_for_timeout(500)

    def press_import_rules(self):
        self.button_import_rules.click()
        self.page.wait_for_selector(SEARCH_IN_IMPORT_MODAL, timeout=self.timeout)

    def change_api_method(self, current_method, new_method):
        """Change API method for API rules"""
        self.block_api.get_by_text(current_method).click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        self.menu.get_by_text(new_method, exact=True).click()
        self.page.wait_for_selector(MENU, state="hidden", timeout=self.timeout)

# TO DO need move up

def add_filter(filterType, filterName, elementNumber, page="page: Page"):
    #  dobavit filtr
    page.locator('[style*="padding: 10px; border-radius: 10px;"]').get_by_role("button").click()
    #  choose po tegam
    page.locator(MENU).get_by_text(filterType, exact=True).nth(1).click()
    #  tupo click
    page.locator(".styles_title__nLZ-h").click()
    #  fill filter
    page.locator('[data-testid="filters_search_by_tags"]').locator('[autocorrect=off]').fill(filterName)
    page.wait_for_timeout(3000)
    #  choose filter
    page.get_by_text(filterName, exact=True).nth(0).click()

def delete_rule(page="page: Page"):
    page.wait_for_selector(BUTTON_KORZINA)
    page.locator(BLOCK_RULES_LIST).locator('[type="checkbox"]').first.click()
    page.locator(BUTTON_KORZINA).first.click()
    page.wait_for_timeout(500)
    #  confirm deleting
    page.locator(MODAL_WINDOW).get_by_role("button", name="Удалить").click()
    page.wait_for_timeout(1500)


