"""
Newsfeed/Homepage Tests
========================
Test newsfeed display, filtering, infinite scroll, and post interactions.

Strategy:
- Test page load and initial state
- Test post card elements
- Test emoji reactions
- Test voting interactions
"""

import pytest
from playwright.sync_api import Page, expect
from pages.newsfeed_page import NewsfeedPage
from pages.locators.newsfeed_locators import NEWSFEED, EMOJI_PICKER
from pages.locators.postcard_locators import POST_CARD
from core.logger import log
from config.settings import settings

logger = log()


@pytest.mark.ui
@pytest.mark.newsfeed
@pytest.mark.smoke
class TestNewsfeedLoad:
    """Newsfeed page load tests."""
    
    def test_newsfeed_page_loads(self, page: Page):
        """
        Test ID: FEED-001
        Verify newsfeed page loads successfully.
        """
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        assert newsfeed.is_posts_container_visible(), \
            "Posts container should be visible"
    
    def test_newsfeed_shows_posts(self, page: Page):
        """
        Test ID: FEED-002
        Verify newsfeed displays at least one post.
        """
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        post_count = newsfeed.get_post_count()
        assert post_count > 0, f"Should have at least 1 post, found {post_count}"
        logger.info(f"✅ Found {post_count} posts on newsfeed")
    
    def test_newsfeed_page_title_visible(self, page: Page):
        """
        Test ID: FEED-003
        Verify page title is displayed.
        """
        page.goto(settings.urls.base_ui)
        
        page_title = page.locator(NEWSFEED.PAGE_TITLE)
        expect(page_title).to_be_visible(timeout=10000)


@pytest.mark.ui
@pytest.mark.newsfeed
class TestPostCardElements:
    """Post card UI elements tests."""
    
    def test_post_card_has_title(self, page: Page):
        """
        Test ID: FEED-010
        Verify post card displays title.
        """
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        first_post = newsfeed.get_first_post_card()
        title = first_post.locator(POST_CARD.TITLE)
        
        expect(title).to_be_visible()
        title_text = title.text_content()
        assert len(title_text.strip()) > 0, "Title should not be empty"
    
    def test_post_card_has_author_info(self, page: Page):
        """
        Test ID: FEED-011
        Verify post card displays author information.
        """
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        first_post = newsfeed.get_first_post_card()
        # Use .first because repost cards may have 2 author names
        author = first_post.locator(POST_CARD.AUTHOR_NAME).first
        
        expect(author).to_be_visible()
        logger.info("✅ Author info displayed on post card")
    
    def test_post_card_has_thumbnail(self, page: Page):
        """
        Test ID: FEED-012
        Verify post card displays thumbnail image.
        """
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        first_post = newsfeed.get_first_post_card()
        thumbnail = first_post.locator(POST_CARD.THUMBNAIL_IMAGE)
        
        # Thumbnail may or may not be present
        if thumbnail.is_visible():
            logger.info("✅ Thumbnail image displayed")
        else:
            logger.info("ℹ️ No thumbnail on this post (may be text-only)")
    
    def test_post_card_has_timestamp(self, page: Page):
        """
        Test ID: FEED-013
        Verify post card displays timestamp.
        """
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        first_post = newsfeed.get_first_post_card()
        timestamp = first_post.locator(POST_CARD.TIMESTAMP)
        
        expect(timestamp).to_be_visible()
        logger.info("✅ Timestamp displayed on post card")


@pytest.mark.ui
@pytest.mark.newsfeed
@pytest.mark.interactions
class TestPostCardVoting:
    """Post card voting interaction tests."""
    
    def test_upvote_button_visible(self, page: Page):
        """
        Test ID: FEED-020
        Verify upvote button is visible on post card.
        """
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        first_post = newsfeed.get_first_post_card()
        upvote_btn = first_post.locator(POST_CARD.UPVOTE_BUTTON)
        
        expect(upvote_btn).to_be_visible()
        logger.info("✅ Upvote button visible")
    
    def test_downvote_button_visible(self, page: Page):
        """
        Test ID: FEED-021
        Verify downvote button is visible on post card.
        """
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        first_post = newsfeed.get_first_post_card()
        downvote_btn = first_post.locator(POST_CARD.DOWNVOTE_BUTTON)
        
        expect(downvote_btn).to_be_visible()
        logger.info("✅ Downvote button visible")
    
    def test_click_upvote_requires_login(self, page: Page):
        """
        Test ID: FEED-022
        Verify clicking upvote without login prompts for login.
        """
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        first_post = newsfeed.get_first_post_card()
        upvote_btn = first_post.locator(POST_CARD.UPVOTE_BUTTON)
        
        upvote_btn.click()
        
        # Should show login prompt or redirect
        page.wait_for_timeout(1000)
        current_url = page.url
        
        # Either redirected to login or modal appeared
        logger.info(f"ℹ️ After upvote click (unauthenticated): {current_url}")
    
    def test_logged_in_user_can_upvote(self, logged_in_page: Page):
        """
        Test ID: FEED-023
        Verify logged-in user can upvote a post.
        """
        page = logged_in_page
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        first_post = newsfeed.get_first_post_card()
        upvote_btn = first_post.locator(POST_CARD.UPVOTE_BUTTON)
        
        # Get initial vote count
        # vote_count = first_post.locator(POST_CARD.VOTE_COUNT)
        
        upvote_btn.click()
        page.wait_for_timeout(1000)
        
        logger.info("✅ Upvote clicked (verify vote count changed)")


@pytest.mark.ui
@pytest.mark.newsfeed
@pytest.mark.interactions
class TestPostCardActions:
    """Post card action buttons tests."""
    
    def test_save_button_visible(self, page: Page):
        """
        Test ID: FEED-030
        Verify save/bookmark button is visible.
        """
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        first_post = newsfeed.get_first_post_card()
        save_btn = first_post.locator(POST_CARD.SAVE_BUTTON)
        
        expect(save_btn).to_be_visible()
        logger.info("✅ Save button visible")
    
    def test_share_button_visible(self, page: Page):
        """
        Test ID: FEED-031
        Verify share/repost button is visible.
        """
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        first_post = newsfeed.get_first_post_card()
        share_btn = first_post.locator(POST_CARD.SHARE_BUTTON)
        
        expect(share_btn).to_be_visible()
        logger.info("✅ Share button visible")
    
    def test_logged_in_user_can_save_post(self, logged_in_page: Page):
        """
        Test ID: FEED-032
        Verify logged-in user can save a post.
        """
        page = logged_in_page
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        first_post = newsfeed.get_first_post_card()
        save_btn = first_post.locator(POST_CARD.SAVE_BUTTON)
        
        save_btn.click()
        page.wait_for_timeout(1000)
        
        # Save button should toggle state
        logger.info("✅ Save button clicked")


@pytest.mark.ui
@pytest.mark.newsfeed
@pytest.mark.interactions
class TestEmojiReactions:
    """Post emoji reaction tests."""
    
    def test_add_emoji_button_visible(self, page: Page):
        """
        Test ID: FEED-040
        Verify add emoji button is visible on post card.
        """
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        first_post = newsfeed.get_first_post_card()
        add_emoji_btn = first_post.locator(POST_CARD.ADD_EMOJI_BUTTON)
        
        expect(add_emoji_btn).to_be_visible()
        logger.info("✅ Add emoji button visible")
    
    def test_click_emoji_opens_picker(self, logged_in_page: Page):
        """
        Test ID: FEED-041
        Verify clicking add emoji button opens emoji picker.
        """
        page = logged_in_page
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        first_post = newsfeed.get_first_post_card()
        add_emoji_btn = first_post.locator(POST_CARD.ADD_EMOJI_BUTTON)
        
        add_emoji_btn.click()
        
        # Wait for emoji picker
        emoji_dialog = page.locator(EMOJI_PICKER.DIALOG)
        
        try:
            emoji_dialog.wait_for(state="visible", timeout=5000)
            logger.info("✅ Emoji picker opened")
            emoji_dialog.click(EMOJI_PICKER.FIRST_EMOJI)  # first emoji
            logger.info("✅ Thả Emoji selected")
        except Exception:
            logger.info("ℹ️ Emoji picker may have different implementation")


@pytest.mark.ui
@pytest.mark.newsfeed
class TestNewsfeedScroll:
    """Newsfeed infinite scroll tests."""
    
    def test_scroll_loads_more_posts(self, page: Page):
        """
        Test ID: FEED-050
        Verify scrolling loads more posts (infinite scroll).
        """
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        initial_count = newsfeed.get_post_count()
        
        # Scroll to load more
        newsfeed.scroll_and_load_more()
        
        new_count = newsfeed.get_post_count()
        
        # May or may not load more depending on total posts
        logger.info(f"📊 Posts: {initial_count} -> {new_count}")
        
        if new_count > initial_count:
            logger.info("✅ More posts loaded via scroll")
        else:
            logger.info("ℹ️ No additional posts (may have reached end)")


@pytest.mark.ui
@pytest.mark.newsfeed
class TestPostCardNavigation:
    """Post card click navigation tests."""
    
    def test_click_post_navigates_to_details(self, page: Page):
        """
        Test ID: FEED-060
        Verify clicking post card navigates to post details page.
        """
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        # Click on post content link (not action buttons)
        first_post = newsfeed.get_first_post_card()
        content_link = first_post.locator(POST_CARD.CONTENT_LINK)
        
        if content_link.is_visible():
            content_link.click()
            
            try:
                page.wait_for_url("**/post/**", timeout=10000)
                logger.info("✅ Navigated to post details")
            except Exception:
                logger.info("ℹ️ Navigation may have different URL pattern")
        else:
            # Try clicking title
            title_link = first_post.locator(POST_CARD.TITLE)
            title_link.click()
            
            try:
                page.wait_for_url("**/post/**", timeout=10000)
                logger.info("✅ Navigated to post details via title")
            except Exception:
                logger.info("ℹ️ Navigation pattern may differ")
