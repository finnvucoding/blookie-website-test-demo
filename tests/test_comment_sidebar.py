"""
Block Comment Sidebar Tests
============================
Test comment creation on individual blocks via sidebar.

Strategy: Hybrid API + UI
"""

import pytest
from playwright.sync_api import Page
from pages.post_details_page import PostDetailsPage
from utils.api_client import BlogAPIClient
from pages.locators.postdetails_page_locators import (
    POST_DETAILS_CONTENT,
    BLOCK_COMMENT_SIDEBAR
)


# @pytest.mark.skip(reason="UI selectors need to be updated after inspecting actual frontend HTML")
@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.comments
class TestBlockCommentSidebar:
    """Block comment sidebar functionality tests."""
    
    def test_create_comment_sidebar(
        self,
        logged_in_page: Page,
        test_post: dict
    ):
        """
        Test ID: BLOCK-COMMENT-001
        Test adding comment to a specific block via sidebar.
        
        Steps:
        1. Navigate to post details page
        2. Hover over a text block to reveal comment icon
        3. Click block comment icon to open sidebar
        4. Add comment in sidebar
        5. Verify comment appears in sidebar
        """
        page = logged_in_page
        post_page = PostDetailsPage(page)
        
        # Navigate to post
        post_page.open_post(test_post["id"])
        page.wait_for_timeout(2000)
        
        # Find and hover over first text block
        text_block = page.locator(POST_DETAILS_CONTENT.TEXT_BLOCK).first
        assert text_block.is_visible(), "Text block should be visible"
        
        text_block.hover()
        page.wait_for_timeout(500)
        
        # Click block comment button to open sidebar
        comment_button = page.locator(POST_DETAILS_CONTENT.BLOCK_COMMENT_BUTTON).first
        assert comment_button.is_visible(), "Block comment button should appear on hover"
        comment_button.click()
        
        page.wait_for_timeout(1000)
        
        # Verify sidebar is open
        sidebar = page.locator(BLOCK_COMMENT_SIDEBAR.SIDEBAR)
        assert sidebar.is_visible(), "Block comment sidebar should be visible"
        
        # Verify sidebar title
        title = page.locator(BLOCK_COMMENT_SIDEBAR.COMMENTS_TITLE)
        assert title.is_visible(), "Sidebar should have 'Bình luận' title"
        
        # Add comment in sidebar
        comment_text = "This is a block-specific comment!"
        textarea = page.locator(BLOCK_COMMENT_SIDEBAR.COMMENT_TEXTAREA)
        assert textarea.is_visible(), "Comment textarea should be visible"
        
        textarea.fill(comment_text)
        
        # Submit comment
        submit_button = page.locator(BLOCK_COMMENT_SIDEBAR.COMMENT_SUBMIT_BUTTON)
        submit_button.click()
        
        page.wait_for_timeout(2000)
        
        # Check if empty state is gone
        empty_state = page.locator(BLOCK_COMMENT_SIDEBAR.EMPTY_STATE)
        if empty_state.is_visible():
            # If still showing empty state, check the text
            empty_text = page.locator(BLOCK_COMMENT_SIDEBAR.EMPTY_STATE_TEXT)
            assert not empty_text.is_visible(), "Empty state should be hidden after adding comment"
        
        # Verify comment content is visible
        comment_content = page.locator(f"{BLOCK_COMMENT_SIDEBAR.COMMENTS_LIST} >> text='{comment_text}'")
        assert comment_content.is_visible(), "Block comment should appear in sidebar"
    
    def test_sidebar_empty_state(
        self,
        logged_in_page: Page,
        test_post: dict
    ):
        """
        Test ID: BLOCK-COMMENT-002
        Test sidebar shows empty state when no comments exist.
        
        Steps:
        1. Open post with blocks
        2. Click block comment icon on a block without comments
        3. Verify empty state is displayed
        """
        page = logged_in_page
        post_page = PostDetailsPage(page)
        
        post_page.open_post(test_post["id"])
        page.wait_for_timeout(2000)
        
        # Hover and click block comment
        text_block = page.locator(POST_DETAILS_CONTENT.TEXT_BLOCK).first
        text_block.hover()
        page.wait_for_timeout(500)
        
        comment_button = page.locator(POST_DETAILS_CONTENT.BLOCK_COMMENT_BUTTON).first
        comment_button.click()
        page.wait_for_timeout(1000)
        
        # Verify empty state is shown
        empty_state = page.locator(BLOCK_COMMENT_SIDEBAR.EMPTY_STATE)
        assert empty_state.is_visible(), "Empty state should be visible when no comments exist"
        
        empty_text = page.locator(BLOCK_COMMENT_SIDEBAR.EMPTY_STATE_TEXT)
        assert empty_text.is_visible(), "Empty state text should show 'Chưa có bình luận nào'"
    
    def test_multiple_blocks_separate_comments(
        self,
        logged_in_page: Page,
        test_post: dict
    ):
        """
        Test ID: BLOCK-COMMENT-003
        Test that different blocks have separate comment sections.
        
        Steps:
        1. Add comment to first block
        2. Close sidebar
        3. Open second block comment sidebar
        4. Verify it shows empty state (no comments from first block)
        """
        page = logged_in_page
        post_page = PostDetailsPage(page)
        
        post_page.open_post(test_post["id"])
        page.wait_for_timeout(2000)
        
        # Get all text blocks
        text_blocks = page.locator(POST_DETAILS_CONTENT.TEXT_BLOCK)
        block_count = text_blocks.count()
        
        if block_count < 2:
            pytest.skip("Test requires at least 2 text blocks")
        
        # Add comment to first block
        first_block = text_blocks.nth(0)
        first_block.hover()
        page.wait_for_timeout(500)
        
        page.locator(POST_DETAILS_CONTENT.BLOCK_COMMENT_BUTTON).first.click()
        page.wait_for_timeout(1000)
        
        comment_text_1 = "Comment on first block"
        page.locator(BLOCK_COMMENT_SIDEBAR.COMMENT_TEXTAREA).fill(comment_text_1)
        page.locator(BLOCK_COMMENT_SIDEBAR.COMMENT_SUBMIT_BUTTON).click()
        page.wait_for_timeout(2000)
        
        # Close sidebar (click outside or ESC)
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        
        # Open second block comment sidebar
        second_block = text_blocks.nth(1)
        second_block.hover()
        page.wait_for_timeout(500)
        
        # Get the second block's comment button
        page.locator(POST_DETAILS_CONTENT.BLOCK_COMMENT_BUTTON).nth(1).click()
        page.wait_for_timeout(1000)
        
        # Verify second block shows empty state (no comments)
        empty_state = page.locator(BLOCK_COMMENT_SIDEBAR.EMPTY_STATE)
        assert empty_state.is_visible(), "Second block should show empty state"
        
        # Verify first block's comment is NOT visible here
        first_comment = page.locator(f"text='{comment_text_1}'")
        assert not first_comment.is_visible(), "First block's comment should not appear in second block's sidebar"
    
    def test_sidebar_comment_form_validation(
        self,
        logged_in_page: Page,
        test_post: dict
    ):
        """
        Test ID: BLOCK-COMMENT-004
        Test sidebar comment form validation (empty comment).
        
        Steps:
        1. Open block comment sidebar
        2. Try to submit empty comment
        3. Verify validation or button state
        """
        page = logged_in_page
        post_page = PostDetailsPage(page)
        
        post_page.open_post(test_post["id"])
        page.wait_for_timeout(2000)
        
        # Open sidebar
        text_block = page.locator(POST_DETAILS_CONTENT.TEXT_BLOCK).first
        text_block.hover()
        page.wait_for_timeout(500)
        
        page.locator(POST_DETAILS_CONTENT.BLOCK_COMMENT_BUTTON).first.click()
        page.wait_for_timeout(1000)
        
        # Check submit button state when textarea is empty
        submit_button = page.locator(BLOCK_COMMENT_SIDEBAR.COMMENT_SUBMIT_BUTTON)
        
        # Check if textarea is empty initially
        textarea = page.locator(BLOCK_COMMENT_SIDEBAR.COMMENT_TEXTAREA)
        assert textarea.input_value() == "", "Textarea should be empty initially"
        
        # Verify submit button is disabled when textarea is empty
        assert submit_button.is_disabled(), "Submit button should be disabled when comment is empty"
        
        # Verify empty state is still visible (no comment added)
        empty_state = page.locator(BLOCK_COMMENT_SIDEBAR.EMPTY_STATE)
        assert empty_state.is_visible(), "Empty state should still be visible"


@pytest.mark.regression
@pytest.mark.comments
class TestBlockCommentIntegration:
    """Integration tests for block comments with API setup."""
    
    def test_block_comment_with_api_setup(
        self,
        logged_in_page: Page,
        api_as_user: BlogAPIClient,
        test_post: dict
    ):
        """
        Test ID: BLOCK-COMMENT-INT-001
        Test block comment creation after API-based post setup.
        
        This ensures block comments work on posts created via API.
        """
        page = logged_in_page
        post_page = PostDetailsPage(page)
        
        # Navigate to API-created post
        post_page.open_post(test_post["id"])
        page.wait_for_timeout(2000)
        
        # Verify blocks exist
        text_blocks = page.locator(POST_DETAILS_CONTENT.TEXT_BLOCK)
        assert text_blocks.count() > 0, "Post should have text blocks"
        
        # Open block comment sidebar
        text_blocks.first.hover()
        page.wait_for_timeout(500)
        
        page.locator(POST_DETAILS_CONTENT.BLOCK_COMMENT_BUTTON).first.click()
        page.wait_for_timeout(1000)
        
        # Add comment
        comment_text = "Integration test comment on block"
        page.locator(BLOCK_COMMENT_SIDEBAR.COMMENT_TEXTAREA).fill(comment_text)
        page.locator(BLOCK_COMMENT_SIDEBAR.COMMENT_SUBMIT_BUTTON).click()
        page.wait_for_timeout(2000)
        
        # Verify comment appears
        comment = page.locator(f"{BLOCK_COMMENT_SIDEBAR.COMMENTS_LIST} >> text='{comment_text}'")
        assert comment.is_visible(), "Block comment should be visible in sidebar"
    
    def test_block_comment_persistence(
        self,
        logged_in_page: Page,
        test_post: dict
    ):
        """
        Test ID: BLOCK-COMMENT-INT-002
        Test that block comments persist after closing and reopening sidebar.
        
        Steps:
        1. Add comment to block
        2. Close sidebar
        3. Reopen same block's sidebar
        4. Verify comment is still there
        """
        page = logged_in_page
        post_page = PostDetailsPage(page)
        
        post_page.open_post(test_post["id"])
        page.wait_for_timeout(2000)
        
        # Open sidebar and add comment
        text_block = page.locator(POST_DETAILS_CONTENT.TEXT_BLOCK).first
        text_block.hover()
        page.wait_for_timeout(500)
        
        page.locator(POST_DETAILS_CONTENT.BLOCK_COMMENT_BUTTON).first.click()
        page.wait_for_timeout(1000)
        
        comment_text = "Persistent block comment"
        page.locator(BLOCK_COMMENT_SIDEBAR.COMMENT_TEXTAREA).fill(comment_text)
        page.locator(BLOCK_COMMENT_SIDEBAR.COMMENT_SUBMIT_BUTTON).click()
        page.wait_for_timeout(2000)
        
        # Close sidebar
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        
        # Reopen same block's sidebar
        text_block.hover()
        page.wait_for_timeout(500)
        page.locator(POST_DETAILS_CONTENT.BLOCK_COMMENT_BUTTON).first.click()
        page.wait_for_timeout(1000)
        
        # Verify comment is still visible
        comment = page.locator(f"{BLOCK_COMMENT_SIDEBAR.COMMENTS_LIST} >> text='{comment_text}'")
        assert comment.is_visible(), "Block comment should persist after reopening sidebar"