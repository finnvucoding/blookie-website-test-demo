"""
Blog Posts Tests
================
Test post creation, editing, deletion, and interactions.

Strategy:
- Create/Setup via API (fast)
- Verify via UI (user-facing)
- Test interactions (upvote, downvote, save, repost)
"""

import pytest
from playwright.sync_api import Page
from pages.newsfeed_page import NewsfeedPage
from pages.post_details_page import PostDetailsPage
from utils.api_client import BlogAPIClient
from utils.data_builder import PostBuilder


@pytest.mark.skip(reason="UI selectors need to be updated after inspecting actual frontend HTML")
@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.posts
class TestPostCreation:
    """Post creation tests."""
    
    def test_create_post_via_api_visible_in_ui(
        self,
        logged_in_page: Page,
        api_as_user: BlogAPIClient,
        test_post: dict
    ):
        """
        Test ID: POST-001
        Test post created via API is visible in UI.
        
        Strategy: Hybrid - Create via API, Verify via UI
        """
        page = logged_in_page
        
        # Navigate to newsfeed
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        # Get all post titles
        titles = newsfeed.get_all_post_titles()
        
        # Verify our test post is visible
        assert test_post["title"] in titles, \
            f"Post '{test_post['title']}' should be visible in newsfeed"
    
    def test_post_count_increases_after_creation(
        self,
        logged_in_page: Page,
        api_as_user: BlogAPIClient
    ):
        """
        Test ID: POST-002
        Test post count increases after creating a post.
        """
        page = logged_in_page
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        # Get initial count
        initial_count = newsfeed.get_post_count()
        
        # Create new post via API
        from utils.data_builder import create_quick_post
        user_id = api_as_user._test_user["id"]
        post_data = create_quick_post(user_id)
        
        response = api_as_user.posts.create_post(post_data.to_dict())
        assert response.success, "Post creation failed"
        
        # Refresh page
        newsfeed.refresh()
        newsfeed.wait_for_posts_to_load()
        
        # Verify count increased
        new_count = newsfeed.get_post_count()
        assert new_count > initial_count, \
            f"Post count should increase from {initial_count} to {new_count}"


@pytest.mark.ui
@pytest.mark.posts
class TestPostDetails:
    """Post detail page tests."""
    
    def test_view_post_details(
        self,
        logged_in_page: Page,
        test_post: dict
    ):
        """
        Test ID: POST-010
        Test viewing post details page.
        """
        page = logged_in_page
        post_page = PostDetailsPage(page)
        
        # Open post details
        post_page.open_post(test_post["id"])
        
        # Verify post content
        assert post_page.is_post_visible(), "Post should be visible"
        
        title = post_page.get_post_title()
        assert test_post["title"] in title, \
            f"Title should match: expected '{test_post['title']}', got '{title}'"
    
    def test_post_details_shows_author_info(
        self,
        logged_in_page: Page,
        test_post: dict
    ):
        """
        Test ID: POST-011
        Test post details displays author information.
        """
        page = logged_in_page
        post_page = PostDetailsPage(page)
        
        post_page.open_post(test_post["id"])
        
        # Verify author section visible
        author_name = post_page.get_author_name()
        assert len(author_name) > 0, "Author name should be displayed"


@pytest.mark.skip(reason="UI selectors need to be updated after inspecting actual frontend HTML")
@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.posts
@pytest.mark.interactions
class TestPostVoting:
    """Test upvote/downvote functionality."""
    
    def test_upvote_post(
        self,
        logged_in_page: Page,
        test_post: dict
    ):
        """
        Test ID: VOTE-001
        Test user can upvote a post.
        
        Steps:
            1. Open post details
            2. Click upvote button
            3. Verify upvote count increased
        """
        page = logged_in_page
        post_page = PostDetailsPage(page)
        
        post_page.open_post(test_post["id"])
        
        # Click upvote
        post_page.upvote_post()
        
        # Wait for update
        page.wait_for_timeout(1000)
        
        # Verify upvote button is active
        # (This depends on frontend implementation - adjust selector)
        assert post_page.is_upvote_active(), "Upvote button should be in active state"
    
    def test_toggle_upvote(
        self,
        logged_in_page: Page,
        test_post: dict
    ):
        """
        Test ID: VOTE-002
        Test clicking upvote twice toggles it off.
        """
        page = logged_in_page
        post_page = PostDetailsPage(page)
        
        post_page.open_post(test_post["id"])
        
        # Upvote
        post_page.upvote_post()
        page.wait_for_timeout(500)
        
        # Upvote again (toggle off)
        post_page.upvote_post()
        page.wait_for_timeout(500)
        
        # Verify not active
        assert not post_page.is_upvote_active(), "Upvote should be toggled off"
    
    def test_downvote_post(
        self,
        logged_in_page: Page,
        test_post: dict
    ):
        """
        Test ID: VOTE-003
        Test user can downvote a post.
        """
        page = logged_in_page
        post_page = PostDetailsPage(page)
        
        post_page.open_post(test_post["id"])
        
        # Click downvote
        post_page.downvote_post()
        
        page.wait_for_timeout(1000)
        
        # Verify downvote registered
        # (Add assertions based on frontend implementation)


@pytest.mark.ui
@pytest.mark.posts
@pytest.mark.interactions
class TestPostSaving:
    """Test save post functionality."""
    
    def test_save_post(
        self,
        logged_in_page: Page,
        test_post: dict
    ):
        """
        Test ID: SAVE-001
        Test user can save a post.
        """
        page = logged_in_page
        post_page = PostDetailsPage(page)
        
        post_page.open_post(test_post["id"])
        
        # Click save button
        post_page.save_post()
        
        page.wait_for_timeout(1000)
        
        # Verify save button state changed (implementation-dependent)
        # Could check if button text changed to "Saved" or icon changed


@pytest.mark.skip(reason="Repost button locator needs update for post details page - different from newsfeed")
@pytest.mark.ui
@pytest.mark.posts
@pytest.mark.interactions
class TestRepost:
    """Test repost functionality."""
    
    def test_repost_post(
        self,
        logged_in_page: Page,
        test_post: dict
    ):
        """
        Test ID: REPOST-001
        Test user can repost a post.
        """
        page = logged_in_page
        post_page = PostDetailsPage(page)
        
        post_page.open_post(test_post["id"])
        
        # Click repost
        post_page.click_repost()
        
        page.wait_for_timeout(1500)
        
        # Verify repost action completed
        # (Check if confirmation modal appears or redirect happens)


@pytest.mark.api
@pytest.mark.posts
class TestPostAPI:
    """API-level post tests."""
    
    def test_create_post_via_api(self, api_as_user: BlogAPIClient):
        """
        Test ID: POST-API-001
        Test creating post via API.
        """
        user_id = api_as_user._test_user["id"]
        
        post_data = PostBuilder() \
            .with_author(user_id) \
            .with_title("Test Post via API") \
            .add_text_block("This is a test post") \
            .build()
        
        response = api_as_user.posts.create_post(post_data.to_dict())
        
        assert response.success, f"Post creation failed: {response.data}"
        assert response.status_code in [200, 201]
        
        # Verify response contains post ID
        post_id = response.json.get("data", {}).get("id")
        assert post_id is not None, "Response should contain post ID"
    
    def test_get_post_by_id(self, api_as_user: BlogAPIClient, test_post: dict):
        """
        Test ID: POST-API-002
        Test retrieving post by ID via API.
        """
        response = api_as_user.posts.get_post(test_post["id"])
        
        assert response.success, "Should retrieve post successfully"
        
        data = response.json.get("data", {})
        assert data.get("id") == test_post["id"]
        assert data.get("title") == test_post["title"]
    
    def test_update_post(self, api_as_user: BlogAPIClient, test_post: dict):
        """
        Test ID: POST-API-003
        Test updating post via API.
        """
        new_title = "Updated Title"
        
        response = api_as_user.posts.update_post(
            test_post["id"],
            {"title": new_title}
        )
        
        assert response.success, "Update should succeed"
        
        # Verify update
        get_response = api_as_user.posts.get_post(test_post["id"])
        updated_title = get_response.json.get("data", {}).get("title")
        assert updated_title == new_title, "Title should be updated"
    
    def test_delete_post(self, api_as_user: BlogAPIClient):
        """
        Test ID: POST-API-004
        Test deleting post via API.
        """
        # Create a post
        from utils.data_builder import create_quick_post
        user_id = api_as_user._test_user["id"]
        post_data = create_quick_post(user_id)
        
        create_resp = api_as_user.posts.create_post(post_data.to_dict())
        post_id = create_resp.json.get("data", {}).get("id")
        
        # Delete it
        delete_resp = api_as_user.posts.delete_post(post_id)
        assert delete_resp.success, "Delete should succeed"
        
        # Verify deleted (404 when trying to get)
        get_resp = api_as_user.posts.get_post(post_id)
        assert get_resp.status_code == 404, "Post should not exist after deletion"


@pytest.mark.regression
@pytest.mark.slow
def test_multiple_posts_creation_performance(api_as_user: BlogAPIClient):
    """
    Test ID: POST-PERF-001
    Test creating multiple posts in sequence.
    
    Performance benchmark: Should create 10 posts in < 5 seconds via API.
    """
    import time
    from utils.data_builder import create_quick_post
    
    user_id = api_as_user._test_user["id"]
    
    start_time = time.time()
    
    for i in range(10):
        post_data = create_quick_post(user_id)
        response = api_as_user.posts.create_post(post_data.to_dict())
        assert response.success, f"Post {i+1} creation failed"
    
    elapsed = time.time() - start_time
    
    assert elapsed < 5.0, f"Creating 10 posts took {elapsed:.2f}s, should be < 5s"
