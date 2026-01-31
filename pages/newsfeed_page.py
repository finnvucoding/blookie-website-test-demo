from typing import List
from playwright.sync_api import Page, Locator
from core.base_page import BasePage
from pages.locators.newsfeed_locators import NEWSFEED
from pages.locators.postcard_locators import POST_CARD
from core.logger import log

logger = log()


class NewsfeedPage(BasePage):
    """Newsfeed/Homepage interactions."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        from config.settings import settings
        self.url = f"{settings.urls.base_ui}/"
    
    def open(self):
        """Navigate to newsfeed."""
        super().open(self.url)
        logger.info("📄 Opened Newsfeed Page")
        self.wait_for_posts_to_load()
    
    # ==================== WAITS ====================
    
    def wait_for_posts_to_load(self, timeout: int = 10000):
        """Wait for at least one post to appear (uses .first to avoid strict mode)."""
        # Use .first because POSTS_CONTAINER matches multiple post items
        first_post = self.page.locator(NEWSFEED.POSTS_CONTAINER).first
        self.wait_for_visible(first_post, "First Post Card", timeout)

    def get_all_post_cards(self) -> List[Locator]:
        """Get all post cards on current page."""
        return self.page.locator(NEWSFEED.POST_CARD).all()
    
    def get_post_count(self) -> int:
        """Get number of visible posts."""
        return self.page.locator(NEWSFEED.POST_CARD).count()
    
    def get_all_post_titles(self) -> List[str]:
        """Extract all post titles from current page."""
        titles = []
        post_cards = self.get_all_post_cards()
        
        for card in post_cards:
            title_elem = card.locator(POST_CARD.TITLE).first
            if title_elem.is_visible():
                titles.append(title_elem.text_content().strip())
        
        logger.info(f"📝 Found {len(titles)} post titles")
        return titles
    
    def get_first_post_card(self) -> Locator:
        """Get first post card."""
        return self.page.locator(NEWSFEED.POST_CARD).first
    
    # ==================== ACTIONS ====================
    
    def click_create_post_button(self):
        """Click 'Create Post' button."""
        button = self.page.locator(NEWSFEED.CREATE_POST_BUTTON)
        self.click(button, "Create Post Button")
    
    def click_first_post(self):
        """Click on first post to open details."""
        first_post = self.get_first_post_card()
        self.click(first_post.locator(POST_CARD.TITLE), "First Post Card")
    
    def click_filter_all(self):
        """Click 'All' filter."""
        filter_btn = self.page.locator(NEWSFEED.FILTER_ALL)
        self.click(filter_btn, "Filter: All")
    
    def click_filter_following(self):
        """Click 'Following' filter."""
        filter_btn = self.page.locator(NEWSFEED.FILTER_FOLLOWING)
        self.click(filter_btn, "Filter: Following")
    
    def scroll_and_load_more(self):
        """Scroll down to trigger infinite scroll / load more."""
        logger.info("📜 Scrolling to load more posts...")
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(2000)  # Wait for new posts to load
    
    # ==================== POST INTERACTIONS ====================
    
    def upvote_first_post(self):
        """Upvote the first post."""
        first_post = self.get_first_post_card()
        upvote_btn = first_post.locator(POST_CARD.UPVOTE_BUTTON)
        self.click(upvote_btn, "Upvote on First Post")
    
    def comment_on_first_post(self):
        """Click comment button on first post."""
        first_post = self.get_first_post_card()
        comment_btn = first_post.locator(POST_CARD.COMMENT_BUTTON)
        self.click(comment_btn, "Comment Button on First Post")
    
    def save_first_post(self):
        """Save the first post."""
        first_post = self.get_first_post_card()
        save_btn = first_post.locator(POST_CARD.SAVE_BUTTON)
        self.click(save_btn, "Save Button on First Post")
    
    # ==================== VERIFICATIONS ====================
    
    def is_posts_container_visible(self) -> bool:
        """Check if at least one post is visible."""
        # Use .first to avoid strict mode violation with multiple posts
        first_post = self.page.locator(NEWSFEED.POST_CARD).first
        return self.is_visible(first_post)

