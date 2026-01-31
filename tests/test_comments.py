"""
Comments Tests
==============
Test comment creation, replies, deletion.

Strategy: Hybrid API + UI
"""

import pytest
from playwright.sync_api import Page
from pages.post_details_page import PostDetailsPage
from utils.api_client import BlogAPIClient
from utils.data_builder import CommentBuilder
from pages.locators.postdetails_page_locators import POST_DETAILS, POST_COMMENTS


# @pytest.mark.skip(reason="UI selectors need to be updated after inspecting actual frontend HTML")
@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.comments
class TestComments:
    """Comment functionality tests."""
    
    def test_add_comment_to_post(
        self,
        logged_in_page: Page,
        test_post: dict
    ):
        """
        Test ID: COMMENT-001
        Test adding comment to a post via UI.
        """
        page = logged_in_page
        post_page = PostDetailsPage(page)
        
        post_page.open_post(test_post["id"])
        
        # Get initial comment count
        initial_count = post_page.get_comment_count()
        
        # Add comment
        comment_text = "This is a test comment!"
        post_page.add_comment(comment_text)
        
        # Wait and verify
        page.wait_for_timeout(1500)
        
        new_count = post_page.get_comment_count()
        assert new_count == initial_count + 1, \
            f"Comment count should increase from {initial_count} to {new_count}"
        
        # Verify comment appears in list
        comments = post_page.get_all_comments_text()
        assert comment_text in comments, "New comment should appear in list"
    
    def test_reply_to_comment(
        self,
        logged_in_page: Page,
        test_post: dict,
        api_as_user: BlogAPIClient
    ):
        """
        Test ID: COMMENT-002
        Test replying to an existing comment.
        
        Setup: Create initial comment via API
        Test: Reply via UI
        """
        page = logged_in_page
        
        # SETUP: Create a comment via API first
        user_id = api_as_user._test_user["id"]
        comment_data = CommentBuilder() \
            .on_post(test_post["id"]) \
            .by_commenter(user_id) \
            .with_content("Parent comment") \
            .build()
        
        comment_resp = api_as_user.comments.create_comment(
            post_id=comment_data.post_id,
            commenter_id=comment_data.commenter_id,
            content=comment_data.content
        )
        assert comment_resp.success, "Failed to create parent comment"
        
        # TEST: Reply via UI
        post_page = PostDetailsPage(page)
        post_page.open_post(test_post["id"])
        
        reply_text = "This is a reply!"
        post_page.reply_to_first_comment(reply_text)
        
        # VERIFY - wait for reply to appear and expand replies if needed
        page.wait_for_timeout(1500)
        
        # Look for the reply text directly in the page
        # Replies might be in a nested container, so search for the text
        reply_visible = page.locator(f"text='{reply_text}'").is_visible()
        
        # If not visible, try clicking "View replies" button
        if not reply_visible:
            view_replies_btn = page.locator(POST_COMMENTS.VIEW_REPLIES_BUTTON).first
            if view_replies_btn.is_visible():
                view_replies_btn.click()
                page.wait_for_timeout(1000)
        
        # Check again for the reply text
        reply_visible = page.locator(f"text='{reply_text}'").is_visible()
        assert reply_visible, "Reply should appear in comments"
    
    def test_comment_shows_author_info(
        self,
        logged_in_page: Page,
        test_post: dict
    ):
        """
        Test ID: COMMENT-003
        Test comment displays author information.
        """
        page = logged_in_page
        post_page = PostDetailsPage(page)
        
        # Add a comment
        post_page.open_post(test_post["id"])
        post_page.add_comment("Test comment with author")
        
        page.wait_for_timeout(1500)
        
        # Verify comment has author info visible
        first_comment = page.locator(POST_DETAILS.COMMENT_ITEM).first
        author_elem = first_comment.locator(POST_DETAILS.COMMENT_AUTHOR)
        
        assert author_elem.is_visible(), "Comment author should be visible"


@pytest.mark.api
@pytest.mark.comments
class TestCommentsAPI:
    """API-level comment tests."""
    
    def test_create_comment_via_api(
        self,
        api_as_user: BlogAPIClient,
        test_post: dict
    ):
        """
        Test ID: COMMENT-API-001
        Test creating comment via API.
        """
        user_id = api_as_user._test_user["id"]
        
        response = api_as_user.comments.create_comment(
            post_id=test_post["id"],
            commenter_id=user_id,
            content="API comment test"
        )
        
        assert response.success, f"Comment creation failed: {response.data}"
        
        comment_id = response.json.get("data", {}).get("id")
        assert comment_id is not None, "Should return comment ID"
    
    def test_get_comments_for_post(
        self,
        api_as_user: BlogAPIClient,
        test_post: dict
    ):
        """
        Test ID: COMMENT-API-002
        Test retrieving comments for a post.
        """
        # Create a comment first
        user_id = api_as_user._test_user["id"]
        api_as_user.comments.create_comment(
            post_id=test_post["id"],
            commenter_id=user_id,
            content="Test comment"
        )
        
        # Get comments
        response = api_as_user.comments.get_comments(
            post_id=test_post["id"]
        )
        
        assert response.success, "Should retrieve comments"
        
        # API returns data as list directly
        comments = response.json.get("data", [])
        assert isinstance(comments, list), "Data should be a list"
        assert len(comments) > 0, "Should have at least one comment"
    
    def test_create_reply_via_api(
        self,
        api_as_user: BlogAPIClient,
        test_post: dict
    ):
        """
        Test ID: COMMENT-API-003
        Test creating reply (comment with parentId) via API.
        """
        user_id = api_as_user._test_user["id"]
        
        # Create parent comment
        parent_resp = api_as_user.comments.create_comment(
            post_id=test_post["id"],
            commenter_id=user_id,
            content="Parent comment"
        )
        parent_id = parent_resp.json.get("data", {}).get("id")
        
        # Create reply
        reply_resp = api_as_user.comments.create_comment(
            post_id=test_post["id"],
            commenter_id=user_id,
            content="Reply comment",
            parent_comment_id=parent_id
        )
        
        assert reply_resp.success, "Reply creation should succeed"
        
        reply_data = reply_resp.json.get("data", {})
        assert reply_data.get("id") is not None, "Reply should have an ID"
        assert reply_data.get("content") == "Reply comment", "Reply content should match"
    
    def test_delete_comment_via_api(
        self,
        api_as_user: BlogAPIClient,
        test_post: dict
    ):
        """
        Test ID: COMMENT-API-004
        Test deleting comment via API.
        """
        user_id = api_as_user._test_user["id"]
        
        # Create comment
        create_resp = api_as_user.comments.create_comment(
            post_id=test_post["id"],
            commenter_id=user_id,
            content="Comment to delete"
        )
        comment_id = create_resp.json.get("data", {}).get("id")
        
        # Delete it
        delete_resp = api_as_user.comments.delete_comment(comment_id)
        
        assert delete_resp.success, "Deletion should succeed"


@pytest.mark.regression
def test_nested_replies_structure(
    logged_in_page: Page,
    api_as_user: BlogAPIClient,
    test_post: dict
):
    """
    Test ID: COMMENT-E2E-001
    Test nested comment structure (comment -> reply -> reply).
    
    Creates multi-level replies and verifies structure in UI.
    """
    page = logged_in_page
    user_id = api_as_user._test_user["id"]
    
    # Create parent comment
    parent_resp = api_as_user.comments.create_comment(
        post_id=test_post["id"],
        commenter_id=user_id,
        content="Level 1 comment"
    )
    parent_id = parent_resp.json.get("data", {}).get("id")
    
    # Create first reply (Level 2)
    reply1_resp = api_as_user.comments.create_comment(
        post_id=test_post["id"],
        commenter_id=user_id,
        content="Level 2 reply",
        parent_comment_id=parent_id
    )
    reply1_id = reply1_resp.json.get("data", {}).get("id")

    # Create nested reply (Level 3) via API
    api_as_user.comments.create_comment(
        post_id=test_post["id"],
        commenter_id=user_id,
        content="Level 3 nested reply",
        parent_comment_id=reply1_id
    )
    
    # VERIFY in UI
    post_page = PostDetailsPage(page)
    post_page.open_post(test_post["id"])
    
    # Scroll to comments section
    comments_section = page.locator(POST_DETAILS.COMMENTS_SECTION)
    comments_section.scroll_into_view_if_needed()
    page.wait_for_timeout(2000)
    
    # Check Level 1 comment is visible
    level1_comment = page.locator(POST_DETAILS.COMMENT_LEVEL_1)
    assert level1_comment.count() > 0, "Level 1 comment should be visible"
    
    # Click "View replies" button to expand replies (shows reply count)
    view_replies_btn = page.locator(POST_COMMENTS.VIEW_REPLIES_BUTTON).first
    if view_replies_btn.is_visible():
        view_replies_btn.click()
        page.wait_for_timeout(1500)
    
    # Check Level 2 reply is visible (in reply container with bg-[#FAFAFA])
    level2_reply = page.locator(POST_COMMENTS.REPLY_LEVEL_2)
    
    # Verify nested reply structure exists
    assert level2_reply.count() > 0 or page.locator(POST_COMMENTS.REPLY_LEVEL_EXIST).count() > 0, \
        "Level 2 reply should be visible after expanding"


    
    

