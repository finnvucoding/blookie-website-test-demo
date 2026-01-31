import pytest
from playwright.sync_api import Page
from pages.newsfeed_page import NewsfeedPage
from pages.post_details_page import PostDetailsPage
from utils.api_client import BlogAPIClient


@pytest.mark.skip(reason="UI selectors need to be updated after inspecting actual frontend HTML")
@pytest.mark.ui
@pytest.mark.smoke
class TestWithExistingAccount:
    """Tests using pre-existing account with real data."""
    
    def test_view_existing_user_posts(self, existing_user_page: Page):
        """
        Test ID: EXIST-001
        View posts from existing account.
        
        This test uses the pre-existing account which should have
        posts already created. Good for testing UI with real data.
        """
        page = existing_user_page
        
        # Navigate to newsfeed
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        # Verify posts are visible
        assert newsfeed.is_posts_container_visible(), "Posts should be visible"
        
        post_count = newsfeed.get_post_count()
        print(f"📊 Found {post_count} posts in newsfeed")
        
        # If this account has posts, we should see them
        if post_count > 0:
            titles = newsfeed.get_all_post_titles()
            print(f"📝 Post titles: {titles}")
            assert len(titles) > 0, "Should have post titles"
    
    def test_existing_account_can_create_post(
        self,
        existing_user_page: Page,
        existing_user_api: BlogAPIClient
    ):
        """
        Test ID: EXIST-002
        Existing account can create new posts.
        
        Strategy: Create via API, verify via UI
        """
        page = existing_user_page
        
        # Create post via API
        from utils.data_builder import PostBuilder
        user_id = existing_user_api._test_user["id"]
        
        post_data = PostBuilder() \
            .with_author(user_id) \
            .with_title("Test Post from Existing Account") \
            .add_text_block("This is test content - Created during test execution") \
            .build()
        
        response = existing_user_api.posts.create_post(post_data.to_dict())
        assert response.success, f"Post creation failed: {response.data}"
        
        post_id = response.json.get("data", {}).get("id")
        print(f"✅ Created post ID: {post_id}")
        
        # Verify in UI
        newsfeed = NewsfeedPage(page)
        newsfeed.open()
        
        titles = newsfeed.get_all_post_titles()
        assert post_data.title in titles, "New post should appear in newsfeed"
    
    def test_existing_account_can_comment(
        self,
        existing_user_page: Page,
        existing_user_api: BlogAPIClient
    ):
        """
        Test ID: EXIST-003
        Existing account can comment on posts.
        """
        page = existing_user_page
        
        # First, create a test post
        from utils.data_builder import create_quick_post
        user_id = existing_user_api._test_user["id"]
        post_data = create_quick_post(user_id)
        
        create_resp = existing_user_api.posts.create_post(post_data.to_dict())
        post_id = create_resp.json.get("data", {}).get("id")
        
        # Open post and add comment via UI
        post_page = PostDetailsPage(page)
        post_page.open_post(post_id)
        
        comment_text = "Comment from existing account!"
        post_page.add_comment(comment_text)
        
        # Verify
        page.wait_for_timeout(1500)
        comments = post_page.get_all_comments_text()
        assert comment_text in comments, "Comment should appear"


@pytest.mark.api
class TestExistingAccountAPI:
    """API tests with existing account."""
    
    def test_existing_account_info(self, existing_user_api: BlogAPIClient):
        """
        Test ID: EXIST-API-001
        Get current user info for existing account.
        """
        response = existing_user_api.auth.get_current_user()
        
        assert response.success, "Should get user info"
        
        data = response.json.get("data", {})
        print(f"👤 User ID: {data.get('id')}")
        print(f"📧 Email: {data.get('email')}")
        print(f"👨‍💼 Username: {data.get('username')}")
        
        assert data.get("email") == existing_user_api._test_user["email"]
    
    def test_get_existing_account_posts(self, existing_user_api: BlogAPIClient):
        """
        Test ID: EXIST-API-002
        Get posts created by existing account.
        """
        user_id = existing_user_api._test_user["id"]
        
        # Get newsfeed (should include user's posts)
        response = existing_user_api.posts.get_newsfeed(
            page=1,
            limit=20,
            user_id=user_id
        )
        
        assert response.success, "Should get newsfeed"
        
        data = response.json.get("data", {})
        posts = data.get("items", [])
        
        print(f"📊 Found {len(posts)} posts in newsfeed")
        
        # Print post titles
        for post in posts[:5]:  # First 5
            print(f"  - {post.get('title')}")


@pytest.mark.smoke
def test_comparison_existing_vs_new_user(
    existing_user_api: BlogAPIClient,
    api_as_user: BlogAPIClient
):
    """
    Test ID: COMPARE-001
    Compare behavior between existing and new accounts.
    
    Demonstrates when to use which fixture.
    """
    # Existing account - may have data
    existing_resp = existing_user_api.posts.get_newsfeed()
    existing_posts = existing_resp.json.get("data", {}).get("items", [])
    
    # New account - fresh, no data
    new_resp = api_as_user.posts.get_newsfeed()
    new_posts = new_resp.json.get("data", {}).get("items", [])
    
    print(f"📊 Existing account sees: {len(existing_posts)} posts")
    print(f"📊 New account sees: {len(new_posts)} posts")
    
    # New account is isolated, might see fewer posts
    assert isinstance(existing_posts, list)
    assert isinstance(new_posts, list)


# ============================================
# WHEN TO USE WHICH FIXTURE?
# ============================================

"""
🔍 DECISION GUIDE:

Use `existing_user_api` / `existing_user_page` when:
✅ Testing with realistic data (posts, followers, etc.)
✅ Testing UI display of existing content
✅ Performance testing with loaded account
✅ Exploratory testing
✅ Manual testing scenarios

Use `api_as_user` / `logged_in_page` when:
✅ Need isolated, clean state
✅ Testing specific functionality in isolation
✅ Creating controlled test scenarios
✅ Avoiding test data pollution
✅ Parallel test execution (no conflicts)

Example:
    # Test post creation (isolated) ✅
    def test_create_post(api_as_user):
        # Clean slate, no interference
        
    # Test newsfeed with data (realistic) ✅
    def test_newsfeed_display(existing_user_page):
        # See how UI handles real data
"""
