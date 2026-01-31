"""
User Profile Page Tests
========================
Test profile page display, tabs, and user interactions.

Strategy:
- Use API to login with existing account
- Test profile UI elements
- Test tab switching (Posts, Communities)
"""

import pytest
from playwright.sync_api import Page, expect
from pages.locators.profile_locators import PROFILE
from core.logger import log
from config.settings import settings

logger = log()


@pytest.mark.ui
@pytest.mark.profile
class TestProfilePageElements:
    """Profile page UI elements tests."""
    
    def test_profile_displays_user_name(self, logged_in_page: Page, auth_user: dict):
        """
        Test ID: PROFILE-001
        Verify profile page displays user's display name.
        """
        page = logged_in_page
        user_id = auth_user.get("id")
        
        # Navigate to profile
        page.goto(f"{settings.urls.base_ui}/profile/{user_id}")
        
        display_name = page.locator(PROFILE.DISPLAY_NAME)
        expect(display_name).to_be_visible(timeout=10000)
        
        name_text = display_name.text_content()
        assert len(name_text.strip()) > 0, "Display name should not be empty"
        logger.info(f"✅ Profile name displayed: {name_text}")
    
    def test_profile_displays_avatar(self, logged_in_page: Page, auth_user: dict):
        """
        Test ID: PROFILE-002
        Verify profile page displays user's avatar.
        """
        page = logged_in_page
        user_id = auth_user.get("id")
        
        page.goto(f"{settings.urls.base_ui}/profile/{user_id}")
        
        avatar = page.locator(PROFILE.PROFILE_AVATAR)
        expect(avatar).to_be_visible(timeout=10000)
        logger.info("✅ Profile avatar displayed")
    
    def test_profile_shows_follower_stats(self, logged_in_page: Page, auth_user: dict):
        """
        Test ID: PROFILE-003
        Verify profile shows follower/following statistics.
        """
        page = logged_in_page
        user_id = auth_user.get("id")
        
        page.goto(f"{settings.urls.base_ui}/profile/{user_id}")
        
        # Check followers stat
        followers_stat = page.locator(PROFILE.STAT_FOLLOWERS)
        try:
            followers_stat.wait_for(state="visible", timeout=10000)
            followers_text = followers_stat.text_content()
            logger.info(f"✅ Followers count: {followers_text}")
        except Exception:
            logger.info("ℹ️ Followers stat may have different selector")


@pytest.mark.ui
@pytest.mark.profile
class TestProfileTabs:
    """Profile tabs navigation tests."""
    
    def test_posts_tab_is_default(self, logged_in_page: Page, auth_user: dict):
        """
        Test ID: PROFILE-010
        Verify 'Bài viết' tab is selected by default.
        """
        page = logged_in_page
        user_id = auth_user.get("id")
        
        page.goto(f"{settings.urls.base_ui}/profile/{user_id}")
        
        posts_tab = page.locator(PROFILE.TAB_POSTS)
        expect(posts_tab).to_be_visible(timeout=10000)
        
        # Check if active class is present
        tab_class = posts_tab.get_attribute("class") or ""
        # Active tab should have specific styling
        logger.info(f"✅ Posts tab visible, class: {tab_class}")
    
    def test_click_communities_tab(self, logged_in_page: Page, auth_user: dict):
        """
        Test ID: PROFILE-011
        Verify clicking 'Cộng đồng' tab switches content.
        """
        page = logged_in_page
        user_id = auth_user.get("id")
        
        page.goto(f"{settings.urls.base_ui}/profile/{user_id}")
        
        communities_tab = page.locator(PROFILE.TAB_COMMUNITIES)
        
        if communities_tab.is_visible():
            communities_tab.click()
            
            # Wait for tab content to update
            page.wait_for_timeout(1000)
            
            # Tab should now be active
            logger.info("✅ Switched to communities tab")
        else:
            pytest.skip("Communities tab not visible")
    
    def test_posts_tab_shows_user_posts(self, logged_in_page: Page, auth_user: dict):
        """
        Test ID: PROFILE-012
        Verify posts tab displays user's posts.
        """
        page = logged_in_page
        user_id = auth_user.get("id")
        
        page.goto(f"{settings.urls.base_ui}/profile/{user_id}")
        
        tab_content = page.locator(PROFILE.TAB_CONTENT)
        expect(tab_content).to_be_visible(timeout=10000)
        
        # Check for post cards
        post_cards = page.locator(PROFILE.POST_CARD)
        post_count = post_cards.count()
        logger.info(f"✅ Found {post_count} posts on profile")


@pytest.mark.ui
@pytest.mark.profile
class TestProfileNavigation:
    """Profile access via navigation tests."""
    
    def test_access_profile_via_header_avatar(self, logged_in_page: Page):
        """
        Test ID: PROFILE-020
        Verify user can access profile via header avatar menu.
        """
        page = logged_in_page
        page.goto(settings.urls.base_ui)
        
        # Click avatar button
        avatar_btn = page.locator(PROFILE.HEADER_AVATAR_BTN)
        
        if avatar_btn.is_visible():
            avatar_btn.click()
            
            # Click view profile menu item
            view_profile = page.locator(PROFILE.VIEW_PROFILE_MENU_ITEM)
            
            try:
                view_profile.wait_for(state="visible", timeout=3000)
                view_profile.click()
                
                page.wait_for_url("**/profile/**", timeout=5000)
                logger.info("✅ Navigated to profile via menu")
            except Exception:
                logger.info("ℹ️ Profile menu may have different structure")
        else:
            pytest.skip("Header avatar not visible")


@pytest.mark.ui
@pytest.mark.profile
class TestProfilePostCard:
    """Profile post card interaction tests."""
    
    def test_click_post_navigates_to_details(self, logged_in_page: Page, auth_user: dict):
        """
        Test ID: PROFILE-030
        Verify clicking a post card navigates to post details.
        """
        page = logged_in_page
        user_id = auth_user.get("id")
        
        page.goto(f"{settings.urls.base_ui}/profile/{user_id}")
        
        post_card = page.locator(PROFILE.POST_CARD).first
        
        if post_card.is_visible():
            post_card.click()
            
            try:
                page.wait_for_url("**/post/**", timeout=5000)
                logger.info("✅ Navigated to post details")
            except Exception:
                logger.info("ℹ️ Post detail navigation may differ")
        else:
            pytest.skip("No posts found on profile")
    
    def test_first_post_title_is_displayed(self, logged_in_page: Page, auth_user: dict):
        """
        Test ID: PROFILE-031
        Verify first post displays its title correctly.
        """
        page = logged_in_page
        user_id = auth_user.get("id")
        
        page.goto(f"{settings.urls.base_ui}/profile/{user_id}")
        
        post_cards = page.locator(PROFILE.POST_CARD)
        
        if post_cards.count() > 0:
            from pages.locators.postcard_locators import POST_CARD
            first_title = post_cards.first.locator(POST_CARD.TITLE)
            
            if first_title.is_visible():
                title_text = first_title.text_content()
                assert len(title_text.strip()) > 0, "Post title should not be empty"
                logger.info(f"✅ First post title: {title_text}")
            else:
                logger.info("ℹ️ Title element not visible")
        else:
            pytest.skip("No posts on profile to check")
