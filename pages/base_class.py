from playwright.sync_api import Page, expect, BrowserContext, Route

BUTTON_COMMUNICATIONS = '[value="calls"]'
BUTTON_SHARE_CALL = '[data-testid="call_share"]'
BUTTON_EXPAND_CALL = '[data-testid="call_expand"]'
BUTTON_CALLS_LIST_DOWNLOAD = '[data-testid="calls_actions_download"]'
BUTTON_REPORTS = '[value="reports"]'
BUTTON_CREATE_REPORT_IN_MENU = '[href*="/report/create"]'
BUTTON_GENERATE_REPORT = '[data-testid="reportMake"]'
BUTTON_MANAGE_REPORTS = '[href*="/reports"]'
BUTTON_MARKUP = '[value="tags"]'
BUTTON_DICTS = '[data-testid="markup_nav_dicts"]'
BUTTON_ADD_DICT = '[data-testid="markup_addDict"]'
BUTTON_CHECK_LIST = '[data-testid="markup_nav_checklists"]'
BUTTON_GPT = '[data-testid="markup_nav_gpt"]'
BUTTON_NOTIFICATIONS = '[value="notifications"]'
BUTTON_DEALS = '[value="deals"]'
BUTTON_FIND_DEALS = '[data-testid="deals_btns_find"]'
BUTTON_SETTINGS = '[value="settings"]'
BUTTON_USERS = '[data-testid="userLink"]'
BUTTON_RIGHTS = '[href*="/access-rights"]'
BUTTON_FIND_COMMUNICATIONS = '[data-testid="calls_btns_find"]'
BLOCK_ONE_COMMUNICATION = '[class*="MuiAccordionSummary-content"]'
BUTTON_EMPLOYEES = '[href*="settings/employees"]'
BUTTON_ACTIONS_WITH_CALLS = '[href*="/actions-with-calls"]'
BLOCK_ACTION_SELECT = '[class="action-block"]'
BUTTON_WORD_PROCESSING = '[href*="/word-processing"]'
BUTTON_QUOTAS = '[href*="settings/quotas"]'
BUTTON_CONSUMPTION_HISTORY = '[href*="-consumption-history"]'
BUTTON_TARIFFICATION = '[href*="/settings/billing"]'
BUTTON_ADDRESS_BOOK = '[href*="/address-book"]'
INPUT_ADDRESS_BOOK = '[class*="AddressBookTextArea"]'
BUTTON_INTEGRATIONS_IN_MENU = '[href*="settings/integrations"]'
BUTTON_SUBMIT = '[type="submit"]'
BUTTON_ACCEPT = '[data-testid="acceptButton"]'
BUTTON_OTMENA = '[data-testid="cancelButton"]'
BUTTON_SAVE = '[data-testid="saveButton"]'
MENU = '[class*="-menu"]'
MODAL_WINDOW = '[role="dialog"]'
BUTTON_CROSS = '[data-testid="closePopupButton"]'
BUTTON_CLOSE = '[data-testid="CloseIcon"]'
INPUT_SEARCH = '[name="searchString"]'
BUTTON_PENCIL = '[aria-label="Изменить название"]'
BUTTON_KORZINA = '[aria-label="Удалить"]'
BUTTON_ADD_GROUP = '[data-testid="markup_addGroup"]'
INPUT_NEW_GROUP_NAME = '[name="groupName"]'
CHECKBOX = '[type="checkbox"]'

SELECT_LANGUAGE = '[data-testid="stt_language"]'
SELECT_ENGINE = '[data-testid="stt_engine"]'
SELECT_MODEL = '[data-testid="stt_model"]'

INPUT_NAME = '[name="name"]'
INPUT_LOGIN = '[name="login"]'
INPUT_PASSWORD = '[name="password"]'
INPUT_EMAIL = '[name="email"]'
INPUT_PHONE = '[name="phoneNumber"]'
INPUT_COMMENT = '[name="comment"]'
SELECT_ROLE = '[data-testid="selectRole"]'
SELECT_USER_LANG = '[data-testid="selectLanguage"]'
SELECT_INDUSTRY = '[data-testid="selectIndustry"]'
SELECT_PARTNER = '[data-testid="selectPartner"]'
INPUT_NEW_PASSWORD = '[name="newPassword"]'
INPUT_NEW_PASSWORD_REPEAT = '[name="newPasswordRepeat"]'
INPUT_GPT_QUESTION = '[placeholder="Сформулируйте свой вопрос..."]'

ALERT_MESSAGE = '[class*="styles_firstLine__"]'
ALERT_MESSAGE_SECOND = '[class*="styles_secondLine__"]'

class BaseClass:
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 70000
        self.users_list = page.locator("#react-select-2-input")
        self.login = page.locator('[id="username"]')
        self.password = page.locator('[id="password"]')
        self.button_enter = page.locator(BUTTON_SUBMIT)
        self.button_accept = page.locator(BUTTON_ACCEPT)
        self.menu = page.locator(MENU)
        self.modal_window = page.locator(MODAL_WINDOW)
        self.snackbar = page.locator('[class*="SnackbarItem-wrappedRoot"]')
        '''Dates and calendar'''
        self.yesterday = page.locator('[data-testid="yesterday"]')
        self.week = page.locator('[data-testid="week"]')
        self.month = page.locator('[data-testid="month"]')
        self.quarter = page.locator('[data-testid="quarter"]')
        self.year = page.locator('[data-testid="year"]')
        self.all_time = page.locator('[value="all_time"]')
        self.first_date = page.locator('[date-range="start"]')
        self.last_date = page.locator('[date-range="end"]')
        '''Word processing'''
        self.select_language = page.locator(SELECT_LANGUAGE)#.locator('[type="text"]')
        self.select_engine = page.locator(SELECT_ENGINE)
        self.select_model = page.locator(SELECT_MODEL)
        '''User info'''
        self.input_login = page.locator(INPUT_LOGIN)
        self.input_name = page.locator(INPUT_NAME)
        self.input_email = page.locator(INPUT_EMAIL)
        self.input_phone = page.locator(INPUT_PHONE)
        self.input_comment = page.locator(INPUT_COMMENT)
        self.input_password = page.locator(INPUT_PASSWORD)
        self.select_user_lang = page.locator(SELECT_USER_LANG).locator("svg")
        self.select_industry = page.locator(SELECT_INDUSTRY)
        self.select_partner = page.locator(SELECT_PARTNER)
        self.input_new_password = page.locator(INPUT_NEW_PASSWORD)
        self.input_new_password_repeat = page.locator(INPUT_NEW_PASSWORD_REPEAT)
        '''Tags'''
        self.communication_tag = page.locator('[class*="_blueTag_"]')
        self.deal_tag = page.locator('[class*="_lightBlueTag_"]')
        self.fragment_tag = page.locator('[class*="_purpleTag_"]')
        '''Other'''
        self.button_markup = page.locator(BUTTON_MARKUP)
        self.button_dicts = page.locator(BUTTON_DICTS)
        self.button_check_list = page.locator(BUTTON_CHECK_LIST)
        self.button_gpt = page.locator(BUTTON_GPT)
        self.button_users = page.locator(BUTTON_USERS)
        self.button_add_group = page.locator(BUTTON_ADD_GROUP)
        self.input_new_group_name_field = page.locator(INPUT_NEW_GROUP_NAME)
        self.button_korzina = page.locator(BUTTON_KORZINA)
        self.button_pencil = page.locator(BUTTON_PENCIL)
        self.button_employees = page.locator(BUTTON_EMPLOYEES)
        self.button_quotas = page.locator(BUTTON_QUOTAS)
        self.button_address_book = page.locator(BUTTON_ADDRESS_BOOK)
        self.button_integrations_in_menu = page.locator(BUTTON_INTEGRATIONS_IN_MENU)
        self.button_rights = page.locator(BUTTON_RIGHTS)
        self.button_word_pocessing = page.locator(BUTTON_WORD_PROCESSING)
        self.button_share_call = page.locator(BUTTON_SHARE_CALL).locator('[type="button"]')
        self.button_expand_call = page.locator(BUTTON_EXPAND_CALL)
        self.button_calls_list_download = page.locator(BUTTON_CALLS_LIST_DOWNLOAD)
        self.input_search = page.locator(INPUT_SEARCH)
        self.button_find_communications = page.locator(BUTTON_FIND_COMMUNICATIONS)
        self.block_one_communication = page.locator(BLOCK_ONE_COMMUNICATION)
        self.button_cross = page.locator(BUTTON_CROSS)
        self.alert_message = page.locator(ALERT_MESSAGE)
        self.alert_message_second = page.locator(ALERT_MESSAGE_SECOND)

    def navigate(self, url: str):
        """Opens main page"""
        #self.page.route('**/*.png', lambda route: route.abort())
        self.page.goto(url, timeout=self.timeout)

    def auth(self, login: str, password: str):
        """Auth"""
        self.page.wait_for_selector("[id='username']", timeout=self.timeout)
        self.login.type(login, delay=5)
        self.page.wait_for_selector("[id='password']", timeout=self.timeout)
        self.password.type(password, delay=5)
        self.page.wait_for_selector(BUTTON_SUBMIT, timeout=self.timeout)
        self.button_enter.click()
        self.page.wait_for_timeout(1000)
        self.page.wait_for_load_state(state="load", timeout=self.timeout)
        self.page.wait_for_timeout(1000)

    def reload_page(self):
        """Reload page, wait for load and 1 second more"""
        self.page.reload()
        self.page.wait_for_load_state(state="load", timeout=self.timeout)
        self.page.wait_for_selector('[alt="Imot.io loader"]', state="hidden")
        self.page.wait_for_load_state(state="load", timeout=self.timeout)
        self.page.wait_for_timeout(1000)

    def go_to_user(self, name: str):
        """Change user"""
        self.page.wait_for_timeout(5000)
        self.users_list.type(name, delay=10)
        self.page.get_by_text(name, exact=True).click()
        #self.page.wait_for_selector('[class*="CallsHeader"]')
        self.page.wait_for_load_state(state="load", timeout=self.timeout)
        self.page.wait_for_timeout(2000)

    def quit_from_profile(self):
        self.page.wait_for_timeout(500)
        #self.page.get_by_label("Профиль").click()
        self.page.locator('[class*="MuiIconButton-sizeSmall"]').nth(2).click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        self.menu.locator('[id*="option-1"]').click()
        #self.menu.get_by_text("Выйти", exact=True).click()
        self.page.wait_for_timeout(2000)

    def assert_quited(self):
        expect(self.button_enter).to_be_visible()

    def choose_period_date(self, first_date: str, last_date: str):
        """Choose period"""
        self.page.wait_for_timeout(2500)
        self.page.wait_for_selector('[class="ant-space-item"]', timeout=self.timeout)
        self.page.wait_for_timeout(2000)
        self.first_date.click(timeout=self.timeout)
        self.page.wait_for_timeout(300)
        self.first_date.fill(first_date)
        self.page.wait_for_timeout(300)
        self.last_date.click(timeout=self.timeout)
        self.page.wait_for_timeout(300)
        self.last_date.fill(last_date)
        self.page.wait_for_timeout(300)
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(300)

    def select_period_value(self, period: str):
        """Select period"""
        self.page.wait_for_selector('[class*="shown"]', timeout=self.timeout)
        self.page.locator(f'[data-testid="{period}"]').click()
        self.page.wait_for_selector('[class*="shown"]', state="hidden")
        self.page.wait_for_timeout(500)

    def press_key(self, key: str):
        """Press key on keyboard"""
        self.page.wait_for_timeout(1000)
        self.page.keyboard.press(key)
        self.page.wait_for_timeout(1000)

    def check_alert(self, message: str):
        """Wait snackbar, check text, wait for close"""
        self.snackbar.wait_for(state="visible", timeout=self.timeout)
        expect(self.snackbar).to_contain_text(message)
        self.snackbar.wait_for(state="hidden", timeout=self.timeout)

    def click_notifications(self):
        """Click Notifications"""
        self.page.wait_for_selector(BUTTON_NOTIFICATIONS, timeout=self.timeout)
        self.page.wait_for_timeout(1000)
        self.page.locator(BUTTON_NOTIFICATIONS).click(timeout=self.timeout)
        self.page.wait_for_load_state(state="load", timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def click_deals(self):
        """Click Deals"""
        self.page.wait_for_selector(BUTTON_DEALS, timeout=self.timeout)
        self.page.wait_for_timeout(500)
        self.page.locator(BUTTON_DEALS).click()
        self.page.wait_for_load_state(state="load", timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def click_settings(self):
        """Click Settings"""
        self.page.wait_for_selector(BUTTON_SETTINGS, timeout=self.timeout)
        self.page.wait_for_timeout(500)
        self.page.locator(BUTTON_SETTINGS).click()
        self.page.wait_for_load_state(state="load", timeout=self.timeout)
        self.page.wait_for_timeout(500)
        self.page.wait_for_selector(INPUT_LOGIN, timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def click_communications(self):
        """Click Communications"""
        self.page.wait_for_selector(BUTTON_COMMUNICATIONS, timeout=self.timeout)
        self.page.wait_for_timeout(500)
        self.page.locator(BUTTON_COMMUNICATIONS).click()
        self.page.wait_for_timeout(500)
        self.page.wait_for_selector(BUTTON_FIND_COMMUNICATIONS, timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def click_reports(self):
        """Click Reports"""
        self.page.wait_for_selector(BUTTON_REPORTS, timeout=self.timeout)
        self.page.wait_for_timeout(500)
        self.page.locator(BUTTON_REPORTS).click()
        self.page.wait_for_load_state(state="load", timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def press_create_report(self):
        self.page.wait_for_selector(BUTTON_CREATE_REPORT_IN_MENU, timeout=self.timeout)
        self.page.wait_for_timeout(500)
        self.page.locator(BUTTON_CREATE_REPORT_IN_MENU).click()
        self.page.wait_for_timeout(500)
        self.page.wait_for_selector(BUTTON_GENERATE_REPORT, timeout=self.timeout)

    def press_report_management(self):
        self.page.wait_for_selector(BUTTON_MANAGE_REPORTS, timeout=self.timeout)
        self.page.locator(BUTTON_MANAGE_REPORTS).click()
        self.page.wait_for_selector('[role="table"]', timeout=self.timeout)

    def click_markup(self):
        """Click Markup"""
        self.page.wait_for_selector(BUTTON_MARKUP, timeout=self.timeout)
        self.button_markup.click()
        self.page.wait_for_load_state(state="load", timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def click_to_dicts(self):
        """Go to dicts"""
        self.page.wait_for_timeout(1000)
        self.page.wait_for_selector(BUTTON_DICTS, timeout=self.timeout)
        self.page.wait_for_timeout(1000)
        self.button_dicts.click()
        self.page.wait_for_timeout(1000)
        self.page.wait_for_load_state(state="load", timeout=self.timeout)

    def click_check_lists(self):
        """Go to check lists"""
        self.page.wait_for_selector(BUTTON_CHECK_LIST, timeout=self.timeout)
        self.page.wait_for_timeout(1000)
        self.button_check_list.click()
        self.page.wait_for_timeout(500)
        self.page.wait_for_load_state(state="load", timeout=self.timeout)

    def click_gpt(self):
        """Go to gpt"""
        self.page.wait_for_selector(BUTTON_GPT, timeout=self.timeout)
        self.button_gpt.click()
        self.page.wait_for_selector('[filter="url(#filter0_b_4973_59500)"]', timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def click_rights(self):
        self.button_rights.click()
        self.page.wait_for_timeout(1000)
        self.page.wait_for_selector(BUTTON_ACCEPT, timeout=self.timeout)

    def click_employees(self):
        """Click employees in left menu"""
        self.button_employees.click()
        self.page.wait_for_load_state(state="load", timeout=self.timeout)
        self.page.wait_for_selector('[role="grid"]', timeout=self.timeout)

    def go_to_users_list(self):
        self.page.wait_for_selector(BUTTON_USERS, timeout=self.timeout)
        self.button_users.click()
        self.page.wait_for_timeout(1000)
        self.page.wait_for_selector('[class="circular-progress"]', state='hidden', timeout=self.timeout)

    def click_actions_with_calls(self):
        self.page.locator(BUTTON_ACTIONS_WITH_CALLS).click()
        self.page.wait_for_selector(BLOCK_ACTION_SELECT, timeout=self.timeout)

    def click_word_processing(self):
        self.button_word_pocessing.click()
        self.page.wait_for_selector(SELECT_LANGUAGE, timeout=self.timeout)

    def click_quota(self):
        self.page.wait_for_timeout(500)
        self.button_quotas.click()
        self.page.wait_for_timeout(500)
        self.page.wait_for_selector('[role="grid"]', timeout=self.timeout)

    def click_address_book(self):
        """Click address book button"""
        self.page.wait_for_timeout(500)
        self.button_address_book.click()
        self.page.wait_for_selector(INPUT_ADDRESS_BOOK, timeout=self.timeout)

    def press_integrations_in_menu(self):
        self.button_integrations_in_menu.click(timeout=self.timeout)
        self.page.wait_for_timeout(700)

    def click_language_select(self):
        """Select language in word processing"""
        self.select_language.click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def click_engine_select(self):
        """Select engine in word processing"""
        self.select_engine.click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def click_model_select(self):
        """Select model in word processing"""
        self.select_model.click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        self.page.wait_for_timeout(1000)

    def choose_option(self, option_number: int):
        """Choose option from menu"""
        self.menu.locator(f'[id$="-option-{option_number}"]').click()

    def choose_from_menu_by_text_and_wait_for_modal(self, name: str):
        self.page.wait_for_timeout(500)
        self.menu.get_by_text(name, exact=True).click()
        self.page.wait_for_timeout(1000)
        self.page.wait_for_selector(MODAL_WINDOW, timeout=self.timeout)

    def choose_user_import_from(self, username: str):
        self.page.locator('[class*="CustomSelect_simpleSelect"]').locator('[type="text"]').type(username, delay=10)
        self.menu.get_by_text(username, exact=True).click()
        self.page.wait_for_selector('[data-testid*="_importSearch}"]', timeout=self.timeout)
        self.page.wait_for_timeout(1000)

    def press_create_group(self):
        """Press create group in markup"""
        self.page.wait_for_selector(BUTTON_ADD_GROUP, timeout=self.timeout)
        self.button_add_group.click()
        self.page.wait_for_selector(INPUT_NEW_GROUP_NAME, timeout=self.timeout)

    def input_new_group_name(self, group_name: str):
        """Type new group name"""
        self.input_new_group_name_field.type(group_name, delay=10)
        self.modal_window.locator(BUTTON_ACCEPT).click()
        self.page.wait_for_timeout(500)

    def close_export_modal(self):
        self.page.wait_for_selector(BUTTON_CROSS, timeout=self.timeout)
        self.button_cross.click()
        self.page.wait_for_selector(MODAL_WINDOW, state="hidden")

    def close_modal_window(self):
        self.button_cross.click()
        self.page.wait_for_selector(MODAL_WINDOW, state="hidden", timeout=self.timeout)

