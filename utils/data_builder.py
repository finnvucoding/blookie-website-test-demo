"""
Test Data Builders using Faker
===============================
Generate realistic test data for Blog Website testing.
Follows Builder Pattern for flexibility.

Usage:
    from utils.data_builder import UserBuilder, PostBuilder
    
    user_data = UserBuilder().with_random_email().build()
    post_data = PostBuilder().with_title("My Post").build()
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from faker import Faker
from enum import Enum
import random

fake = Faker()


class BlogPostType(Enum):
    """Blog post types matching backend enum."""
    PERSONAL = "PERSONAL"
    COMMUNITY = "COMMUNITY"
    REPOST = "REPOST"


class BlockType(Enum):
    """Content block types."""
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    CODE = "CODE"
    QUOTE = "QUOTE"


@dataclass
class UserData:
    """User registration/profile data."""
    email: str
    name: str  # Backend uses 'name', not 'username'
    password: str
    bio: Optional[str] = None
    gender: Optional[str] = None  # "male" | "female" | "other"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict, excluding None values."""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class BlockData:
    """Content block data."""
    type: str
    content: str
    x: int = 0
    y: int = 0
    width: int = 12
    height: int = 100
    image_caption: Optional[str] = None
    object_fit: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "type": self.type,
            "content": self.content,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height
        }
        if self.image_caption:
            result["imageCaption"] = self.image_caption
        if self.object_fit:
            result["objectFit"] = self.object_fit
        return result


@dataclass
class PostData:
    """Blog post creation data."""
    title: str
    type: str
    author_id: int
    blocks: List[Dict[str, Any]] = field(default_factory=list)
    community_id: Optional[int] = None
    original_post_id: Optional[int] = None  # For reposts
    hashtag_ids: List[int] = field(default_factory=list)
    thumbnail_url: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to API-ready dict."""
        data = {
            "title": self.title,
            "type": self.type,
            "authorId": self.author_id,
            "blocks": self.blocks,
        }
        
        if self.community_id:
            data["communityId"] = self.community_id
        if self.original_post_id:
            data["originalPostId"] = self.original_post_id
        if self.hashtag_ids:
            data["hashtagIds"] = self.hashtag_ids
        if self.thumbnail_url:
            data["thumbnailUrl"] = self.thumbnail_url
            
        return data


@dataclass
class CommentData:
    """Comment creation data."""
    post_id: int
    commenter_id: int
    content: str
    comment_type: str = "POST"  # POST or BLOCK
    parent_comment_id: Optional[int] = None  # For replies
    reply_to_user_id: Optional[int] = None
    block_id: Optional[int] = None  # For BLOCK type comments
    
    def to_dict(self) -> Dict[str, Any]:
        data = {
            "postId": self.post_id,
            "commenterId": self.commenter_id,
            "content": self.content,
            "type": self.comment_type,
        }
        if self.parent_comment_id:
            data["parentCommentId"] = self.parent_comment_id
        if self.reply_to_user_id:
            data["replyToUserId"] = self.reply_to_user_id
        if self.block_id and self.comment_type == "BLOCK":
            data["blockId"] = self.block_id
        return data


# ============================================
# BUILDER CLASSES
# ============================================

class UserBuilder:
    """
    Builder for User test data.
    
    Example:
        user = (UserBuilder()
                .with_random_email()
                .with_name("John Doe")
                .with_password("Test@123")
                .build())
    """
    
    def __init__(self):
        self._data = UserData(
            email="",
            name="",  # Backend uses 'name', not 'username'
            password="Test@12345"  # Default secure password
        )
    
    def with_email(self, email: str) -> 'UserBuilder':
        """Set specific email."""
        self._data.email = email
        return self
    
    def with_random_email(self) -> 'UserBuilder':
        """Generate random email."""
        self._data.email = fake.email()
        return self
    
    def with_name(self, name: str) -> 'UserBuilder':
        """Set specific display name."""
        self._data.name = name
        return self
    
    def with_random_name(self) -> 'UserBuilder':
        """Generate random full name."""
        self._data.name = fake.name()
        return self
    
    def with_password(self, password: str) -> 'UserBuilder':
        """Set specific password."""
        self._data.password = password
        return self
    
    def with_bio(self, bio: str) -> 'UserBuilder':
        """Set bio."""
        self._data.bio = bio
        return self
    
    def with_random_bio(self) -> 'UserBuilder':
        """Generate random bio."""
        self._data.bio = fake.text(max_nb_chars=200)
        return self
    
    def with_gender(self, gender: str) -> 'UserBuilder':
        """Set gender."""
        self._data.gender = gender
        return self
    
    def as_male(self) -> 'UserBuilder':
        """Set gender as male."""
        self._data.gender = "male"
        return self
    
    def as_female(self) -> 'UserBuilder':
        """Set gender as female."""
        self._data.gender = "female"
        return self
    
    def build(self) -> UserData:
        """Build and return UserData object."""
        # Auto-generate missing required fields
        if not self._data.email:
            self._data.email = fake.email()
        if not self._data.name:
            self._data.name = fake.name()  # Generate full name
        
        return self._data


class BlockBuilder:
    """
    Builder for content blocks.
    
    Example:
        block = (BlockBuilder()
                 .as_text()
                 .with_content("Hello World")
                 .at_position(0, 0)
                 .with_size(12, 100)
                 .build())
    """
    
    def __init__(self):
        self._data = BlockData(
            type=BlockType.TEXT.value,
            content="",
            x=0,
            y=0,
            width=12,
            height=100
        )
    
    def as_text(self) -> 'BlockBuilder':
        """Set block type as TEXT."""
        self._data.type = BlockType.TEXT.value
        return self
    
    def as_image(self) -> 'BlockBuilder':
        """Set block type as IMAGE."""
        self._data.type = BlockType.IMAGE.value
        return self
    
    def as_code(self) -> 'BlockBuilder':
        """Set block type as CODE."""
        self._data.type = BlockType.CODE.value
        return self
    
    def as_quote(self) -> 'BlockBuilder':
        """Set block type as QUOTE."""
        self._data.type = BlockType.QUOTE.value
        return self
    
    def with_content(self, content: str) -> 'BlockBuilder':
        """Set block content."""
        self._data.content = content
        return self
    
    def with_random_text(self, paragraphs: int = 1) -> 'BlockBuilder':
        """Generate random text content."""
        self._data.content = fake.paragraph()
        return self
    
    def with_random_image_url(self) -> 'BlockBuilder':
        """Generate random image URL."""
        self._data.content = fake.image_url()
        return self
    
    def at_position(self, x: int = 0, y: int = 0) -> 'BlockBuilder':
        """Set block position."""
        self._data.x = x
        self._data.y = y
        return self
    
    def with_size(self, width: int = 12, height: int = 100) -> 'BlockBuilder':
        """Set block size."""
        self._data.width = width
        self._data.height = height
        return self
    
    def build(self) -> Dict[str, Any]:
        """Build and return block as dict."""
        if not self._data.content:
            # Auto-generate content based on type
            if self._data.type == BlockType.TEXT.value:
                self._data.content = fake.paragraph()
            elif self._data.type == BlockType.IMAGE.value:
                self._data.content = fake.image_url()
            elif self._data.type == BlockType.CODE.value:
                self._data.content = "print('Hello World')"
        
        return self._data.to_dict()


class PostBuilder:
    """
    Builder for Blog Post test data.
    
    Example:
        post = (PostBuilder()
                .with_author(1)
                .with_title("My Post")
                .add_text_block("Content here")
                .as_personal()
                .build())
    """
    
    def __init__(self):
        self._data = PostData(
            title="",
            type=BlogPostType.PERSONAL.value,
            author_id=0,
            blocks=[]
        )
    
    def with_author(self, author_id: int) -> 'PostBuilder':
        """Set author ID."""
        self._data.author_id = author_id
        return self
    
    def with_title(self, title: str) -> 'PostBuilder':
        """Set post title."""
        self._data.title = title
        return self
    
    def with_random_title(self) -> 'PostBuilder':
        """Generate random title."""
        self._data.title = fake.sentence(nb_words=6).rstrip('.')
        return self
    
    def as_personal(self) -> 'PostBuilder':
        """Set post type as PERSONAL."""
        self._data.type = BlogPostType.PERSONAL.value
        return self
    
    def as_community(self, community_id: int) -> 'PostBuilder':
        """Set post type as COMMUNITY."""
        self._data.type = BlogPostType.COMMUNITY.value
        self._data.community_id = community_id
        return self
    
    def as_repost(self, original_post_id: int) -> 'PostBuilder':
        """Set post type as REPOST."""
        self._data.type = BlogPostType.REPOST.value
        self._data.original_post_id = original_post_id
        return self
    
    def add_block(self, block: Dict[str, Any]) -> 'PostBuilder':
        """Add a content block."""
        self._data.blocks.append(block)
        return self
    
    def add_text_block(self, content: str, y: int = None) -> 'PostBuilder':
        """Quick add text block."""
        block_y = y if y is not None else len(self._data.blocks) * 100
        block = BlockBuilder().as_text().with_content(content).at_position(0, block_y).with_size(12, 100).build()
        self._data.blocks.append(block)
        return self
    
    def add_random_text_blocks(self, count: int = 3) -> 'PostBuilder':
        """Add multiple random text blocks."""
        for i in range(count):
            block_y = len(self._data.blocks) * 100
            block = BlockBuilder().as_text().with_random_text().at_position(0, block_y).with_size(12, 100).build()
            self._data.blocks.append(block)
        return self
    
    def add_image_block(self, image_url: str, y: int = None) -> 'PostBuilder':
        """Quick add image block."""
        block_y = y if y is not None else len(self._data.blocks) * 100
        block = BlockBuilder().as_image().with_content(image_url).at_position(0, block_y).with_size(12, 200).build()
        self._data.blocks.append(block)
        return self
    
    def with_hashtags(self, hashtag_ids: List[int]) -> 'PostBuilder':
        """Set hashtag IDs."""
        self._data.hashtag_ids = hashtag_ids
        return self
    
    def with_thumbnail(self, url: str) -> 'PostBuilder':
        """Set thumbnail URL."""
        self._data.thumbnail_url = url
        return self
    
    def build(self) -> PostData:
        """Build and return PostData object."""
        # Auto-generate missing required fields
        if not self._data.title:
            self._data.title = fake.sentence(nb_words=6).rstrip('.')
        if not self._data.blocks:
            # Add at least one text block
            self.add_random_text_blocks(1)
        
        return self._data


class CommentBuilder:
    """
    Builder for Comment test data.
    
    Example:
        comment = (CommentBuilder()
                   .on_post(post_id=1)
                   .by_commenter(user_id=2)
                   .with_content("Great post!")
                   .build())
    """
    
    def __init__(self):
        self._data = CommentData(
            post_id=0,
            commenter_id=0,
            content=""
        )
    
    def on_post(self, post_id: int) -> 'CommentBuilder':
        """Set post ID."""
        self._data.post_id = post_id
        return self
    
    def by_commenter(self, commenter_id: int) -> 'CommentBuilder':
        """Set commenter ID."""
        self._data.commenter_id = commenter_id
        return self
    
    def by_author(self, author_id: int) -> 'CommentBuilder':
        """Alias for by_commenter for backward compatibility."""
        self._data.commenter_id = author_id
        return self
    
    def with_content(self, content: str) -> 'CommentBuilder':
        """Set comment content."""
        self._data.content = content
        return self
    
    def with_random_content(self) -> 'CommentBuilder':
        """Generate random comment."""
        self._data.content = fake.sentence(nb_words=random.randint(5, 15))
        return self
    
    def as_reply_to(self, parent_comment_id: int, reply_to_user_id: int = None) -> 'CommentBuilder':
        """Set as reply to another comment."""
        self._data.parent_comment_id = parent_comment_id
        if reply_to_user_id:
            self._data.reply_to_user_id = reply_to_user_id
        return self
    
    def build(self) -> CommentData:
        """Build and return CommentData object."""
        if not self._data.content:
            self._data.content = fake.sentence()
        
        return self._data


# ============================================
# HELPER FUNCTIONS
# ============================================

def create_quick_user() -> UserData:
    """Quick factory for random user."""
    return UserBuilder().with_random_email().with_random_name().build()


def create_quick_post(author_id: int, blocks_count: int = 2) -> PostData:
    """Quick factory for random post."""
    return (PostBuilder()
            .with_author(author_id)
            .with_random_title()
            .add_random_text_blocks(blocks_count)
            .build())


def create_quick_comment(post_id: int, author_id: int) -> CommentData:
    """Quick factory for random comment."""
    return (CommentBuilder()
            .on_post(post_id)
            .by_author(author_id)
            .with_random_content()
            .build())
