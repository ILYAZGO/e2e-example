from pages.base_class import *

BLOCK_ADMIN_BAR = '[data-testid="adminBar"]'

class AdminBar(BaseClass):
    def __init__(self, page: Page):
        super().__init__(page)
        self.block_admin_bar = page.locator(BLOCK_ADMIN_BAR)
        self.back_arrow = page.locator(BLOCK_ADMIN_BAR).get_by_role("button")
        self.language = page.locator('[class*="styles_langHandler"]')
        self.languages_menu = page.locator('[role="listbox"]')

    def back_arrow_click(self):
        """Back arrow click"""
        self.back_arrow.click()

    def change_lang(self, current: str, to: str):
        """Change language"""
        self.language.get_by_role("button", name=current).click()
        self.page.wait_for_timeout(500)
        self.languages_menu.get_by_role("option", name=to).click()
        self.page.wait_for_selector('[class*="Hint_question__title"]', timeout=self.timeout)

    def check_user_list_have_text(self, text: str):
        """Check that user list have exact text"""
        self.users_list.click()
        self.page.wait_for_selector(MENU)
        expect(self.menu).to_have_text(text)
        self.users_list.click()

    def check_user_list_contain_text(self, text: str):
        """Check that user list contain text"""
        self.users_list.click()
        self.page.wait_for_selector(MENU, timeout=self.timeout)
        expect(self.menu).to_contain_text(text)
        self.users_list.click()

    def assert_text(self, text: str):
        """Check that user can see text"""
        expect(self.page.get_by_text(text)).to_be_visible(timeout=self.timeout)

    def assert_page_title(self, title:str):
        """Assert page title"""
        self.page.wait_for_timeout(2000)
        expect(self.page).to_have_title(title, timeout=self.timeout)









