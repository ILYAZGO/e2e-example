from pages.base_class import *

BUTTON_GPT_CREATE_RULE = '[data-testid="markup_addGroup"]'
BUTTON_SAVE_EDITED_NAME = '[class*="styles_checkButton"]'
BUTTON_IMPORT_GPT = '[data-testid="markup_importDicts"]'

INPUT_GPT_RULE_NAME = '[placeholder="Название правила"]'
INPUT_GPT_TEG_NAME = '[placeholder="Название"]'

class GPT(BaseClass):
    def __init__(self, page: Page):
        super().__init__(page)
        self.button_create_gpt_rule = page.locator(BUTTON_GPT_CREATE_RULE)
        self.input_gpt_rule_name = page.locator(INPUT_GPT_RULE_NAME)
        self.input_gpt_tag_name = page.locator(INPUT_GPT_TEG_NAME)
        self.input_gpt_question = page.locator(INPUT_GPT_QUESTION)

    def delete_rule(self):
        self.page.wait_for_selector(BUTTON_KORZINA, timeout=self.timeout)
        self.button_korzina.first.click()
        self.page.wait_for_selector(MODAL_WINDOW, timeout=self.timeout)
        self.page.wait_for_timeout(500)
        self.modal_window.get_by_role("button", name="Удалить").click()
        self.page.wait_for_selector(MODAL_WINDOW, state="hidden")
        self.page.wait_for_timeout(500)

    def press_add_settings(self):
        self.page.get_by_role("button", name="Добавить настройки").click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)

    def click_create_new_gpt_rule(self):
        self.button_create_gpt_rule.click()
        self.page.wait_for_timeout(500)
        self.page.wait_for_selector(INPUT_GPT_RULE_NAME, timeout=self.timeout)

    def fill_gpt_rule_with_one(self, gpt_rule_name: str):
        """Creates gpt rule with one question"""
        self.input_gpt_rule_name.type(gpt_rule_name, delay=5)
        self.page.wait_for_timeout(1000)
        self.input_gpt_tag_name.type("GPTteg1", delay=5)
        self.page.wait_for_timeout(500)
        self.input_gpt_question.type("GPTquestion1", delay=5)
        self.page.wait_for_timeout(500)

    def fill_gpt_rule_with_two(self, gpt_rule_name: str):
        """Creates gpt rule with two questions"""
        self.input_gpt_rule_name.type(gpt_rule_name, delay=5)
        self.page.wait_for_timeout(1000)
        self.input_gpt_tag_name.type("GPTteg1", delay=5)
        self.page.wait_for_timeout(500)
        self.input_gpt_question.type("GPTquestion1", delay=5)
        self.page.wait_for_timeout(500)
        self.page.get_by_role("button", name="Добавить вопрос").click()
        self.page.wait_for_timeout(1000)
        self.input_gpt_tag_name.nth(1).type("GPTteg2", delay=5)
        self.page.wait_for_timeout(500)
        self.input_gpt_question.nth(1).type("GPTquestion2", delay=5)
        self.page.wait_for_timeout(500)

    def turn_on_rule(self):
        self.page.locator('[aria-label="Вкл/Выкл"]').locator('[type="checkbox"]').click()
        #self.page.wait_for_selector('[class*="Mui-checked"]', timeout=self.timeout)

    def rename_gpt_rule(self, old_name, new_name):
        self.button_pencil.click()
        self.page.locator('[class*="styles_dpBothBox"]').locator(f'[value="{old_name}"]').type(new_name, delay=5)
        self.page.locator(BUTTON_SAVE_EDITED_NAME).click()

    def press_save_in_gpt(self):
        self.button_accept.click(force=True)
        self.page.wait_for_timeout(500)


# TO DO need move up

def add_filter(filterType, filterName, page="page: Page"):
    page.locator('[style="margin-top: 5px;"]').get_by_role("button").click()
    page.locator('[class*="-menu"]').get_by_text(filterType, exact=True).nth(1).click()
    page.wait_for_timeout(500)
    page.locator('[aria-label="Фильтры коммуникаций"]').click()
    page.wait_for_timeout(500)
    page.locator('[data-testid="filters_search_by_tags"]').locator('[autocorrect=off]').fill(filterName)
    page.wait_for_timeout(2300)
    page.get_by_text(filterName, exact=True).nth(0).click()


# def all_checkboxes_to_be_checked(page="page: Page"):
#     # Находим все чекбоксы на странице
#     checkboxes = page.query_selector_all('input[type="checkbox"]')
#     # Проверяем состояние каждого чекбокса
#     all_checked = all(checkbox.is_checked() for checkbox in checkboxes)
#     return all_checked

def amount_checkboxes_to_be_checked(amount, page="page: Page"):
    # Находим все чекбоксы на странице
    checkboxes = page.query_selector_all('input[type="checkbox"]')
    # Check that amount checked
    all_checked = sum(checkbox.is_checked() for checkbox in checkboxes)
    return all_checked==amount