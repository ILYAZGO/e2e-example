from pages.base_class import *
from playwright.sync_api import Page, expect

from utils.variables import wait_until_visible

INPUT_NEW_GROUP_NAME = '[name="groupName"]'
INPUT_TAG_RULE_NAME = '[name="title"]'
ACTIVE_GROUP = '[class*="styles_isActive_"]'
BUTTON_ADD_TAG = '[data-testid="markup_addTaggingRule"]'
INPUT_TAG_NAME = '[data-testid="markup_newRuleInput"]'
BUTTON_SAVE_EDITED_NAME = ".styles_root__4Hw2A"
BUTTON_ADD_SEQUENCE = '[data-testid="addNewTagSequenceItemBtn"]'
BUTTON_DELETE_SEQUENCE = '[data-testid="TagSequenceDeleteItem"]'
LIST_PRESENCE_ONE_OF_TAGS = '[data-testid="presenceOfOneOfTags"]'
LIST_PRESENCE_ONE_OF_TAGS_IN_INTERVAL_AFTER = '[data-testid="presenceOfOneOfTagsInSpecifiedIntervalAfter"]'
INPUT_INTERVAL_BETWEEN_TAGS = '[data-testid="intervalBetweenTags"]'
CHECK_BOX_ABSENCE_OF_TAGS = '[data-testid="triggeredInAbsenceOfTags"]'
CHECK_BOX_REVERSE_LOGIC = '[data-testid="reverseLogic"]'
BUTTON_IMPORT_RULES = '[data-testid="markup_importTagRules"]'
GROUP_LIST = '[class*="styles_dpBothBox_"]'

class Rules(BaseClass):
    def __init__(self, page: Page):
        super().__init__(page)
        self.button_add_tag = page.locator(BUTTON_ADD_TAG)
        self.input_tag_name = page.locator(INPUT_TAG_NAME)
        self.input_tag_rule_name = page.locator('[name="title"]')

    def delete_group(self):
        self.page.locator(ACTIVE_GROUP).locator(BUTTON_KORZINA).click()
        self.page.wait_for_timeout(500)

    def delete_rule_or_dict(self):
        self.page.locator('[width="30"]').click()
        self.page.wait_for_selector(MODAL_WINDOW, timeout=self.timeout)
        self.modal_window.get_by_role("button", name="Удалить").click()
        self.page.wait_for_selector(MODAL_WINDOW, state="hidden")

    def press_create_rule(self):
        self.page.wait_for_selector(BUTTON_ADD_TAG, timeout=self.timeout)
        self.button_add_tag.click()
        self.page.wait_for_selector(INPUT_TAG_NAME, timeout=self.timeout)

    def input_new_rule_name(self, rule_name: str):
        self.input_tag_name.type(rule_name, delay=10)
        self.press_key("Enter")  # kostil'
        self.page.wait_for_timeout(1000)

    def click_import_rules(self):
        self.page.wait_for_selector(BUTTON_IMPORT_RULES, timeout=self.timeout)
        self.page.locator(BUTTON_IMPORT_RULES).click()

    def change_sort(self, current: str, change_to: str ):
        self.page.get_by_text(current, exact=True).click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        self.menu.get_by_text(change_to, exact=True).click()
        self.page.wait_for_load_state(state="load", timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def assert_first_group_name(self, name: str):
        self.page.wait_for_timeout(500)
        expect(self.page.locator('[data-testid="test"]').first).to_contain_text(name)



# TO DO move up
# inputs
INPUT_EDIT_GROUP_NAME = "//input[@value='12345']"


def fill_what_said(text, page="page: Page"):
    page.locator('[data-testid="fragmentRuleWhatSaid"]').locator('[autocorrect="off"]').type(text, delay=10)
    page.keyboard.press("Enter", delay=10)
    page.wait_for_timeout(500)

def add_additional_terms(list, page="page: Page"):
    page.wait_for_timeout(500)
    page.locator('[data-testid="fragmentRuleAddButton"]').locator('[type="button"]').dblclick()
    page.wait_for_selector('[class*="-menu"]', timeout=wait_until_visible)
    for i in list:
        page.locator('[class*="-menu"]').get_by_text(i).click()
    page.locator('[data-testid="fromStart"]').click()
    page.locator('[data-testid="onlyFirstMatch"]').click()
    for l in range(10):
        page.locator('[placeholder=">X, <X или X-Y. Время в секундах"]').nth(l).fill(f"{l}")
    page.wait_for_timeout(500)


