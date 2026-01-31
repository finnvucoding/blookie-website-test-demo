"""
API Client for Blog Website Backend
====================================
Provides a clean interface for all API interactions with automatic:
- Session management
- Authentication (JWT tokens via cookies)
- Response parsing
- Error handling

Usage:
    from utils.api_client import BlogAPIClient
    
    api = BlogAPIClient()
    api.auth.login(email="test@example.com", password="pass123")
    posts = api.posts.get_newsfeed()
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from requests import Session, Response
from config.settings import settings
from core.logger import log

logger = log()


@dataclass
class APIResponse:
    """Standardized API response wrapper."""
    status_code: int
    data: Any
    success: bool
    raw_response: Response

    @property
    def json(self) -> Dict[str, Any]:
        """Get response as JSON dict."""
        if isinstance(self.data, dict):
            return self.data
        return {}


class BaseAPIClient:
    """Base client with common HTTP methods."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = Session()
        self.session.headers.update({
            **settings.default_headers,
            "Content-Type": "application/json",
        })
    
    def _mask_sensitive_data(self, data: dict) -> dict:
        """Mask sensitive fields in request/response data for logging."""
        if not isinstance(data, dict):
            return data
        
        sensitive_keys = ["password", "secret", "token", "accessToken", "refreshToken", 
                         "key", "credential", "pass", "pwd", "api_key", "apiKey"]
        
        masked = data.copy()
        for key in masked:
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                masked[key] = "********"
            elif isinstance(masked[key], dict):
                masked[key] = self._mask_sensitive_data(masked[key])
        return masked
        
    def _request(
        self, 
        method: str, 
        endpoint: str, 
        **kwargs
    ) -> APIResponse:
        """
        Internal request handler with logging and error handling.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (will be joined with base_url)
            **kwargs: Additional arguments for requests (json, params, headers, etc.)
        
        Returns:
            APIResponse object
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Set timeout if not provided
        kwargs.setdefault('timeout', settings.timeouts.API_REQUEST / 1000)
        
        logger.info(f"🌐 {method} {url}")
        if 'json' in kwargs:
            # Mask sensitive fields before logging
            log_body = self._mask_sensitive_data(kwargs['json'])
            logger.debug(f"📤 Request Body: {log_body}")
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Try to parse JSON
            try:
                data = response.json()
            except Exception:
                data = response.text
            
            logger.info(f"✅ Response: {response.status_code}")
            # Mask sensitive fields in response before logging
            log_data = self._mask_sensitive_data(data) if isinstance(data, dict) else data
            logger.debug(f"📥 Response Data: {log_data}")
            
            return APIResponse(
                status_code=response.status_code,
                data=data,
                success=response.ok,
                raw_response=response
            )
            
        except Exception as e:
            logger.error(f"❌ API Request Failed: {str(e)}")
            raise
    
    def get(self, endpoint: str, **kwargs) -> APIResponse:
        """HTTP GET request."""
        return self._request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> APIResponse:
        """HTTP POST request."""
        return self._request("POST", endpoint, **kwargs)
    
    def patch(self, endpoint: str, **kwargs) -> APIResponse:
        """HTTP PATCH request."""
        return self._request("PATCH", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> APIResponse:
        """HTTP PUT request."""
        return self._request("PUT", endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> APIResponse:
        """HTTP DELETE request."""
        return self._request("DELETE", endpoint, **kwargs)


class AuthAPI:
    """Authentication API endpoints."""
    
    def __init__(self, client: BaseAPIClient):
        self.client = client
    
    def register(self, email: str, name: str, password: str) -> APIResponse:
        """
        Register new user account.
        
        Args:
            email: User email address
            name: User display name (min 2 chars)
            password: Password (min 8 chars, must contain uppercase, lowercase, number)
        """
        return self.client.post("auth/register", json={
            "email": email,
            "name": name,
            "password": password
        })
    
    def login(self, email_or_username: str, password: str) -> APIResponse:
        """
        Login user and store authentication token.
        Backend returns JWT in response body as accessToken.
        """
        response = self.client.post("auth/login", json={
            "emailOrUsername": email_or_username,
            "password": password
        })
        
        if response.success:
            logger.info(f"🔐 Logged in as: {email_or_username}")
            # Extract access token from response and set it in header
            data = response.json.get("data", {})
            access_token = data.get("accessToken")
            if access_token:
                self.client.session.headers["Authorization"] = f"Bearer {access_token}"
                logger.debug("🔑 Auth token set in headers")
        
        return response
    
    def logout(self) -> APIResponse:
        """Logout current user and clear auth token."""
        response = self.client.post("auth/logout")
        # Clear auth header
        self.client.session.headers.pop("Authorization", None)
        return response
    
    def get_current_user(self) -> APIResponse:
        """Get current authenticated user info."""
        return self.client.get("auth/me")


class PostsAPI:
    """Blog Posts API endpoints."""
    
    def __init__(self, client: BaseAPIClient):
        self.client = client
    
    def get_newsfeed(
        self, 
        page: int = 1, 
        limit: int = 20,
        user_id: Optional[int] = None
    ) -> APIResponse:
        """Get newsfeed posts (homepage)."""
        params = {"page": page, "limit": limit}
        if user_id:
            params["userId"] = user_id
        return self.client.get("newsfeed", params=params)
    
    def create_post(self, post_data: Dict[str, Any]) -> APIResponse:
        """
        Create new blog post.
        
        Args:
            post_data: {
                "title": "Post Title",
                "description": "Post description",
                "type": "PERSONAL" | "COMMUNITY" | "REPOST",
                "blocks": [...],  # Content blocks
                "authorId": 1,
                "communityId": null | 1,  # For community posts
                "hashtagIds": [1, 2],  # Optional
            }
        """
        return self.client.post("blog-posts", json=post_data)
    
    def get_post(self, post_id: int, user_id: Optional[int] = None) -> APIResponse:
        """Get single post details."""
        params = {"userId": user_id} if user_id else {}
        return self.client.get(f"blog-posts/{post_id}", params=params)
    
    def update_post(self, post_id: int, update_data: Dict[str, Any]) -> APIResponse:
        """Update existing post."""
        return self.client.patch(f"blog-posts/{post_id}", json=update_data)
    
    def delete_post(self, post_id: int) -> APIResponse:
        """Delete post."""
        return self.client.delete(f"blog-posts/{post_id}")
    
    def repost(self, original_post_id: int, author_id: int) -> APIResponse:
        """Create repost."""
        return self.client.post("blog-posts/repost", json={
            "authorId": author_id,
            "originalPostId": original_post_id,
            "type": "REPOST"
        })
    
    def check_reposted(self, original_post_id: int) -> APIResponse:
        """Check if current user already reposted."""
        return self.client.get(
            "blog-posts/repost/check",
            params={"originalPostId": original_post_id}
        )
    
    def delete_repost(self, original_post_id: int) -> APIResponse:
        """Remove repost."""
        return self.client.delete(
            "blog-posts/repost",
            params={"originalPostId": original_post_id}
        )


class VotesAPI:
    """Voting (Upvote/Downvote) API endpoints."""
    
    def __init__(self, client: BaseAPIClient):
        self.client = client
    
    def vote(self, user_id: int, post_id: int, vote_type: str) -> APIResponse:
        """
        Cast or toggle vote.
        
        Args:
            vote_type: "upvote" | "downvote"
        """
        return self.client.post("votes", json={
            "userId": user_id,
            "postId": post_id,
            "voteType": vote_type
        })
    
    def get_vote_status(self, user_id: int, post_id: int) -> APIResponse:
        """Get user's current vote on a post."""
        return self.client.get(
            "votes/status",
            params={"userId": user_id, "postId": post_id}
        )


class CommentsAPI:
    """Comments API endpoints."""
    
    def __init__(self, client: BaseAPIClient):
        self.client = client
    
    def create_comment(
        self,
        post_id: int,
        commenter_id: int,
        content: str,
        parent_comment_id: Optional[int] = None,
        reply_to_user_id: Optional[int] = None
    ) -> APIResponse:
        """Create comment or reply."""
        data = {
            "postId": post_id,
            "commenterId": commenter_id,
            "content": content,
            "type": "POST"  # Comment on post (not on block)
        }
        if parent_comment_id:
            data["parentCommentId"] = parent_comment_id
        if reply_to_user_id:
            data["replyToUserId"] = reply_to_user_id
        return self.client.post("comments", json=data)
    
    def get_comments(
        self,
        post_id: int,
        page: int = 1,
        limit: int = 20
    ) -> APIResponse:
        """Get comments for a post."""
        return self.client.get("comments", params={
            "postId": post_id,
            "page": page,
            "limit": limit
        })
    
    def delete_comment(self, comment_id: int) -> APIResponse:
        """Delete comment."""
        return self.client.delete(f"comments/{comment_id}")


class ReactsAPI:
    """Emoji Reactions API endpoints."""
    
    def __init__(self, client: BaseAPIClient):
        self.client = client
    
    def react(
        self,
        user_id: int,
        target_id: int,
        emoji_id: int,
        target_type: str = "post"
    ) -> APIResponse:
        """
        React with emoji.
        
        Args:
            target_type: "post" | "comment"
        """
        return self.client.post("user-reacts", json={
            "userId": user_id,
            "postId": target_id if target_type == "post" else None,
            "commentId": target_id if target_type == "comment" else None,
            "emojiId": emoji_id,
            "type": target_type.upper()
        })
    
    def get_reacts(self, target_id: int, target_type: str = "post") -> APIResponse:
        """Get all reactions for post/comment."""
        return self.client.get("user-reacts", params={
            "postId" if target_type == "post" else "commentId": target_id
        })


class CommunitiesAPI:
    """Communities API endpoints."""
    
    def __init__(self, client: BaseAPIClient):
        self.client = client
    
    def get_all(self, page: int = 1, limit: int = 20) -> APIResponse:
        """Get all communities."""
        return self.client.get("communities", params={"page": page, "limit": limit})
    
    def get_by_id(self, community_id: int) -> APIResponse:
        """Get community details."""
        return self.client.get(f"communities/{community_id}")
    
    def join(self, community_id: int, user_id: int) -> APIResponse:
        """Join community."""
        return self.client.post(f"communities/{community_id}/join", json={"userId": user_id})


class SavedPostsAPI:
    """Saved Posts API endpoints."""
    
    def __init__(self, client: BaseAPIClient):
        self.client = client
    
    def toggle_save(self, user_id: int, post_id: int) -> APIResponse:
        """Toggle save status of a post."""
        return self.client.post("saved-posts/toggle", json={
            "userId": user_id,
            "postId": post_id
        })
    
    def get_saved_posts(
        self,
        user_id: int,
        page: int = 1,
        limit: int = 20
    ) -> APIResponse:
        """Get user's saved posts."""
        return self.client.get("saved-posts", params={
            "userId": user_id,
            "page": page,
            "limit": limit
        })


class SearchAPI:
    """Search API endpoints."""
    
    def __init__(self, client: BaseAPIClient):
        self.client = client
    
    def search(
        self,
        query: str,
        search_type: str = "all",
        page: int = 1,
        limit: int = 20
    ) -> APIResponse:
        """
        Search posts, users, communities.
        
        Args:
            search_type: "all" | "posts" | "users" | "communities"
        """
        return self.client.get("search", params={
            "query": query,
            "type": search_type,
            "page": page,
            "limit": limit
        })


class BlogAPIClient(BaseAPIClient):
    """
    Main API Client with all endpoints organized by domain.
    
    Usage:
        api = BlogAPIClient()
        api.auth.login("user@example.com", "password123")
        posts = api.posts.get_newsfeed()
    """
    
    def __init__(self, base_url: Optional[str] = None):
        super().__init__(base_url or settings.urls.base_api)
        
        # Initialize domain-specific API handlers
        self.auth = AuthAPI(self)
        self.posts = PostsAPI(self)
        self.votes = VotesAPI(self)
        self.comments = CommentsAPI(self)
        self.reacts = ReactsAPI(self)
        self.communities = CommunitiesAPI(self)
        self.saved_posts = SavedPostsAPI(self)
        self.search = SearchAPI(self)
        
        logger.info(f"🔧 Blog API Client initialized: {self.base_url}")
    
    def get_cookies(self) -> Dict[str, str]:
        """Extract cookies from session (useful for Playwright context injection)."""
        return {cookie.name: cookie.value for cookie in self.session.cookies}
    
    def clear_session(self):
        """Clear all cookies and auth state."""
        self.session.cookies.clear()
        logger.info("🧹 Session cleared")
