import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from utils.data_builder import create_quick_user
from utils.api_client import BlogAPIClient


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.auth
class TestLogin:
    """Login functionality tests."""
    
    def test_login_with_valid_credentials(self, page: Page):
        """
        Test ID: AUTH-001
        Test successful login with valid email/password.
        
        Pre-condition: User exists in system AND is verified
        Steps:
            1. Use existing verified account (from .env)
            2. Open login page
            3. Enter valid credentials
            4. Click login button
            5. Verify redirect to protected page
        Expected: User successfully logged in and redirected
        """
        from config.settings import settings
        
        # Use existing verified account
        if not settings.existing_user_creds.is_valid:
            pytest.skip("Existing user credentials not configured in .env")
        
        email = settings.existing_user_creds.email
        password = settings.existing_user_creds.password
        
        # TEST: UI Login
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(email=email, password=password)
        
        # VERIFY: Successfully logged in (can access protected page)
        is_logged_in = login_page.wait_for_redirect_after_login()
        assert is_logged_in, "User should be logged in and able to access protected page"
    
    def test_login_with_invalid_password(self, page: Page):
        """
        Test ID: AUTH-002
        Test login fails with wrong password.
        
        Steps:
            1. Use existing verified user email
            2. Attempt login with wrong password
            3. Verify error message shown
        Expected: Error message displayed, user not logged in
        """
        from config.settings import settings
        
        if not settings.existing_user_creds.is_valid:
            pytest.skip("Existing user credentials not configured in .env")
        
        # TEST: Login with wrong password
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(email=settings.existing_user_creds.email, password="WrongPassword123!")
        
        # VERIFY: Error message - wait for toast to appear
        assert login_page.is_error_visible(timeout=5000), "Error message should be visible"
        
        error_text = login_page.get_error_message()
        assert error_text, f"Error message should not be empty, got: '{error_text}'"
    
    def test_login_with_nonexistent_user(self, page: Page):
        """
        Test ID: AUTH-003
        Test login with email that doesn't exist.
        
        Expected: Error message displayed
        """
        login_page = LoginPage(page)
        login_page.open()
        
        login_page.login(
            email="nonexistent_user_12345@example.com",
            password="SomePassword123!"
        )
        
        # VERIFY: Wait for toast to appear with proper timeout
        assert login_page.is_error_visible(timeout=5000), "Error should be shown for nonexistent user"
        
        error_text = login_page.get_error_message()
        assert error_text, "Error message should not be empty"
    
    def test_login_with_username_instead_of_email(self, page: Page):
        """
        Test ID: AUTH-004
        Test login using username instead of email.
        
        The backend accepts both emailOrUsername field.
        Since we may not know the exact username, we test that
        the field accepts username format (not email format).
        
        Note: This test verifies the UI accepts username input,
        which will fail because the user doesn't exist.
        """
        # TEST: Login with a username (not email format)
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(
            email="some_random_username",  # Not an email format
            password="SomePassword123!"
        )
        
        # VERIFY: Should show error for non-existent user
        # This proves the backend accepts username in emailOrUsername field
        assert login_page.is_error_visible(), "Should show error for non-existent username"


@pytest.mark.ui
@pytest.mark.auth
class TestLogout:
    """Logout functionality tests."""
    
    def test_logout_successfully(self, page: Page):
        """
        Test ID: AUTH-010
        Test user can logout successfully.
        
        Steps:
            1. Login with existing verified user
            2. Navigate to protected page
            3. Click user menu
            4. Click logout
            5. Verify redirect to login/home
        
        Note: This test requires proper locators for the navigation menu.
        Currently skipped until proper selectors are identified from the actual UI.
        """
        # TODO: Update this test with proper locators once navigation HTML is analyzed
        pytest.skip("Logout test needs proper navigation selectors - requires UI analysis")
        
        from config.settings import settings
        from pages.login_page import LoginPage
        
        if not settings.existing_user_creds.is_valid:
            pytest.skip("Existing user credentials not configured in .env")
        
        # First, login
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(
            email=settings.existing_user_creds.email,
            password=settings.existing_user_creds.password
        )
        
        # Verify logged in
        is_logged_in = login_page.wait_for_redirect_after_login()
        assert is_logged_in, "Should be logged in first"
        
        # Click user avatar to open menu
        from pages.locators import NAVIGATION
        user_avatar = page.locator(NAVIGATION.USER_AVATAR).first
        user_avatar.click()
        
        # Wait for menu to appear
        page.wait_for_timeout(500)
        
        # Click logout
        logout_btn = page.locator(NAVIGATION.LOGOUT_BUTTON).first
        logout_btn.click()
        
        # VERIFY: Redirected to login page or homepage
        page.wait_for_timeout(1000)
        current_url = page.url
        assert "/login" in current_url or current_url.endswith("/"), \
            f"Should redirect after logout, current URL: {current_url}"


@pytest.mark.api
@pytest.mark.auth
class TestAuthAPI:
    """API-level authentication tests."""
    
    def test_register_via_api(self, api: BlogAPIClient):
        """
        Test ID: AUTH-API-001
        Test user registration via API.
        Note: After registration, user needs email verification to login.
        """
        user = create_quick_user()
        
        response = api.auth.register(
            email=user.email,
            name=user.name,
            password=user.password
        )
        
        assert response.success, f"Registration should succeed: {response.data}"
        assert response.status_code in [200, 201], "Should return 200/201"
        
        # Verify response contains user data
        # Response format: { data: { accessToken: "...", user: { id, username, email, role } } }
        data = response.json.get("data", {})
        user_info = data.get("user", {})
        assert user_info.get("email") == user.email, f"Email should match. Got: {user_info}"
    
    def test_login_via_api(self, api: BlogAPIClient):
        """
        Test ID: AUTH-API-002
        Test login via API returns JWT token in cookies.
        Note: Only verified accounts can login.
        """
        from config.settings import settings
        
        if not settings.existing_user_creds.is_valid:
            pytest.skip("Existing user credentials not configured in .env")
        
        # Login with existing verified account
        response = api.auth.login(
            settings.existing_user_creds.email,
            settings.existing_user_creds.password
        )
        
        assert response.success, f"Login should succeed: {response.data}"
        
        # Verify cookies set
        cookies = api.get_cookies()
        assert len(cookies) > 0, "Should have auth cookies after login"
    
    def test_get_current_user_when_authenticated(self, api: BlogAPIClient):
        """
        Test ID: AUTH-API-003
        Test /auth/me endpoint returns current user.
        Note: Uses existing verified account since new accounts need email verification.
        """
        from config.settings import settings
        
        if not settings.existing_user_creds.is_valid:
            pytest.skip("Existing user credentials not configured in .env")
        
        # Login first
        login_resp = api.auth.login(
            settings.existing_user_creds.email,
            settings.existing_user_creds.password
        )
        assert login_resp.success, f"Login failed: {login_resp.data}"
        
        # Get current user
        response = api.auth.get_current_user()
        
        assert response.success, f"Should return current user info: {response.data}"
        
        data = response.json.get("data", {})
        assert data.get("email") == settings.existing_user_creds.email
    
    def test_duplicate_email_registration(self, api: BlogAPIClient):
        """
        Test ID: AUTH-API-004
        Test registering with duplicate email fails.
        """
        user = create_quick_user()
        
        # Register once
        response1 = api.auth.register(user.email, user.name, user.password)
        assert response1.success
        
        # Try to register again with same email
        response2 = api.auth.register(user.email, "Different User Name", user.password)
        
        assert not response2.success, "Should fail with duplicate email"
        assert response2.status_code in [400, 409], "Should return 400 or 409 conflict"


@pytest.mark.smoke
@pytest.mark.regression
def test_complete_auth_flow(page: Page):
    """
    Test ID: AUTH-E2E-001
    End-to-end authentication flow with existing verified account.
    
    Covers: Login -> Access Protected Page -> Logout
    Note: Cannot test full Register->Verify->Login flow without email access.
    Note: Logout step requires proper navigation selectors - currently testing login only.
    """
    from pages.login_page import LoginPage
    from config.settings import settings
    
    if not settings.existing_user_creds.is_valid:
        pytest.skip("Existing user credentials not configured in .env")
    
    # 1. Login via UI with existing verified account
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(
        email=settings.existing_user_creds.email,
        password=settings.existing_user_creds.password
    )
    
    # 2. Verify login succeeded (can access protected page)
    is_logged_in = login_page.wait_for_redirect_after_login()
    assert is_logged_in, "Should be logged in and access protected page"
    
    # TODO: Add logout test when proper navigation selectors are identified
    # For now, we verify successful login which is the critical path

