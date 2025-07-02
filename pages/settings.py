from pages.base_class import *

BUTTON_PERSONAL_INFO = '[href*="/profile"]'
BUTTON_UPLOAD = '[href*="/upload"]'

INPUT_QUOTA_TIME = '[name="time"]'

BLOCK_LEFT_MENU = '[class*="styles_list_"]'
LEFT_MENU_ITEM = "[class='styles_content__MNyQa']"
BLOCK_PERSONAL_INFO = '[class*="LeftMenuLayout_content"]'
BLOCK_ONE_RIGHT = '[class*="styles_toggleItem_"]'

SELECT_TIMEZONE = '[data-testid="selectTimezone"]'

CHECKBOX_MERGE_ALL_TO_ONE = '[name="merge_all_to_one_audio"]'
RECOGNITION_PRIORITY = '[data-testid="count_per_iteration"]'
CHECKBOX_DIARIZATION = '[name="diarization"]'
CHECKBOX_ECONOMIZE = '[id="sttEconomize"]'
CHECKBOX_USE_WEBHOOK = '[name="use_webhook"]'
CHECKBOX_ADD_PUNCTUATION = '[name="add_punctuation"]'
CHECKBOX_ENGINE_DIARIZATION = '[name="engine_diarization"]'
CHECKBOX_NORMALIZATION = '[name="text_normalization"]'
CHECKBOX_PROFANITY_FILTER = '[name="profanity_filter"]'
CHECKBOX_LITERATURE_STYLE = '[name="literature_text"]'
CHECKBOX_PHONE_FORMATTING = '[name="phone_formatting"]'
BLOCK_WITH_BUTTON = '[class*="STT_controlButtonsBlock"]'

BUTTON_CONSUMPTION_HISTORY_AUDIO = '[href*="-consumption-history/audio"]'
BUTTON_CONSUMPTION_HISTORY_GPT = '[href*="-consumption-history/gpt"]'
BUTTON_CONSUMPTION_HISTORY_CHATS = '[href*="-consumption-history/dialogs"]'
SEARCH_IN_CONSUMPTION_AUDIO = '[data-testid="AudioCommunications_searchBySource"]'
SEARCH_IN_CONSUMPTION_GPT = '[data-testid="GPTCommunications_searchBySource"]'
SEARCH_IN_CONSUMPTION_CHATS = '[data-testid="DialogsCommunications_searchBySource"]'
CALENDAR_IN_CONSUMPTION = '[class="ant-space-item"]'
TOTAL_AUDIO_MIN = '[class*="communicationsStyles_totalValueInMinutes_"]'
TOTAL_AUDIO_HOURS = '[class*="communicationsStyles_totalValueInHours_"]'
TOTAL_GPT_MONEY = '[class*="communicationsStyles_gptValuesWrapper_"]'
TOTAL_CHATS = '[class*="communicationsStyles_chatsValuesWrapper_"]'

BUTTON_RATES = '[href*="/settings/billing/aboutRates"]'
BUTTON_WRITEOFFS = '[href*="/settings/billing/writeoffs"]'
BUTTON_CHARGES = '[href*="/settings/billing/payments"]'
MESSAGE_TARIFFICATION_EMPTY = '[class*="styles_firstLine__"]'
SEARCH_IN_TARIFFICATION = '[data-testid="Writeoffs_search"]'
TOTAL_IN_TABLE = '[class*="style_valuesWrapper_"]'

BUTTON_GPT_QUOTAS = '[href*="quotas/gpt-quotas"]'
BLOCK_GPT_QUOTAS = '[class*="styles_quotasWrapper"]'
#BLOCK_CHAT_GPT = '[class*="styles_ChatGPTwrapper"]'
#BLOCK_YANDEX_GPT = '[class*="styles_YandexGPTwrapper"]'
INPUT_NEW_QUOTA = '[placeholder="Новое значение"]'
BLOCK_WITH_SAVE_BUTTON = '[class*="styles_saveButton"]'
BLOCK_WITH_AMOUNT = '[class*="styles_amount_"]'
BUTTON_CREATE_COMMUNICATIONS = '[data-testid="upload_create_communications"]'
BUTTON_DELETE_ALL_COMMUNICATIONS = '[data-testid="upload_delete_communications"]'

class Settings(BaseClass):
    def __init__(self, page: Page):
        super().__init__(page)
        self.input_address_book = page.locator(INPUT_ADDRESS_BOOK)
        self.button_personal_info = page.locator(BUTTON_PERSONAL_INFO)
        self.button_gpt_in_quotas = page.locator(BUTTON_GPT_QUOTAS)
        #self.input_chat_gpt_quota_value = page.locator(BLOCK_CHAT_GPT).locator(INPUT_NEW_QUOTA)
        #self.input_yandex_gpt_quota_value = page.locator(BLOCK_YANDEX_GPT).locator(INPUT_NEW_QUOTA)
        self.one_right_block = page.locator(BLOCK_ONE_RIGHT)
        self.input_quota_time = page.locator(INPUT_QUOTA_TIME)
        self.input_timezone = page.locator(SELECT_TIMEZONE).locator('[type="text"]')
        self.select_role = page.locator(SELECT_ROLE).locator('[type="text"]')
        self.button_create_communications = page.locator(BUTTON_CREATE_COMMUNICATIONS)
        self.button_delete_all_communications = page.locator(BUTTON_DELETE_ALL_COMMUNICATIONS)
        self.file_upload_requirements = page.locator('[class*="_requirements_"]')
        self.delete_file_confirmation = self.modal_window.locator('[data-testid="upload_delete_ok"]')
        self.delete_files_confirmation = self.modal_window.locator('[data-testid="upload_delete_all_ok"]')

    def fill_address_book(self, text: str):
        """Fill address book with text"""
        self.input_address_book.clear()
        self.page.wait_for_timeout(1000)
        self.input_address_book.fill(text)
        self.page.wait_for_timeout(1000)

    def assert_address_book_text(self, text: str):
        """Check address book text"""
        self.page.wait_for_timeout(2000)
        expect(self.input_address_book).to_contain_text([text])

    def click_personal_info(self):
        self.button_personal_info.click()
        self.page.wait_for_selector(INPUT_LOGIN, timeout=self.timeout)

    def fill_quota_time(self, minutes: str):
        self.page.wait_for_timeout(500)
        self.input_quota_time.clear()
        self.page.wait_for_timeout(1000)
        self.input_quota_time.type(minutes, delay=5)

    def press_add_in_quotas(self):
        """Working in table and modal window"""
        self.page.get_by_role("button", name="Добавить", exact=True).click()
        self.page.wait_for_selector(MODAL_WINDOW, timeout=self.timeout)

    def press_add_in_modal_in_quotas(self):
        """Working in table and modal window"""
        self.page.wait_for_selector(BUTTON_ACCEPT, timeout=self.timeout)
        self.page.locator(MODAL_WINDOW).locator(BUTTON_ACCEPT).click()
        self.page.wait_for_selector(MODAL_WINDOW, timeout=self.timeout)

    def press_save(self):
        self.page.get_by_role("button", name="Сохранить").click()
        self.page.wait_for_timeout(500)

    def press_save_in_rights(self):
        self.button_accept.click()
        self.page.wait_for_timeout(500)

    def go_to_operator_from_table(self):
        self.page.locator('[aria-rowindex="2"]').locator('[class="rs-table-cell rs-table-cell-first"]').click()
        self.page.wait_for_load_state(state="load", timeout=self.timeout)
        self.page.wait_for_selector(INPUT_LOGIN, timeout=self.timeout)

    def change_login(self, login: str):
        self.page.wait_for_selector(INPUT_LOGIN, timeout=self.timeout)
        self.page.wait_for_load_state(state="load", timeout=self.timeout)
        self.input_login.clear()
        self.input_login.type(login, delay=5)

    def change_industry(self, industry: str):
        self.select_industry.click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        self.menu.get_by_text(industry, exact=True).click()

    def assert_industries_list(self, industries_list: str):
        self.select_industry.click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        expect(self.menu).to_contain_text(industries_list)
        self.input_phone.click()

    def change_partner(self, partner: str):
        self.select_partner.click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        self.page.locator(MENU).get_by_text(partner, exact=True).click()

    def click_all_checkboxes_on_page(self):
        # Находим все чекбоксы на странице
        checkboxes = self.page.query_selector_all('input[type="checkbox"]')
        # Выполняем клик на каждом чекбоксе
        for checkbox in checkboxes:
            if not checkbox.is_checked():
                checkbox.click()

    def fill_personal_information_admin_and_manager(self, name: str, email: str, phone: str, comment: str, timezone: str, user_lang: str):
        """admin and manager can see and write comment"""
        self.page.wait_for_timeout(500)
        self.input_name.clear()
        self.input_name.type(name, delay=5)
        self.page.wait_for_selector(f'[value="{name}"]', timeout=self.timeout)
        self.input_email.clear()
        self.input_email.type(email, delay=5)
        self.page.wait_for_selector(f'[value="{email}"]', timeout=self.timeout)
        self.input_phone.clear()
        self.input_phone.type(phone, delay=5)
        self.page.wait_for_selector(f'[value="{phone}"]', timeout=self.timeout)
        self.input_comment.clear()
        self.input_comment.fill(comment)
        self.page.wait_for_timeout(1000)
        self.select_user_lang.click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        self.menu.get_by_text(user_lang, exact=True).click()
        self.page.wait_for_timeout(500)
        self.input_timezone.click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        self.page.get_by_text(timezone).click()
        self.page.wait_for_selector(f'[value="{timezone}"]', state="hidden")

    def fill_personal_information_user_and_operator(self, name: str, email: str, phone: str, timezone: str, user_lang: str):
        """user and operator cant see and write comment"""
        self.page.wait_for_timeout(500)
        self.input_name.clear()
        self.input_name.type(name, delay=5)
        self.page.wait_for_selector(f'[value="{name}"]', timeout=self.timeout)
        self.input_email.clear()
        self.input_email.type(email, delay=5)
        self.page.wait_for_selector(f'[value="{email}"]', timeout=self.timeout)
        self.input_phone.clear()
        self.input_phone.type(phone, delay=5)
        self.page.wait_for_selector(f'[value="{phone}"]', timeout=self.timeout)
        self.page.wait_for_timeout(1000)
        self.select_user_lang.click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        self.menu.get_by_text(user_lang, exact=True).click()
        self.page.wait_for_timeout(500)
        self.input_timezone.click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        self.page.wait_for_timeout(500)
        self.menu.get_by_text(timezone).click()
        self.page.wait_for_selector(f'[value="{timezone}"]', state="hidden")
        self.page.wait_for_timeout(500)

    def click_to_gpt_tab(self):
        """Click to GPT tab in quotas"""
        self.button_gpt_in_quotas.click()
        self.page.wait_for_timeout(2000)

    # def type_chat_gpt_quota_value(self, value: str):
    #     self.input_chat_gpt_quota_value.clear()
    #     self.input_chat_gpt_quota_value.type(value, delay=30)
    #
    # def type_yandex_gpt_quota_value(self, value: str):
    #     self.input_yandex_gpt_quota_value.clear()
    #     self.input_yandex_gpt_quota_value.type(value, delay=30)

    def fill_quota_value(self, number: int, value: str):
        self.page.locator('[placeholder="Новое значение"]').nth(number).clear()
        self.page.locator('[placeholder="Новое значение"]').nth(number).type(value, delay=5)

    def change_role(self, role: str):
        self.select_role.click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        self.menu.get_by_text(role).click()

    def click_to_upload_files(self):
        self.page.wait_for_selector(BUTTON_UPLOAD, timeout=self.timeout)
        self.page.locator(BUTTON_UPLOAD).click()
        self.page.wait_for_selector(BUTTON_CREATE_COMMUNICATIONS, timeout=self.timeout)

    def set_input_files(self, file: str):
        self.page.locator('[name="audio"]').set_input_files(file)
        self.page.wait_for_timeout(2000)

# TO DO move up

def all_checkboxes_to_be_checked(page="page: Page"):
    page.wait_for_timeout(500)
    # Находим все чекбоксы на странице
    checkboxes = page.query_selector_all('input[type="checkbox"]')
    page.wait_for_timeout(500)
    # Проверяем состояние каждого чекбокса
    all_checked = all(checkbox.is_checked() for checkbox in checkboxes)
    return all_checked

