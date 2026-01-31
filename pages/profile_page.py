from playwright.sync_api import Page
from core.base_page import BasePage
from pages.locators.profile_locators import PROFILE
from core.logger import log

logger = log()


class ProfilePage(BasePage):
    """User profile page interactions."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        from config.settings import settings
        self.base_url = settings.urls.base_ui
    
    def open_profile(self):
        avatar = self.page.locator(PROFILE.HEADER_AVATAR_BTN).click()
        self.click(avatar.locator(PROFILE.VIEW_PROFILE_MENU_ITEM))

    