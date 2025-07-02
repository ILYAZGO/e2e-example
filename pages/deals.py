#from playwright.sync_api import Page, expect
from pages.base_class import *

DEALS_FOUND = '[class*="_dealsHeaderInner_"]'

class Deals(BaseClass):
    def __init__(self, page: Page):
        super().__init__(page)

        self.deals_found = page.locator(DEALS_FOUND)
        self.open_deal_in_new_tab = page.locator('[data-testid="deal-main-share"]')
        self.deal_date = page.locator('[class*="_dealDate_"]')
        self.communications_count = page.locator('[class*="_communicationsCount_"]')
        self.score_percent = page.locator('[class*="_scorePercent_"]')
        self.deal_score = page.locator('[class*="_callScore_"]')
        self.deal_binding_tag = page.locator('[data-testid="deal-main-binding-tag-0"]')


#
        self.deal_header_block = page.locator('[data-testid="deal-main-root"]')
        self.deal_header_block_date = self.deal_header_block.locator('[class*="_dealDate_"]')
        self.deal_header_block_score_percent = self.deal_header_block.locator('[class*="_scorePercent_"]')
        self.deal_header_block_score = self.deal_header_block.locator('[class*="_callScore_"]')
        self.deal_header_block_binding_tag = self.deal_header_block.locator('[data-testid="deal-main-binding-tag-0"]')
#
        self.deal_communication_block = page.locator('[class*="_singleDealBlock_"]')

        self.deal_communication_date = self.deal_communication_block.locator('[class*="_operatorTagsBlockData_"]')
        self.deal_communication_score_percent = self.deal_communication_block.locator('[class*="_scorePercent_"]')
        self.deal_communication_score = self.deal_communication_block.locator('[class*="_callScore_"]')

        self.deal_communication_operator_phone = self.deal_communication_block.locator('[class*="_operatorPhone_"]')
        self.deal_communication_client_phone = self.deal_communication_block.locator('[class*="_clientTagsBlockPhone_"]')
        self.deal_communication_duration = self.deal_communication_block.locator('[class*="_clientTagsBlockDuration_"]')
        self.deal_communication_score = self.deal_communication_block.locator('[class*="_callScore_"]')
        self.deal_communication_deal_tags_block = self.deal_communication_block.locator('[class*="_dealTagsBlock_"]')

        self.deal_checklist = page.locator('[class="CheckListGroup"]')
        self.deal_checklist_name = self.deal_checklist.locator('[class="CheckListGroupLabel"]')



        self.deal_tags_block = page.locator('[class*="_dealTagsBlock_"]')
        self.deal_button_retag = page.locator('[aria-label="Перетегировать"]')

    def download_deal(self):
        self.button_calls_list_download.click()
        self.page.wait_for_selector(MENU)





