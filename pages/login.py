from pages.base_class import *

ALERT_MESSAGE = '[class*="MuiAlert-message"]'

class LoginPage(BaseClass):
    def __init__(self, page: Page):
        super().__init__(page)
        self.alert = page.locator(ALERT_MESSAGE)

    def assert_alert_visible(self, text: str):
        expect(self.alert).to_be_visible()
        expect(self.alert).to_contain_text(text)

    def assert_button_enter_enabled(self):
        self.page.wait_for_timeout(500)
        expect(self.button_enter).to_be_enabled()
