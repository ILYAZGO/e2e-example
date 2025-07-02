#from playwright.sync_api import Page, expect
from pages.base_class import *

INPUT_DICT_NAME = '[name="dictName"]'
INPUT_WORDS_LIST = '[name="phrases"]'
BUTTON_IMPORT_DICTS = '[data-testid="markup_importDicts"]'

class Dicts(BaseClass):
    def __init__(self, page: Page):
        super().__init__(page)
        self.button_dicts = page.locator(BUTTON_DICTS)
        self.input_dict_name = page.locator(INPUT_DICT_NAME)
        self.input_words_list = page.locator(INPUT_WORDS_LIST)
        self.button_add_dict = page.locator(BUTTON_ADD_DICT)
        self.button_import_dicts = page.locator(BUTTON_IMPORT_DICTS)

    def create_dict(self, dict_name: str, text: str):
        self.button_add_dict.click()
        self.page.wait_for_selector(INPUT_DICT_NAME, timeout=self.timeout)
        self.input_dict_name.type(dict_name, delay=10)
        self.modal_window.locator(BUTTON_ACCEPT).click()
        self.page.wait_for_selector(INPUT_WORDS_LIST, timeout=self.timeout)
        self.input_words_list.type(text, delay=10)

    def create_dict_without_text(self, dict_name: str):
        self.button_add_dict.click()
        self.page.wait_for_selector(INPUT_DICT_NAME, timeout=self.timeout)
        self.input_dict_name.type(dict_name, delay=10)
        self.modal_window.locator(BUTTON_ACCEPT).click()

    def change_dict_type(self, current_type: str, next_type: str):
        self.page.get_by_text(current_type, exact=True).click()
        self.page.wait_for_timeout(500)
        self.menu.get_by_text(next_type, exact=True).click()
        self.page.wait_for_timeout(500)

    def change_sort(self, current: str, change_to: str ):
        self.page.get_by_text(current, exact=True).click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        self.menu.get_by_text(change_to, exact=True).click()
        self.page.wait_for_load_state(state="load", timeout=self.timeout)
        self.page.wait_for_timeout(500)

'''------locators for rules---------'''
# TO DO need move up

# inputs
INPUT_EDIT_GROUP_NAME = "//input[@value='12345']"
# buttons
BUTTON_SAVE_EDITED_NAME = ".styles_root__4Hw2A"
# other
GROUP_LIST = '[class*="styles_dpBothBox_"]'
ACTIVE_GROUP = '[class*="styles_isActive_"]'
GROUP_ITEMS = '[class*="styles_groupItem_"]'
NAZVANIE_SLOVARYA = '[name="title"]'

TOOLTIP_BUTTON_DOBAVIT_SLOVAR = '[aria-label="Чтобы добавить словарь, выберите или добавьте группу."]'

# other
CLICK_ON_GROUP = "//p[normalize-space()='12345']"

def delete_rule_or_dict(page="page: Page"):
    #page.locator(".css-izdlur").click()
    #page.get_by_text("Удалить", exact=True).click()
    page.locator('[width="30"]').click()
    page.wait_for_selector(MODAL_WINDOW)
    page.locator(MODAL_WINDOW).get_by_role("button", name="Удалить").click()
    page.wait_for_selector(MODAL_WINDOW, state="hidden")

def delete_group(page="page: Page"):
    page.locator(ACTIVE_GROUP).locator(BUTTON_KORZINA).click()



