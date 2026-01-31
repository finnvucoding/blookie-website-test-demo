import pytest
from typing import Dict, Any, Generator
from playwright.sync_api import Playwright, Browser, BrowserContext, Page, sync_playwright

from config.settings import settings
from core.logger import log
from utils.api_client import BlogAPIClient
from utils.data_builder import create_quick_post

logger = log()


# ============================================
# PYTEST CONFIGURATION HOOKS
# ============================================

def pytest_configure(config):
    """
    Called before test run starts.
    Setup directories, logging, and register custom markers.
    """
    # Register custom markers
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression suite")
    config.addinivalue_line("markers", "api: API-only tests")
    config.addinivalue_line("markers", "ui: UI/Playwright tests")
    config.addinivalue_line("markers", "slow: Tests that take > 30 seconds")
    config.addinivalue_line("markers", "auth: Authentication tests")
    config.addinivalue_line("markers", "posts: Post-related tests")
    config.addinivalue_line("markers", "comments: Comment-related tests")
    config.addinivalue_line("markers", "search: Search functionality tests")
    config.addinivalue_line("markers", "navigation: Navigation tests")
    config.addinivalue_line("markers", "profile: Profile page tests")
    config.addinivalue_line("markers", "newsfeed: Newsfeed/homepage tests")
    config.addinivalue_line("markers", "interactions: User interaction tests")
    config.addinivalue_line("markers", "admin: Admin panel tests")
    
    logger.info("=" * 80)
    logger.info("🚀 BLOG WEBSITE TEST AUTOMATION - STARTING")
    logger.info(f"📍 Environment: {settings.environment.value.upper()}")
    logger.info(f"🌐 Base URL: {settings.urls.base_ui}")
    logger.info(f"🔌 API URL: {settings.urls.base_api}")
    logger.info("=" * 80)
    
    # Create required directories
    (settings.project_root / "logs").mkdir(exist_ok=True)
    (settings.project_root / "screenshots").mkdir(exist_ok=True)
    (settings.project_root / "reports").mkdir(exist_ok=True)
    (settings.project_root / "logs" / "videos").mkdir(exist_ok=True)


def pytest_unconfigure(config):
    """Called after test run completes."""
    logger.info("=" * 80)
    logger.info("✅ TEST RUN COMPLETED")
    logger.info("=" * 80)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test failures and take screenshots.
    Also renames video files to match test name.
    Executed after each test phase (setup, call, teardown).
    """
    outcome = yield
    report = outcome.get_result()
    
    # Only capture screenshot on test failure during 'call' phase
    if report.when == "call" and report.failed:
        # Try to get page fixture from test
        page = item.funcargs.get('page')
        if page:
            test_name = item.nodeid.replace("::", "_").replace("/", "_").replace(" ", "_")
            timestamp = settings.get_current_timestamp()
            screenshot_path = f"screenshots/FAILED_{test_name}_{timestamp}.png"
            
            try:
                page.screenshot(path=screenshot_path, full_page=True)
                logger.error(f"📸 Failure screenshot saved: {screenshot_path}")
                
                # Store test name for video renaming later
                item._test_name_for_video = f"FAILED_{test_name}_{timestamp}"
            except Exception as e:
                logger.warning(f"⚠️ Could not capture screenshot: {e}")
    
    # Rename video after test completes (during teardown phase)
    if report.when == "teardown":
        page = item.funcargs.get('page')
        if page and settings.browser.RECORD_VIDEO:
            try:
                video = page.video
                if video:
                    # Get original video path
                    original_path = video.path()
                    
                    # Create new video name based on test name
                    test_name = item.nodeid.replace("::", "_").replace("/", "_").replace(" ", "_")
                    timestamp = settings.get_current_timestamp()
                    
                    # Use FAILED prefix if test failed
                    prefix = getattr(item, '_test_name_for_video', None)
                    if prefix:
                        new_video_name = f"{prefix}.webm"
                    else:
                        new_video_name = f"{test_name}_{timestamp}.webm"
                    
                    new_path = settings.project_root / "logs" / "videos" / new_video_name
                    
                    # Rename video file
                    import os
                    if os.path.exists(original_path):
                        os.rename(original_path, new_path)
                        logger.info(f"🎬 Video saved: {new_path}")
            except Exception as e:
                logger.debug(f"⚠️ Could not rename video: {e}")


# ============================================
# BROWSER & PAGE FIXTURES
# ============================================

@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """
    Session-scoped Playwright instance.
    Starts Playwright once for entire test session.
    """
    logger.info("🎭 Starting Playwright...")
    with sync_playwright() as playwright:
        yield playwright
    logger.info("🎭 Playwright stopped")


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """
    Session-scoped browser instance.
    Launches browser once and reuses across tests.
    
    For parallel execution, change scope to 'function'.
    """
    logger.info(f"🌐 Launching browser (Headless={settings.browser.HEADLESS})...")
    
    browser = playwright_instance.chromium.launch(
        headless=settings.browser.HEADLESS,
        slow_mo=settings.browser.SLOW_MO
    )
    
    logger.info("✅ Browser launched successfully")
    yield browser
    
    logger.info("🌐 Closing browser...")
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Function-scoped browser context.
    Creates isolated context for each test (fresh cookies, storage).
    """
    from core.browser_factory import BrowserFactory
    
    context = BrowserFactory.create_context(browser)
    logger.debug("🪟 Created new browser context")
    
    yield context
    
    # Cleanup
    context.close()
    logger.debug("🪟 Closed browser context")


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Function-scoped page.
    Creates new page for each test.
    """
    page = context.new_page()
    logger.debug("📄 Created new page")
    
    yield page
    
    # Take screenshot before closing if needed
    page.close()
    logger.debug("📄 Closed page")


# ============================================
# API FIXTURES
# ============================================

@pytest.fixture(scope="session")
def api() -> Generator[BlogAPIClient, None, None]:
    """
    Session-scoped API client.
    Reuses HTTP session across tests.
    
    Note: For tests requiring different users, use `api_as_user` fixture.
    """
    logger.info("🔌 Initializing API client...")
    client = BlogAPIClient()
    
    yield client
    
    # Cleanup
    client.clear_session()
    logger.info("🔌 API client cleaned up")


@pytest.fixture(scope="function")
def api_as_user(api: BlogAPIClient) -> Generator[BlogAPIClient, None, None]:
    """
    Function-scoped API client with logged-in user.
    Uses existing verified account (backend requires email verification).
    """
    # Get existing verified account credentials
    creds = settings.existing_user_creds
    
    if not creds.email or not creds.password:
        pytest.skip("No existing verified user credentials configured in settings")
    
    # Login with existing verified account
    login_response = api.auth.login(creds.email, creds.password)
    
    if not login_response.success:
        pytest.fail(f"Failed to login with existing account: {login_response.data}")
    
    user_data = login_response.json.get("data", {}).get("user", {})
    user_id = user_data.get("id")
    username = user_data.get("username", "Test User")
    
    logger.info(f"👤 Logged in with existing account: {creds.email} (ID: {user_id})")
    
    # Attach user info to API client for convenience
    api._test_user = {
        "email": creds.email,
        "name": username,
        "password": creds.password,
        "id": user_id
    }
    
    yield api
    
    # Cleanup: Logout
    api.auth.logout()
    api.clear_session()
    logger.info(f"🧹 User logged out: {creds.email}")


# ============================================
# AUTHENTICATION FIXTURES
# ============================================

@pytest.fixture(scope="function")
def auth_user(page: Page, api: BlogAPIClient) -> Dict[str, Any]:
    """
    Provides authenticated user in both UI and API.
    
    Uses existing verified account to login via API, then injects token.
    NOTE: Backend requires email verification before login, so we must use
    an existing verified account instead of creating a new one.
    
    Returns:
        Dict with user info: {email, name, password, id, cookies}
    """
    # Use existing verified account (configured in .env)
    if not settings.existing_user_creds.is_valid:
        pytest.skip("Existing user credentials not configured in .env - required for auth")
    
    email = settings.existing_user_creds.email
    password = settings.existing_user_creds.password
    
    # Login via API
    login_response = api.auth.login(email, password)
    assert login_response.success, f"Login failed: {login_response.data}"
    
    user_info = login_response.json.get("data", {}).get("user", {})
    user_id = user_info.get("id")
    user_name = user_info.get("username")
    
    # The auth token is already set in api.session headers by login()
    # We need to also set it in the browser for UI tests
    access_token = login_response.json.get("data", {}).get("accessToken")
    
    # Navigate to domain first
    page.goto(settings.urls.base_ui)
    
    # Store token in localStorage (common pattern for SPAs)
    page.evaluate(f"""
        localStorage.setItem('accessToken', '{access_token}');
    """)
    
    logger.info(f"🔐 Authenticated user ready: {email} (ID: {user_id})")
    
    return {
        "email": email,
        "name": user_name,
        "password": password,
        "id": user_id,
        "access_token": access_token
    }


@pytest.fixture(scope="function")
def logged_in_page(auth_user: Dict[str, Any], page: Page) -> Page:
    """
    Page with authenticated user session.
    Ready to navigate to any protected page.
    
    Usage:
        def test_create_post(logged_in_page):
            logged_in_page.goto("/create-post")
            # User is already logged in
    """
    logger.info("📄 Page with authenticated session ready")
    return page


# ============================================
# EXISTING USER FIXTURES (Pre-existing Account)
# ============================================

@pytest.fixture(scope="function")
def existing_user_api(api: BlogAPIClient) -> Generator[BlogAPIClient, None, None]:
    """
    API client logged in with EXISTING test account.
    
    Use this when you need to test with an account that has existing data
    (posts, followers, etc.) instead of a fresh account.
    
    Credentials come from .env: EXISTING_USER_EMAIL, EXISTING_USER_PASSWORD
    
    Usage:
        def test_with_existing_data(existing_user_api):
            # Account already has posts, comments, etc.
            response = existing_user_api.posts.get_newsfeed()
    """
    # Get existing user credentials from settings
    if not settings.existing_user_creds.is_valid:
        pytest.skip("Existing user credentials not configured in .env")
    
    # Login with existing account
    login_response = api.auth.login(
        settings.existing_user_creds.email,
        settings.existing_user_creds.password
    )
    
    if not login_response.success:
        pytest.fail(f"Failed to login existing user: {login_response.data}")
    
    user_data = login_response.json.get("data", {}).get("user", {})
    user_id = user_data.get("id")
    username = user_data.get("username")
    
    logger.info(f"👤 Logged in as existing user: {settings.existing_user_creds.email} (ID: {user_id})")
    
    # Attach user info
    api._test_user = {
        "email": settings.existing_user_creds.email,
        "password": settings.existing_user_creds.password,
        "username": username,
        "id": user_id
    }
    
    yield api
    
    # Logout
    api.auth.logout()
    api.clear_session()
    logger.info("🧹 Existing user logged out")


@pytest.fixture(scope="function")
def existing_user_page(page: Page, existing_user_api: BlogAPIClient) -> Page:
    """
    Page with EXISTING user authenticated.
    
    Use when you want to interact via UI with an account that has existing data.
    
    Usage:
        def test_view_my_posts(existing_user_page):
            existing_user_page.goto("/profile")
            # Will see existing posts from this account
    """
    # Extract cookies from API session
    api_cookies = existing_user_api.get_cookies()
    
    # Navigate to domain first
    page.goto(settings.urls.base_ui)
    
    # Inject cookies
    for name, value in api_cookies.items():
        page.context.add_cookies([{
            "name": name,
            "value": value,
            "domain": "localhost",  # Adjust based on environment
            "path": "/"
        }])
    
    logger.info(f"🔐 Existing user page ready: {settings.existing_user_creds.email}")
    return page


# ============================================
# TEST DATA FIXTURES
# ============================================

@pytest.fixture(scope="function")
def test_post(api_as_user: BlogAPIClient) -> Dict[str, Any]:
    """
    Creates a test post via API.
    
    Returns:
        Dict with post data: {id, title, author_id}
    """
    user_id = api_as_user._test_user["id"]
    
    # Create post
    post_data = create_quick_post(author_id=user_id, blocks_count=2)
    
    response = api_as_user.posts.create_post(post_data.to_dict())
    assert response.success, f"Failed to create test post: {response.data}"
    
    post_id = response.json.get("data", {}).get("id")
    logger.info(f"📝 Test post created: ID={post_id}, Title='{post_data.title[:30]}...'")
    
    return {
        "id": post_id,
        "title": post_data.title,
        "author_id": user_id
    }


@pytest.fixture(scope="function")
def test_posts(api_as_user: BlogAPIClient) -> list[Dict[str, Any]]:
    """
    Creates multiple test posts (3 by default).
    
    Returns:
        List of post dicts
    """
    user_id = api_as_user._test_user["id"]
    posts = []
    
    for i in range(3):
        post_data = create_quick_post(author_id=user_id)
        response = api_as_user.posts.create_post(post_data.to_dict())
        
        if response.success:
            post_id = response.json.get("data", {}).get("id")
            posts.append({
                "id": post_id,
                "title": post_data.title,
                "author_id": user_id
            })
    
    logger.info(f"📝 Created {len(posts)} test posts")
    return posts


# ============================================
# UTILITY FIXTURES
# ============================================

@pytest.fixture(scope="session")
def base_url() -> str:
    """Get base UI URL."""
    return settings.urls.base_ui


@pytest.fixture(scope="session")
def api_base_url() -> str:
    """Get base API URL."""
    return settings.urls.base_api


@pytest.fixture(autouse=True, scope="function")
def log_test_info(request):
    """
    Auto-use fixture that logs test start/end.
    Runs before and after each test.
    """
    test_name = request.node.nodeid
    logger.info("─" * 80)
    logger.info(f"🧪 TEST START: {test_name}")
    logger.info("─" * 80)
    
    yield
    
    logger.info("─" * 80)
    logger.info(f"✅ TEST END: {test_name}")
    logger.info("─" * 80)
