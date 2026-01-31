from typing import List
from playwright.sync_api import Page
from core.base_page import BasePage
from pages.locators.postdetails_page_locators import POST_DETAILS
from pages.locators.postcard_locators import POST_CARD
from core.logger import log

logger = log()


class PostDetailsPage(BasePage):
    """Post detail page interactions."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        from config.settings import settings
        self.base_url = settings.urls.base_ui
    
    def open_post(self, post_id: int):
        """Navigate to specific post detail page."""
        url = f"{self.base_url}/post/{post_id}"
        super().open(url)
        logger.info(f"📄 Opened Post Details: ID={post_id}")
        self.wait_for_post_content()
    
    # ==================== WAITS ====================
    
    def wait_for_post_content(self, timeout: int = 10000):
        """Wait for post content to load."""
        post_container = self.page.locator(POST_DETAILS.POST_CONTAINER)
        self.wait_for_visible(post_container, "Post Container", timeout)
    
    def wait_for_comments_section(self, timeout: int = 5000):
        """Wait for comments section."""
        comments = self.page.locator(POST_DETAILS.COMMENTS_SECTION)
        self.wait_for_visible(comments, "Comments Section", timeout)
    
    # ==================== GETTERS ====================
    
    def get_post_title(self) -> str:
        """Get post title."""
        title_elem = self.page.locator(POST_DETAILS.POST_TITLE)
        return self.get_text(title_elem, "Post Title")
    
    def get_post_content(self) -> str:
        """Get post content (all blocks concatenated)."""
        content_elem = self.page.locator(POST_DETAILS.POST_CONTENT)
        return self.get_text(content_elem, "Post Content")
    
    def get_author_name(self) -> str:
        """Get post author name."""
        author_elem = self.page.locator(POST_DETAILS.AUTHOR_SECTION)
        return self.get_text(author_elem, "Author Name")
    
    def get_comment_count(self) -> int:
        """Get number of comments."""
        return self.page.locator(POST_DETAILS.COMMENT_ITEM).count()
    
    def get_all_comments_text(self) -> List[str]:
        """Get all comment texts."""
        comments = []
        comment_elements = self.page.locator(POST_DETAILS.COMMENT_ITEM).all()
        
        for comment in comment_elements:
            content = comment.locator(POST_DETAILS.COMMENT_CONTENT).first
            if content.is_visible():
                comments.append(content.text_content().strip())
        
        logger.info(f"💬 Found {len(comments)} comments")
        return comments
    
    # ==================== POST ACTIONS ====================
    
    def upvote_post(self):
        """Upvote the post."""
        upvote_btn = self.page.locator(POST_CARD.UPVOTE_BUTTON)
        self.click(upvote_btn, "Upvote Button")
    
    def downvote_post(self):
        """Downvote the post."""
        downvote_btn = self.page.locator(POST_CARD.DOWNVOTE_BUTTON)
        self.click(downvote_btn, "Downvote Button")
    
    def click_repost(self):
        """Click repost/share button."""
        repost_btn = self.page.locator(POST_CARD.SHARE_BUTTON)
        self.click(repost_btn, "Repost/Share Button")
    
    def click_share(self):
        """Click share button."""
        share_btn = self.page.locator(POST_CARD.SHARE_BUTTON)
        self.click(share_btn, "Share Button")
    
    def save_post(self):
        """Click save post button."""
        save_btn = self.page.locator(POST_CARD.SAVE_BUTTON)
        self.click(save_btn, "Save Button")
    
    def open_more_options(self):
        """Open post more options menu."""
        more_btn = self.page.locator(POST_CARD.MORE_OPTIONS)
        self.click(more_btn, "More Options")
    
    def click_edit_post(self):
        """Click edit post option (from more menu)."""
        self.open_more_options()
        edit_btn = self.page.locator(POST_CARD.EDIT_OPTION)
        self.click(edit_btn, "Edit Post")
    
    def click_delete_post(self):
        """Click delete post option."""
        self.open_more_options()
        delete_btn = self.page.locator(POST_CARD.DELETE_OPTION)
        self.click(delete_btn, "Delete Post")
    
    # ==================== COMMENT ACTIONS ====================
    
    def add_comment(self, comment_text: str):
        """
        Add a comment to the post.
        
        Args:
            comment_text: Comment content
        """
        logger.info(f"💬 Adding comment: {comment_text[:50]}...")
        
        # Fill comment input
        comment_input = self.page.locator(POST_DETAILS.COMMENT_INPUT)
        self.fill(comment_input, comment_text, "Comment Input")
        
        # Submit comment
        submit_btn = self.page.locator(POST_DETAILS.SUBMIT_COMMENT_BUTTON)
        self.click(submit_btn, "Submit Comment Button")
        
        # Wait for comment to appear
        self.page.wait_for_timeout(1000)
        logger.info("✅ Comment submitted")
    
    def reply_to_first_comment(self, reply_text: str):
        """Reply to the first comment."""
        logger.info(f"↩️ Replying to first comment: {reply_text[:50]}...")
        
        # Click reply button on first comment
        first_comment = self.page.locator(POST_DETAILS.COMMENT_ITEM).first
        reply_btn = first_comment.locator(POST_DETAILS.COMMENT_REPLY_BUTTON)
        self.click(reply_btn, "Reply Button")
        
        # Wait for reply form to appear
        self.page.wait_for_timeout(500)
        
        # Fill reply input (within the comment context)
        reply_input = first_comment.locator(POST_DETAILS.REPLY_INPUT)
        self.fill(reply_input, reply_text, "Reply Input")
        
        # Submit using the reply submit button within the comment
        submit_btn = first_comment.locator(POST_DETAILS.REPLY_SUBMIT)
        self.click(submit_btn, "Submit Reply")
        
        self.page.wait_for_timeout(1000)
        logger.info("✅ Reply submitted")
    
    def delete_first_comment(self):
        """Delete the first comment (must be owner)."""
        first_comment = self.page.locator(POST_DETAILS.COMMENT_ITEM).first
        delete_btn = first_comment.locator(POST_DETAILS.COMMENT_DELETE_BUTTON)
        self.click(delete_btn, "Delete Comment Button")
        
        # Confirm deletion if there's a confirmation dialog
        # (Add confirmation handling if needed)
        logger.info("🗑️ Comment deleted")
    
    # ==================== VERIFICATIONS ====================
    
    def is_post_visible(self) -> bool:
        """Check if post container is visible."""
        container = self.page.locator(POST_DETAILS.POST_CONTAINER)
        return self.is_visible(container)
    
    def is_comments_section_visible(self) -> bool:
        """Check if comments section is visible."""
        section = self.page.locator(POST_DETAILS.COMMENTS_SECTION)
        return self.is_visible(section)
    
    def is_upvote_active(self) -> bool:
        """Check if upvote button is in active state."""
        upvote_btn = self.page.locator(POST_CARD.UPVOTE_BUTTON)
        # Assuming active state is indicated by a class like 'active' or 'voted'
        return "active" in upvote_btn.get_attribute("class") or "voted" in upvote_btn.get_attribute("class")
