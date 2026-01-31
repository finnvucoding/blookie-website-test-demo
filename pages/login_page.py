from playwright.sync_api import Page
from core.base_page import BasePage
from pages.locators.login_locators import LOGIN_PAGE
from core.logger import log
from config.settings import settings

logger = log()

class LoginPage(BasePage):
    """Login page interactions."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = settings.urls.full_login_url
    
    def open(self):
        """Navigate to login page."""
        super().open(self.url)
        logger.info("📄 Opened Login Page")
        self.wait_for_visible(LOGIN_PAGE.EMAIL_INPUT, "Email input field")
    
    # ==================== ACTIONS ====================
    
    def fill_email(self, email: str):
        """Fill email/username input."""
        input_field = self.page.locator(LOGIN_PAGE.EMAIL_INPUT).first
        self.click(input_field, "Email input field")
        self.fill(input_field, email, "Email input field")
        self.page.wait_for_timeout(settings.timeouts.SHORT)
    
    def fill_password(self, password: str):
        """Fill password input."""
        input_field = self.page.locator(LOGIN_PAGE.PASSWORD_INPUT)
        self.click(input_field, "Password input field")
        self.fill(input_field, password, "Password input field")
        self.page.wait_for_timeout(settings.timeouts.SHORT)

    def click_login_button(self, wait_for_result: bool = True):
        self.click(self.page.locator(LOGIN_PAGE.LOGIN_BUTTON), "Login button")
        if wait_for_result:
            self.page.wait_for_timeout(1000)
    
    def login(self, email: str, password: str):
        logger.info(f"🔐 Attempting to login as: {email}")
        self.fill_email(email)
        self.fill_password(password)
        self.click_login_button()
    
    def click_register_link(self):
        self.click(self.page.locator(LOGIN_PAGE.REGISTER_LINK), "Register link")
        self.page.wait_for_timeout(settings.timeouts.SHORT)
    
    # ==================== VERIFICATIONS ====================
    
    def is_error_visible(self, timeout: int = 5000) -> bool:
        """Check if login error toast is displayed.
        
        Args:
            timeout: Max time to wait for error toast (ms)
        """
        try:
            error_msg = self.page.locator(LOGIN_PAGE.ERROR_MESSAGE)
            error_msg.first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False
    
    def get_error_message(self) -> str:
        """Get error message text from toast."""
        error_msg = self.page.locator(LOGIN_PAGE.ERROR_MESSAGE)
        if error_msg.count() > 0:
            return error_msg.first.text_content().strip()
        return ""
    
    
    def is_logged_in(self) -> bool:
        """
        Check if user is currently logged in.
        nếu có biểu tượng chuông là đã login.
        """
        bell_icon = self.page.locator(LOGIN_PAGE.BELL_ICON)
        return bell_icon.first.is_visible()
    
    def wait_for_redirect_after_login(self, timeout: int = 10000) -> bool:
        """
        Returns True if login was successful (redirected away from login page).
        Uses Smart Wait instead of time.sleep - Rule #1 compliance.
        
        Args:
            timeout: Max wait time in milliseconds
            
        Returns:
            bool: True if redirected (login successful), False otherwise
        """
        try:
            # Wait for URL to NOT contain /login anymore
            self.page.wait_for_url(
                lambda url: "/login" not in url.lower(),
                timeout=timeout
            )
            logger.info("✅ Login successful - redirected away from login page")
            return True
        except Exception:
            logger.warning("⚠️ Still on login page after timeout")
            return False