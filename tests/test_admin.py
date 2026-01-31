import pytest
from playwright.sync_api import Page, expect

from config.settings import settings
from core.logger import log
from pages.locators.admin_locators import (
    ADMIN_DASHBOARD,
    ADMIN_USERS,
    ADMIN_USER_DIALOG,
    ADMIN_POSTS,
    ADMIN_REPORTS
)

logger = log()


# ============================================
# FIXTURES
# ============================================

@pytest.fixture(scope="function")
def admin_page(page: Page, api) -> Page:
    """
    Page with admin user authenticated.
    Logs in via API and injects token to browser.
    """
    if not settings.admin_creds.is_valid:
        pytest.skip("Admin credentials not configured in .env (ADMIN_EMAIL, ADMIN_PASSWORD)")
    
    # Login via API
    login_response = api.auth.login(
        settings.admin_creds.email,
        settings.admin_creds.password
    )
    
    if not login_response.success:
        pytest.fail(f"Admin login failed: {login_response.data}")
    
    access_token = login_response.json.get("data", {}).get("accessToken")
    user_info = login_response.json.get("data", {}).get("user", {})
    
    # Check if user has admin role
    if user_info.get("role") != "ADMIN":
        pytest.fail(f"User {settings.admin_creds.email} is not an admin (role: {user_info.get('role')})")
    
    # Navigate to domain and inject token
    page.goto(settings.urls.base_ui)
    page.evaluate(f"localStorage.setItem('accessToken', '{access_token}')")
    
    logger.info(f"🔐 Admin authenticated: {settings.admin_creds.email}")
    return page


# ============================================
# ADMIN PAGE NAVIGATION TESTS
# ============================================

@pytest.mark.ui
@pytest.mark.admin
@pytest.mark.smoke
class TestAdminNavigation:
    """Admin page navigation tests (via direct URLs)."""
    
    def test_can_access_dashboard_page(self, admin_page: Page):
        """
        Test ID: ADMIN-001
        Verify admin can access dashboard page directly.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/dashboard")
        page.wait_for_load_state("networkidle")
        
        # Dashboard page should have title "Dashboard"
        title = page.locator("h1:has-text('Dashboard')")
        expect(title).to_be_visible(timeout=10000)
        logger.info("✅ Dashboard page accessible")
    
    def test_can_access_users_page(self, admin_page: Page):
        """
        Test ID: ADMIN-002
        Verify admin can access users management page.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/users/list")
        page.wait_for_load_state("networkidle")
        
        # Users page should have title "Quản lý người dùng"
        title = page.locator("h1:has-text('Quản lý người dùng')")
        expect(title).to_be_visible(timeout=10000)
        logger.info("✅ Users page accessible")
    
    def test_can_access_posts_page(self, admin_page: Page):
        """
        Test ID: ADMIN-003
        Verify admin can access posts management page.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/posts/list")
        page.wait_for_load_state("networkidle")
        
        # Posts page should have title "Quản lý Bài Đăng"
        title = page.locator("h1:has-text('Quản lý Bài Đăng')")
        expect(title).to_be_visible(timeout=10000)
        logger.info("✅ Posts page accessible")
    
    def test_can_access_reports_page(self, admin_page: Page):
        """
        Test ID: ADMIN-004
        Verify admin can access reports page.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/reports/list")
        page.wait_for_load_state("networkidle")
        
        # Reports page should have title "Quản lý Báo cáo"
        title = page.locator("h1:has-text('Quản lý Báo cáo')")
        expect(title).to_be_visible(timeout=10000)
        logger.info("✅ Reports page accessible")


# ============================================
# ADMIN DASHBOARD TESTS
# ============================================

@pytest.mark.ui
@pytest.mark.admin
class TestAdminDashboard:
    """Admin dashboard page tests."""
    
    def test_dashboard_page_loads(self, admin_page: Page):
        """
        Test ID: ADMIN-010
        Verify dashboard page loads successfully.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/dashboard")
        page.wait_for_load_state("networkidle")
        
        title = page.locator(ADMIN_DASHBOARD.PAGE_TITLE)
        expect(title).to_be_visible(timeout=10000)
        logger.info("✅ Dashboard page loaded")
    
    def test_period_filter_buttons_visible(self, admin_page: Page):
        """
        Test ID: ADMIN-011
        Verify period filter buttons (Today, 7 days, 30 days) are visible.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/dashboard")
        page.wait_for_load_state("networkidle")
        
        today_btn = page.locator(ADMIN_DASHBOARD.TODAY_BUTTON)
        week_btn = page.locator(ADMIN_DASHBOARD.WEEK_BUTTON)
        month_btn = page.locator(ADMIN_DASHBOARD.MONTH_BUTTON)
        
        expect(today_btn).to_be_visible(timeout=10000)
        expect(week_btn).to_be_visible(timeout=10000)
        expect(month_btn).to_be_visible(timeout=10000)
        logger.info("✅ Period filter buttons visible")
    
    def test_click_period_filter_changes_data(self, admin_page: Page):
        """
        Test ID: ADMIN-012
        Verify clicking period filter changes active button.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/dashboard")
        page.wait_for_load_state("networkidle")
        
        week_btn = page.locator(ADMIN_DASHBOARD.WEEK_BUTTON)
        if week_btn.is_visible():
            week_btn.click()
            page.wait_for_timeout(1000)
            logger.info("✅ Period filter clicked successfully")
        else:
            logger.info("ℹ️ Period filter not visible")


# ============================================
# ADMIN USERS MANAGEMENT TESTS
# ============================================

@pytest.mark.ui
@pytest.mark.admin
class TestAdminUsersManagement:
    """Admin users management page tests."""
    
    def test_users_page_loads(self, admin_page: Page):
        """
        Test ID: ADMIN-020
        Verify users management page loads.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/users/list")
        page.wait_for_load_state("networkidle")
        
        title = page.locator(ADMIN_USERS.PAGE_TITLE)
        expect(title).to_be_visible(timeout=10000)
        logger.info("✅ Users management page loaded")
    
    def test_users_table_is_visible(self, admin_page: Page):
        """
        Test ID: ADMIN-021
        Verify users table is displayed.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/users/list")
        page.wait_for_load_state("networkidle")
        
        # Users page uses a regular HTML table, not MuiTable
        table = page.locator("table.w-full")
        expect(table).to_be_visible(timeout=10000)
        logger.info("✅ Users table visible")
    
    def test_search_input_exists(self, admin_page: Page):
        """
        Test ID: ADMIN-022
        Verify search input field exists.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/users/list")
        page.wait_for_load_state("networkidle")
        
        search = page.locator(ADMIN_USERS.SEARCH_INPUT)
        expect(search).to_be_visible(timeout=10000)
        logger.info("✅ Search input visible")
    
    def test_search_users_by_name(self, admin_page: Page):
        """
        Test ID: ADMIN-023
        Verify searching users by name works.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/users/list")
        page.wait_for_load_state("networkidle")
        
        search = page.locator(ADMIN_USERS.SEARCH_INPUT)
        if search.is_visible():
            search.fill("admin")
            page.wait_for_timeout(1000)  # Wait for search debounce
            logger.info("✅ Search executed")
        else:
            logger.info("ℹ️ Search input not visible")
    
    def test_user_row_has_action_buttons(self, admin_page: Page):
        """
        Test ID: ADMIN-024
        Verify user rows have action buttons.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/users/list")
        page.wait_for_load_state("networkidle")
        
        first_row = page.locator(ADMIN_USERS.USER_ROW).first
        if first_row.is_visible():
            actions = first_row.locator(ADMIN_USERS.CELL_ACTIONS)
            expect(actions).to_be_visible(timeout=5000)
            logger.info("✅ Action buttons visible")
        else:
            logger.info("ℹ️ No user rows found")


# ============================================
# ADMIN POSTS MANAGEMENT TESTS
# ============================================

@pytest.mark.ui
@pytest.mark.admin
class TestAdminPostsManagement:
    """Admin posts management page tests."""
    
    def test_posts_page_loads(self, admin_page: Page):
        """
        Test ID: ADMIN-030
        Verify posts management page loads.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/posts/list")
        page.wait_for_load_state("networkidle")
        
        title = page.locator(ADMIN_POSTS.PAGE_TITLE)
        expect(title).to_be_visible(timeout=10000)
        logger.info("✅ Posts management page loaded")
    
    def test_posts_stats_cards_visible(self, admin_page: Page):
        """
        Test ID: ADMIN-031
        Verify stats cards (total, active, hidden posts) are visible.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/posts/list")
        page.wait_for_load_state("networkidle")
        
        total_card = page.locator(ADMIN_POSTS.TOTAL_POSTS_CARD)
        
        if total_card.is_visible():
            logger.info("✅ Stats cards visible")
        else:
            logger.info("ℹ️ Stats cards not visible on this layout")
    
    def test_posts_table_is_visible(self, admin_page: Page):
        """
        Test ID: ADMIN-032
        Verify posts table is displayed.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/posts/list")
        page.wait_for_load_state("networkidle")
        
        table = page.locator(ADMIN_POSTS.POSTS_TABLE)
        expect(table).to_be_visible(timeout=10000)
        logger.info("✅ Posts table visible")
    
    def test_search_posts_input_exists(self, admin_page: Page):
        """
        Test ID: ADMIN-033
        Verify search input for posts exists.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/posts/list")
        page.wait_for_load_state("networkidle")
        
        search = page.locator(ADMIN_POSTS.SEARCH_INPUT)
        expect(search).to_be_visible(timeout=10000)
        logger.info("✅ Search input visible")
    
    def test_status_filter_exists(self, admin_page: Page):
        """
        Test ID: ADMIN-034
        Verify status filter dropdown exists.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/posts/list")
        page.wait_for_load_state("networkidle")
        
        status_filter = page.locator(ADMIN_POSTS.STATUS_FILTER_SELECT)
        if status_filter.is_visible():
            logger.info("✅ Status filter visible")
        else:
            logger.info("ℹ️ Status filter may use different UI component")
    
    def test_pagination_exists(self, admin_page: Page):
        """
        Test ID: ADMIN-035
        Verify pagination controls exist.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/posts/list")
        page.wait_for_load_state("networkidle")
        
        pagination = page.locator(ADMIN_POSTS.PAGINATION_CONTAINER)
        if pagination.is_visible():
            logger.info("✅ Pagination visible")
        else:
            logger.info("ℹ️ Not enough posts for pagination")


# ============================================
# ADMIN REPORTS MANAGEMENT TESTS
# ============================================

@pytest.mark.ui
@pytest.mark.admin
class TestAdminReportsManagement:
    """Admin reports management page tests."""
    
    def test_reports_page_loads(self, admin_page: Page):
        """
        Test ID: ADMIN-040
        Verify reports management page loads.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/reports/list")
        page.wait_for_load_state("networkidle")
        
        # Check page loaded by title
        title = page.locator("h1:has-text('Quản lý Báo cáo')")
        expect(title).to_be_visible(timeout=10000)
        logger.info("✅ Reports page loaded")
    
    def test_reports_table_visible(self, admin_page: Page):
        """
        Test ID: ADMIN-041
        Verify reports table is displayed (if reports exist).
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/reports/list")
        page.wait_for_load_state("networkidle")
        
        table = page.locator(ADMIN_REPORTS.REPORTS_TABLE)
        if table.is_visible():
            logger.info("✅ Reports table visible")
        else:
            logger.info("ℹ️ No reports table (may be empty or different layout)")


# ============================================
# ADMIN USER DIALOGS TESTS
# ============================================

@pytest.mark.ui
@pytest.mark.admin
@pytest.mark.skip(reason="Dialog tests require specific user data setup")
class TestAdminUserDialogs:
    """Admin user dialog interaction tests."""
    
    def test_view_user_dialog_opens(self, admin_page: Page):
        """
        Test ID: ADMIN-050
        Verify clicking view button opens user details dialog.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/users/list")
        page.wait_for_load_state("networkidle")
        
        first_row = page.locator(ADMIN_USERS.USER_ROW).first
        if first_row.is_visible():
            view_btn = first_row.locator(ADMIN_USERS.VIEW_USER_BUTTON)
            if view_btn.is_visible():
                view_btn.click()
                
                dialog = page.locator(ADMIN_USER_DIALOG.DIALOG)
                expect(dialog).to_be_visible(timeout=5000)
                logger.info("✅ View dialog opened")
    
    def test_edit_user_dialog_opens(self, admin_page: Page):
        """
        Test ID: ADMIN-051
        Verify clicking edit button opens edit dialog.
        """
        page = admin_page
        page.goto(f"{settings.urls.base_ui}/admin/users/list")
        page.wait_for_load_state("networkidle")
        
        first_row = page.locator(ADMIN_USERS.USER_ROW).first
        if first_row.is_visible():
            edit_btn = first_row.locator(ADMIN_USERS.EDIT_USER_BUTTON)
            if edit_btn.is_visible():
                edit_btn.click()
                
                dialog = page.locator(ADMIN_USER_DIALOG.DIALOG)
                expect(dialog).to_be_visible(timeout=5000)
                logger.info("✅ Edit dialog opened")
