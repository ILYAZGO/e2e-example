from playwright.sync_api import Page, expect
from pages.base_class import *

BUTTON_IMOT_IO = '[alt="Imot.io"]'


class Links(BaseClass):
    def __init__(self, page: Page):
        super().__init__(page)
        self.imot_io = page.locator(BUTTON_IMOT_IO)

    def assert_url(self, link):
        self.page.wait_for_selector('[alt="Imot.io loader"]', state="hidden")
        expect(self.page).to_have_url(link)

    def click_imot_io(self):
        self.imot_io.click()
        self.page.wait_for_selector("[id='username']")
        self.page.wait_for_timeout(1000)