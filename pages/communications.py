from pages.base_class import *


NAYDENO_ZVONKOV = '[class*="CallsHeader_callsTitleText"]'
FIRST_PAGE_PAGINATION = '[aria-label="page 1"]'
CALL_DATE_AND_TIME = '//html/body/div/div/div[2]/div/div[3]/div[2]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/p'
CHANGE_SORT = '//*[@id="root"]/div/div[2]/div/div[3]/div[1]/div/div[2]/div/div[1]/div/div/div[2]/div'
COMMENT_AREA = '[class*="styles_content_"]'
ALL_COMMENTS_AREA = '[class*="styles_withAllComments_"]'
SELECT_WITH_SEARCH_MANUAL_TAGS = '[data-testid="CustomSelectWithSearch"]'
TAG_WITHOUT_VALUE = '[class*="styles_tagSimple"]'
TAG_WITH_VALUE = '[class*="styles_tagTablet"]'

INPUT_CLIENT_NUMBER = '[data-testid="filters_client_phone"]'
INPUT_CLIENT_DICT_OR_TEXT = '[data-testid="filters_client_phrases"]'
INPUT_EMPLOYEE_NUMBER = '[data-testid="filters_operator_phone"]'
INPUT_EMPLOYEE_DICT_OR_TEXT = '[data-testid="filters_operator_phrases"]'
INPUT_TIME = '[data-testid="filters_call_time_interval"]'
INPUT_CALL_DURATION = '[data-testid="filters_call_duration"]'
INPUT_ID = '[data-testid="filters_any_id"]'
INPUT_BY_TAGS = '[data-testid="filters_search_by_tags"]'

BUTTON_CALLS_ACTION = '[data-testid="calls_actions_actions-btn"]'    # (...) button
BUTTON_CLEAR = '[data-testid="calls_btns_clear"]'
BUTTON_ADD_CONDITION = '[data-testid="addCondition_search_by_tags"]'
BUTTON_GPT = '[href*="/call/gpt?callId="]'
BUTTON_ADD_COMMENT = '[class*="styles_addButton"]'
BUTTON_ADD_COMMENT_TITLE = '[class*="styles_addTitleButton"]'
BUTTON_SAVE_TEMPLATE = '[data-testid="calls_btns_save-temp"]'
BUTTON_RETAG = '[data-testid="calls_actions_retag"]'
CURRENT_TEMPLATE_NAME = '[data-testid="templatesCalls"]'

BUTTON_ADD_GPT_RULE = '[data-testid="addRuleBtn"]'

COMMUNICATIONS_SEARCH = "//h6[contains(text(),'Поиск по коммуникациям')]"

OPEN_CALL_AREA = '[class="MuiAccordion-region"]'
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
AUDIO_PLAYER = '[class*="react-audio-player"]'

BLOCK_CHECK_LISTS = '[class*="_CallsCheckLists_"]'
TOOLTIP_IN_CHECK_LIST = ('[aria-label="Если чек-лист имеет отрицательные значения, то процент будет считаться '
                         'по следующей формуле: (итог. балл - мин.балл) / (макс.балл - мин.балл) * 100"]')
CHECK_LIST_PERCENT = '[class*="scorePercent"]'
CHECK_LIST_NAME = '[class="CheckListGroupLabel"]'
CHECK_LIST_MIN_MAX ='[class*="_minMaxPoints_"]'
POINTS_IN_CHECK_LISTS_LIST = '[class*="pointsWithQuestion_"]'
CHECK_LIST_VALUES_IN_CALL_HEADER = '[class*="_allScore_"]'

class Communications(BaseClass):
    def __init__(self, page: Page):
        super().__init__(page)
        self.template_name = page.locator(CURRENT_TEMPLATE_NAME)
        self.button_calls_action = page.locator(BUTTON_CALLS_ACTION).locator('[type="button"]')
        self.button_ex_from_call = page.locator(OPEN_CALL_AREA).locator('[aria-label="Excel экспорт"]').locator('[type="button"]')
        self.button_add_comment = page.locator(BUTTON_ADD_COMMENT)
        self.button_cross_in_manual_tags = page.locator('[class*="_manualGroup_"]').locator('[type="button"]')
        self.button_submit_in_word_processing = page.locator(BLOCK_WITH_BUTTON).locator(BUTTON_SUBMIT)
        self.button_save_template = page.locator(BUTTON_SAVE_TEMPLATE)
        self.communications_found = page.locator('[class*="CallsHeader_callsTitleText"]')

        self.sort = page.locator(CHANGE_SORT)
        self.tag_without_value = page.locator(TAG_WITHOUT_VALUE)
        self.tag_with_value = page.locator(TAG_WITH_VALUE)
        self.button_clear = page.locator(BUTTON_CLEAR)
        self.call_date_and_time = page.locator(CALL_DATE_AND_TIME)
        self.just_click = page.locator(COMMUNICATIONS_SEARCH)
        self.input_client_number = page.locator(INPUT_CLIENT_NUMBER).locator('[type="text"]')
        self.input_client_dict_or_text = page.locator(INPUT_CLIENT_DICT_OR_TEXT).locator('[type="text"]')
        self.input_employee_number = page.locator(INPUT_EMPLOYEE_NUMBER).locator('[type="text"]')
        self.input_employee_dict_or_text = page.locator(INPUT_EMPLOYEE_DICT_OR_TEXT).locator('[type="text"]')
        self.input_time = page.locator(INPUT_TIME).locator('[type="text"]')
        self.input_call_duration = page.locator(INPUT_CALL_DURATION).locator('[type="text"]')
        self.input_id = page.locator(INPUT_ID).locator('[type="text"]')
        self.input_by_tags = page.locator(INPUT_BY_TAGS).locator('[type="text"]')
        self.input_manual_tag_name = page.locator(SELECT_WITH_SEARCH_MANUAL_TAGS).locator('[type="text"]')
        self.vert_dots_in_template = page.locator('[class=" css-izdlur"]')

    def assert_check_period_dates(self, begin: str, end: str):
        """Check first and last dates"""
        self.page.wait_for_timeout(1000)
        expect(self.first_date).to_have_value(begin)
        expect(self.last_date).to_have_value(end)

    def assert_check_period_dates_disabled(self):
        """Check that dates disabled if all-time"""
        expect(self.first_date).to_be_disabled()
        expect(self.last_date).to_be_disabled()

    def press_find_communications_more_than_50(self):
        """If more than 50, waiting pagination"""
        self.page.wait_for_timeout(1000)
        self.button_find_communications.click()
        self.page.wait_for_timeout(1000)
        self.page.wait_for_selector(NAYDENO_ZVONKOV, timeout=self.timeout)
        self.page.wait_for_timeout(1000)
        self.page.wait_for_selector(FIRST_PAGE_PAGINATION, timeout=self.timeout)
        self.page.wait_for_timeout(1000)

    def press_find_communications_less_than_50(self):
        """If less than 50, not waiting pagination"""
        self.page.wait_for_timeout(1500)
        self.button_find_communications.click()
        self.page.wait_for_timeout(1000)
        self.page.wait_for_selector(NAYDENO_ZVONKOV, timeout=self.timeout)
        self.page.wait_for_timeout(1000)

    def assert_communications_found(self, text: str):
        self.page.wait_for_selector(NAYDENO_ZVONKOV, timeout=self.timeout)
        self.page.wait_for_timeout(2000)
        expect(self.communications_found.nth(0)).to_have_text(text, timeout=self.timeout)

    def change_sort(self, sort_type: str):
        """Change sort"""
        self.sort.click()
        self.menu.get_by_text(sort_type).click()
        self.page.wait_for_selector(FIRST_PAGE_PAGINATION, timeout=self.timeout)

    def assert_call_date_and_time(self, text: str):
        expect(self.call_date_and_time).to_have_text(text, timeout=self.timeout)

    def fill_client_number(self, text: str):
        """Fill filter client number"""
        self.input_client_number.type(text, delay=5)
        self.page.wait_for_timeout(500)
        self.just_click.click()  # tupo click

    def fill_employee_number(self, text: str):
        """Fill filter employee number"""
        self.input_employee_number.type(text, delay=5)
        self.page.wait_for_timeout(500)
        self.just_click.click()  # tupo click

    def fill_time(self, time: str):
        """Fill exact time"""
        self.input_time.type(time, delay=5)
        self.page.wait_for_timeout(500)
        self.just_click.click()  # tupo click

    def fill_id(self, communication_id: str):
        """Fill ID"""
        self.page.wait_for_selector(INPUT_ID, timeout=self.timeout)
        self.input_id.type(communication_id, delay=5)
        self.page.wait_for_timeout(500)
        self.just_click.click()  # tupo click

    def fill_search_length(self, value: str):
        """Fill search length"""
        self.page.wait_for_timeout(500)
        self.input_call_duration.clear()
        self.page.wait_for_timeout(500)
        self.input_call_duration.type(value, delay=5)
        self.page.wait_for_timeout(500)
        self.just_click.click()  # tupo click

    def fill_client_dict_or_text(self, search_text: str, result_text: str):
        """Fill client dict or text"""
        self.input_client_dict_or_text.clear()
        self.input_client_dict_or_text.type(search_text, delay=5)
        self.page.wait_for_timeout(500)
        self.menu.get_by_text(result_text).click()
        self.just_click.click()  # tupo click

    def fill_employee_dict_or_text(self, search_text: str, result_text: str):
        """Fill employee dict or text"""
        self.input_employee_dict_or_text.clear()
        self.input_employee_dict_or_text.type(search_text, delay=5)
        self.page.wait_for_timeout(500)
        self.menu.get_by_text(result_text).click()
        self.just_click.click()  # tupo click

    def fill_by_tag(self, input_number: int, text: str):
        """Fill by tag"""
        self.page.wait_for_timeout(1000)
        self.input_by_tags.nth(input_number).type(text, delay=5)
        self.page.wait_for_timeout(1500)
        self.menu.locator('[id*="-option-0"]').get_by_text(text, exact=True).click()
        self.just_click.click()  # tupo click
        self.page.wait_for_timeout(500)

    def press_clear_button(self):
        """Press clear button"""
        self.button_clear.click()

    def press_calls_action_button_in_list(self, number: int):
        """(...) in list"""
        self.button_calls_action.nth(number).click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)

    def expand_call(self):
        """Expand call"""
        self.page.wait_for_timeout(3000)
        self.page.wait_for_selector(BUTTON_EXPAND_CALL, timeout=self.timeout)
        self.page.wait_for_timeout(4000)
        self.button_expand_call.click()
        self.page.wait_for_timeout(1000)
        self.page.wait_for_selector(ALL_COMMENTS_AREA, timeout=self.timeout)

    def press_cross_in_manual_tags(self):
        """Press + in manual tags"""
        self.page.wait_for_timeout(500)
        self.button_cross_in_manual_tags.click()
        self.page.wait_for_selector(SELECT_WITH_SEARCH_MANUAL_TAGS, timeout=self.timeout)

    def add_manual_tag_name(self, text: str):
        """Add manual tag name"""
        self.input_manual_tag_name.type(text, delay=10)
        self.page.wait_for_timeout(1000)

    def delete_manual_tag_from_call_header(self, number: int):
        """Press pencil and delete manual tag from call header"""
        self.page.wait_for_timeout(500)
        self.page.locator(BLOCK_ONE_COMMUNICATION).locator('[fill="#d9f7be"]').nth(number).click()
        self.page.wait_for_selector('[role="tooltip"]', timeout=self.timeout)
        self.page.locator('[role="tooltip"]').get_by_text("Удалить").click()
        self.page.wait_for_selector(MODAL_WINDOW, timeout=self.timeout)
        self.modal_window.locator(BUTTON_SUBMIT).click()
        self.page.wait_for_selector(MODAL_WINDOW, state="hidden", timeout=self.timeout)

    def delete_manual_tag_from_manual_tags(self, number: int):
        """Press pencil and delete manual tag from manual tag list"""
        self.page.wait_for_timeout(500)
        self.page.locator('[class*="_manualGroup_"]').locator('[fill="#d9f7be"]').nth(number).click()
        self.page.wait_for_selector('[role="tooltip"]', timeout=self.timeout)
        self.page.locator('[role="tooltip"]').get_by_text("Удалить").click()
        self.page.wait_for_selector(MODAL_WINDOW, timeout=self.timeout)
        self.modal_window.locator(BUTTON_SUBMIT).click()
        self.page.wait_for_selector(MODAL_WINDOW, state="hidden", timeout=self.timeout)

    def assert_tags_have_count(self, without_value: int, with_value: int):
        self.page.wait_for_load_state(state="load", timeout=self.timeout)
        self.page.wait_for_timeout(2500)
        expect(self.tag_with_value).to_have_count(with_value, timeout=self.timeout)
        self.page.wait_for_timeout(2500)
        expect(self.tag_without_value).to_have_count(without_value, timeout=self.timeout)

    def press_add_comment(self):
        """Press add comment button"""
        self.button_add_comment.click()
        self.page.wait_for_selector('[class*="styles_textareaWrapper"]', timeout=self.timeout)

    def click_submit_in_word_processing(self):
        """Press (submit) in word pocessing modal"""
        self.page.wait_for_timeout(500)
        self.button_submit_in_word_processing.click()
        self.page.wait_for_timeout(500)

    def press_calls_list_download_button(self, number):
        """Press download in calls list"""
        self.button_calls_list_download.nth(number).click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)

    def press_ex_button_in_expanded_call(self):
        self.button_ex_from_call.click()
        self.page.wait_for_selector(MODAL_WINDOW, timeout=self.timeout)

    def press_save_template(self):
        """Press save template"""
        self.button_save_template.click()
        self.page.wait_for_timeout(500)
        self.page.wait_for_selector(MODAL_WINDOW, timeout=self.timeout)

    def press_rename_template(self):
        """Press rename template"""
        self.vert_dots_in_template.click()
        self.page.wait_for_timeout(500)
        self.menu.get_by_text("Переименовать", exact=True).click()
        self.page.wait_for_selector(MODAL_WINDOW, timeout=self.timeout)

    def press_delete_template(self):
        """Press delete template"""
        self.vert_dots_in_template.click()
        self.page.wait_for_timeout(500)
        self.menu.get_by_text("Удалить", exact=True).click()
        self.page.wait_for_selector(MODAL_WINDOW, timeout=self.timeout)

    def assert_template_name(self, template_name: str):
        self.page.wait_for_timeout(2000)
        self.page.wait_for_selector(CURRENT_TEMPLATE_NAME, timeout=self.timeout)
        expect(self.template_name).to_have_text(template_name)

    def assert_menu_values(self, values: str):
        expect(self.menu).to_have_text(values)

    def fill_name(self, name: str):
        """Used for fill new search template name, but can be used for any name if same selector"""
        self.input_name.type(name, delay=5)






