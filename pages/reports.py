from pages.base_class import *

BUTTON_SAVE_AS_NEW = '[data-testid="reportNewSave"]'
BUTTON_REPORT_UPDATE = '[data-testid="reportUpdate"]'
BUTTON_CHANGE_FILTERS = '[data-testid="report_filters_addCriterias"]'
BUTTON_COLLAPSE_EXPAND = '[class*="ShowHideCheck_checkTitle"]'
BUTTON_ADD_COLUMN = '[data-testid="report_rows_addColumn"]'
BUTTON_ADD_ROW = '[data-testid="report_rows_addRow"]'
BUTTON_CREATE_REPORT_IN_MANAGEMENT = '[data-testid="addUserButton"]'

INPUT_BY_TAGS = '[data-testid="filters_search_by_tags"]'
BUTTON_CLEAR = '[data-testid="calls_btns_clear"]'
BUTTON_RETAG = '[data-testid="calls_actions_retag"]'
BUTTON_CALLS_ACTION = '[data-testid="calls_actions_actions-btn"]'    # (...) button
NAYDENO_ZVONKOV = '[class*="CallsHeader_callsTitleText"]'
INPUT_REPORT_NAME = '[name="report_name"]'

# additional params
BUTTON_TAG_VALUE_IN_ADDITIONAL_PARAMS = '[data-testid="tagNameChange"]'
BUTTON_AVERAGE_NUMBER_TAG_VALUE = '[data-testid="avgNumTagChange"]'
BUTTON_SUM_NUMBER_TAG_VALUE = '[data-testid="sumNumTagChange"]'
BUTTON_CHECKLIST_POINT_IN_ADDITIONAL_PARAMS = '[data-testid="checklistChange"]'
BUTTON_CHECKLIST_POINT_PERCENT_IN_ADDITIONAL_PARAMS = '[data-testid="checklistChangePercent"]'
BUTTON_CHECKLIST_QUESTION_POINT_IN_ADDITIONAL_PARAMS = '[data-testid="checklistQuestionChange"]'
BUTTON_CHECKLIST_QUESTION_POINT_PERCENT_IN_ADDITIONAL_PARAMS = '[data-testid="checklistQuestionChangePercent"]'
BUTTON_CHECKLIST_FREQUENT_ANSWER_FOR_QUESTION_IN_ADDITIONAL_PARAMS = '[data-testid="checklistAnswerAvg"]'
BUTTON_COMMENT_IN_ADDITIONAL_PARAMS = '[data-testid="commentary"]'
CHECKBOX_COMMUNICATIONS_ADD_PARAMS = '[data-testid="show_calls_count"]'
CHECKBOX_SUM_TIME_ADD_PARAMS = '[data-testid="show_minutes"]'
CHECKBOX_PERCENTAGE_FROM_REPORT_ADD_PARAMS = '[data-testid="show_percentage"]'
CHECKBOX_PERCENTAGE_FROM_ROW_ADD_PARAMS = '[data-testid="show_percentage_from_all_calls_row"]'
CHECKBOX_PERCENTAGE_FROM_COLUMN_ADD_PARAMS = '[data-testid="show_percentage_from_all_calls_col"]'
CHECKBOX_PERCENTAGE_FROM_ROW_CELL_ADD_PARAMS = '[data-testid="show_percentage_from_sum_calls_row"]'
CHECKBOX_PERCENTAGE_FROM_COLUMN_CELL_ADD_PARAMS = '[data-testid="show_percentage_from_sum_calls_col"]'
CHECKBOX_CLIENT_TALK_TIME_ADD_PARAMS = '[data-testid="show_client_time"]'
CHECKBOX_CLIENT_TALK_TIME_PERCENT_ADD_PARAMS = '[data-testid="show_client_time_percentage"]'
CHECKBOX_OPERATOR_TALK_TIME_ADD_PARAMS = '[data-testid="show_operator_time"]'
CHECKBOX_OPERATOR_TALK_TIME_PERCENT_ADD_PARAMS = '[data-testid="show_operator_time_percentage"]'
CHECKBOX_SILENCE_DURATION_ADD_PARAMS = '[data-testid="show_silence_time"]'
CHECKBOX_SILENCE_DURATION_PERCENT_ADD_PARAMS = '[data-testid="show_silence_time_percentage"]'
CHECKBOX_CLIENTS_PHONES_ADD_PARAMS = '[data-testid="show_client_phones"]'
CHECKBOX_OPERATORS_PHONES_ADD_PARAMS = '[data-testid="show_operator_phones"]'

CHECKBOX_AVERAGE_POINT_CHECKLIST_ADD_PARAMS = '[data-testid="show_checklist_average"]'
CHECKBOX_AVERAGE_POINT_CHECKLIST_PERCENT_ADD_PARAMS = '[data-testid="show_checklist_average_percent"]'
CHECKBOX_FIRST_COMM_TIME_ADD_PARAMS = '[data-testid="show_first_call_dt"]'
CHECKBOX_LAST_COMM_TIME_ADD_PARAMS = '[data-testid="show_last_call_dt"]'

CHECKBOX_POINTS_SUM_ADD_PARAMS = '[data-testid="show_points"]'
CHECKBOX_POINTS_MAX_SUM_ADD_PARAMS = '[data-testid="show_max_points"]'

CHECKBOX_AVERAGE_POINT_DEAL_CHECKLIST_ADD_PARAMS = '[data-testid="show_deal_checklist_average"]'
CHECKBOX_AVERAGE_POINT_DEAL_CHECKLIST_PERCENT_ADD_PARAMS = '[data-testid="show_deal_checklist_average_percent"]'
CHECKBOX_SUM_POINTS_DEAL_CHECKLIST_ADD_PARAMS = '[data-testid="show_deal_points"]'
CHECKBOX_SUM_MIN_POINTS_DEAL_CHECKLIST_ADD_PARAMS = '[data-testid="show_deal_min_points"]'
CHECKBOX_SUM_MAX_POINTS_DEAL_CHECKLIST_ADD_PARAMS = '[data-testid="show_deal_max_points"]'


BUTTON_ADD_PARAMS_APPLY = '[data-testid="report_settings_apply"]'
BUTTON_KORZINA_IN_ADD_PARAMS = '[data-testid*="delete_btn_view_"]'

SELECT_WITH_ADDITIONAL_PARAM = '[class*="AdditionalParams_additionalSelect_"]'

class Reports(BaseClass):
    def __init__(self, page: Page):
        super().__init__(page)
        self.button_generate_report = page.locator(BUTTON_GENERATE_REPORT)
        self.button_add_column = page.locator(BUTTON_ADD_COLUMN)
        self.button_add_row = page.locator(BUTTON_ADD_ROW)
        self.button_collapse_expand = page.locator(BUTTON_COLLAPSE_EXPAND)
        self.button_add_params_apply = page.locator(BUTTON_ADD_PARAMS_APPLY)
        self.select_with_additional_param = page.locator(SELECT_WITH_ADDITIONAL_PARAM).locator('[type="text"]')
        self.button_gear_in_row = page.locator('[data-testid="report_rows_row_1_settings_btn"]')

    def press_generate_report(self):
        self.page.wait_for_timeout(500)
        self.button_generate_report.click()
        self.page.wait_for_selector('[data-id="0"]', timeout=self.timeout)

    def press_add_column(self):
        self.button_add_column.click()
        self.page.wait_for_timeout(1000)

    def press_add_row(self):
        self.button_add_row.click()
        self.page.wait_for_timeout(1000)

    def expand_report(self):
        self.button_collapse_expand.click()
        self.page.wait_for_timeout(500)
        self.page.wait_for_selector(BUTTON_ADD_COLUMN, timeout=self.timeout)

    def collapse_report(self):
        self.button_collapse_expand.click()
        self.page.wait_for_timeout(500)
        self.page.wait_for_selector(BUTTON_ADD_COLUMN, state="hidden")

    def press_create_report_in_management(self):
        self.page.wait_for_timeout(500)
        self.page.locator(BUTTON_CREATE_REPORT_IN_MANAGEMENT).click()
        self.page.wait_for_selector(BUTTON_GENERATE_REPORT, timeout=self.timeout)

    def press_save_as_new(self):
        self.page.wait_for_timeout(500)
        self.page.locator(BUTTON_SAVE_AS_NEW).click()
        self.page.wait_for_selector(MODAL_WINDOW, timeout=self.timeout)

    def assert_check_period_dates(self, begin: str, end: str):
        """Check first and last dates"""
        self.page.wait_for_timeout(500)
        expect(self.first_date).to_have_value(begin)
        expect(self.last_date).to_have_value(end)

    # send reports
    def press_send_report(self):
        self.page.locator('[aria-label="Отправлять отчет"]').click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)

    def choose_where_send_report(self, value: str):
        self.menu.get_by_text(value, exact=True).click()
        self.page.wait_for_selector(MODAL_WINDOW, timeout=self.timeout)

    def click_checkbox_in_tag_and_value(self, row_or_column: str, number: str):
        self.page.locator(f'[data-testid="report_{row_or_column}s_{row_or_column}_{number}_tagCheckbox"]').click()

    def click_checkbox_in_tag_list(self, row_or_column: str, number: str):
        self.page.locator(f'[data-testid="report_{row_or_column}s_{row_or_column}_{number}_tagListCheckbox"]').click()

    def choose_grouping_without_parameters(self, row_or_column: str,  number: str, select: str):
        """Works if you want to choose grouping without other parameters"""
        self.page.locator(f'[data-testid="report_{row_or_column}s_{row_or_column}_{number}_select"]').click()
        self.menu.get_by_text(select, exact=True).click()

    def choose_tag_and_value(self, row_or_column: str, number: str, select: str, tag_name: str, tag_value: str):
        self.page.locator(f'[data-testid="report_{row_or_column}s_{row_or_column}_{number}_select"]').click()
        self.menu.get_by_text(select, exact=True).click()
        self.page.wait_for_timeout(500)
        self.page.locator(f'[data-testid="report_{row_or_column}s_{row_or_column}_{number}_tagSelect"]').click()
        self.page.wait_for_timeout(500)
        self.menu.get_by_text(tag_name, exact=True).click()
        self.page.wait_for_timeout(500)
        self.page.locator(f'[data-testid="report_{row_or_column}s_{row_or_column}_{number}_tagValues"]').click()
        self.page.wait_for_timeout(500)
        self.page.locator('[class*="EnhancedSelect_selectOptions"]').get_by_text(tag_value, exact=True).click()
        self.page.wait_for_timeout(1000)
        self.page.locator('[class*="subtitle1 styles_searchTitleLeftText"]').click()

    def choose_tag_list(self, row_or_column, number: str, *args):
        self.page.locator(f'[data-testid="report_{row_or_column}s_{row_or_column}_{number}_select"]').click()
        self.menu.get_by_text("По списку тегов", exact=True).click()
        self.page.locator(f'[data-testid="report_{row_or_column}s_{row_or_column}_{number}__tagListValues"]').click()
        for i in args:
            self.page.locator('[class*="EnhancedSelect_selectOptions"]').get_by_text(i, exact=True).click()
        self.page.locator('[class*="subtitle1 styles_searchTitleLeftText"]').click()

    def choose_row_by_date(self, number: str, select: str, time: str):
        """Choose row by date. Columns don't have"""
        self.page.locator(f'[data-testid="report_rows_row_{number}_select"]').click()
        self.menu.get_by_text(select, exact=True).click()
        self.page.locator(f'[data-testid="report_rows_row_{number}_time"]').click()
        self.menu.get_by_text(time, exact=True).click()

    def add_checklist_to_report(self, check_list_name):
        self.page.locator(BUTTON_CHANGE_FILTERS).click()
        self.page.locator('[id="Фильтровать по числовым тегам"]').click()
        self.page.mouse.wheel(delta_x=0, delta_y=10000)
        self.page.get_by_text("По чек-листам").nth(1).click()
        self.page.locator(".styles_questionTitle__WSOwz").click()
        self.page.locator('[autocorrect=off]').nth(0).type("автотест", delay=10)
        self.page.wait_for_timeout(500)
        self.page.get_by_text(check_list_name, exact=True).first.click()
        self.page.locator('[class*="subtitle1 styles_searchTitleLeftText"]').click()

    def fill_column_by_exact_filter(self, number: str, column_name: str, tag_name: str, tag_value: str):
        self.page.locator(f'[data-testid="report_columns_column_{number}_select"]').click()
        self.menu.get_by_text("Точный фильтр", exact=True).click()
        self.page.locator(f'[data-testid="report_columns_column_{number}_searchInput"]').locator('[type="text"]').type(
            column_name, delay=10)
        self.page.locator(f'[data-testid="report_columns_column_{number}_searchFilters"]').click()
        self.page.wait_for_timeout(500)
        self.menu.get_by_text(tag_name, exact=True).click()
        self.page.locator('[class*="subtitle1 styles_searchTitleLeftText"]').click()
        self.page.locator('[data-testid="report_columns"]').get_by_text("Все", exact=True).click()
        self.menu.get_by_text(tag_value, exact=True).click()
        self.page.locator('[class*="subtitle1 styles_searchTitleLeftText"]').click()


    # additional params
    def click_apply_in_additional_params(self):
        self.button_add_params_apply.click()
        self.page.wait_for_selector(MODAL_WINDOW, state="hidden", timeout=self.timeout)

    def click_gear_in_rows(self):
        self.button_gear_in_row.click()
        self.page.wait_for_selector(MODAL_WINDOW, timeout=self.timeout)

    def click_gear_in_columns(self, column_number: str):
        self.page.locator(f'[data-testid="report_columns_column_{column_number}_settings_btn"]').click()
        self.page.wait_for_selector(MODAL_WINDOW, timeout=self.timeout)

    def type_value_to_select(self, value: str):
        self.select_with_additional_param.click(force=True)
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        self.page.wait_for_timeout(500)
        self.menu.get_by_text(value, exact=True).click()

    def delete_select(self):
        self.modal_window.locator(BUTTON_KORZINA_IN_ADD_PARAMS).click()
        self.page.wait_for_selector(SELECT_WITH_ADDITIONAL_PARAM, state="hidden")

    def click_add_param_tag_value(self):
        self.page.locator(BUTTON_TAG_VALUE_IN_ADDITIONAL_PARAMS).click()
        self.page.wait_for_selector(SELECT_WITH_ADDITIONAL_PARAM, timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def click_add_param_avg_number_tag_value(self):
        self.page.locator(BUTTON_AVERAGE_NUMBER_TAG_VALUE).click()
        self.page.wait_for_selector(SELECT_WITH_ADDITIONAL_PARAM, timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def click_add_param_sum_number_tag_value(self):
        self.page.locator(BUTTON_SUM_NUMBER_TAG_VALUE).click()
        self.page.wait_for_selector(SELECT_WITH_ADDITIONAL_PARAM, timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def click_add_param_checklist_point(self):
        self.page.locator(BUTTON_CHECKLIST_POINT_IN_ADDITIONAL_PARAMS).click()
        self.page.wait_for_selector(SELECT_WITH_ADDITIONAL_PARAM, timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def click_add_param_checklist_point_percent(self):
        self.page.locator(BUTTON_CHECKLIST_POINT_PERCENT_IN_ADDITIONAL_PARAMS).click()
        self.page.wait_for_selector(SELECT_WITH_ADDITIONAL_PARAM, timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def click_add_param_checklist_question_point(self):
        self.page.locator(BUTTON_CHECKLIST_QUESTION_POINT_IN_ADDITIONAL_PARAMS).click()
        self.page.wait_for_selector(SELECT_WITH_ADDITIONAL_PARAM, timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def click_add_param_checklist_question_point_percent(self):
        self.page.locator(BUTTON_CHECKLIST_QUESTION_POINT_PERCENT_IN_ADDITIONAL_PARAMS).click()
        self.page.wait_for_selector(SELECT_WITH_ADDITIONAL_PARAM, timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def click_add_param_checklist_frequent_answer_for_question(self):
        self.page.locator(BUTTON_CHECKLIST_FREQUENT_ANSWER_FOR_QUESTION_IN_ADDITIONAL_PARAMS).click()
        self.page.wait_for_selector(SELECT_WITH_ADDITIONAL_PARAM, timeout=self.timeout)
        self.page.wait_for_timeout(500)

    def click_add_param_comment(self):
        self.page.locator(BUTTON_COMMENT_IN_ADDITIONAL_PARAMS).click()
        self.page.wait_for_selector(SELECT_WITH_ADDITIONAL_PARAM, timeout=self.timeout)
        self.page.wait_for_timeout(500)



def press_save_current(page="page: Page"):
    page.locator(BUTTON_REPORT_UPDATE).click()
    page.wait_for_selector('[class="modal-btns"]')




