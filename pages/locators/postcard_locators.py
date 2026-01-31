from dataclasses import dataclass

@dataclass(frozen=True)
class PostCardSelectors:
    # Base card
    CARD_CONTAINER: str = "div.newsfeed-masonry-item"
    CARD: str = "article.newsfeed-card"
    
    # Thumbnail
    THUMBNAIL_LINK: str = "a.newsfeed-card__thumbnail"
    THUMBNAIL_IMAGE: str = "img.newsfeed-card__image"
    
    # Content link
    CONTENT_LINK: str = "a.newsfeed-card__content"
    
    # Title
    TITLE: str = "h2.newsfeed-card__title"
    
    # Author section
    AUTHOR_SECTION: str = "div.newsfeed-card__author"
    AUTHOR_AVATAR: str = "img.newsfeed-card__avatar"
    AUTHOR_INFO: str = "div.newsfeed-card__author-info"
    AUTHOR_NAME: str = "span.newsfeed-card__username"
    
    # Timestamp
    TIMESTAMP: str = "time.newsfeed-card__time"
    
    # Interaction section
    INTERACT_SECTION: str = "div.newsfeed-card__interact"
    
    # Emoji reactions (existing emojis on post)
    EMOJI_REACTION_BUTTON: str = "button:has(img[alt='emoji'])"
    EMOJI_REACTION_IMAGE: str = "button img[alt='emoji']"
    EMOJI_REACTION_COUNT: str = "button:has(img[alt='emoji']) span.text-sm"
    
    # Add emoji button (smiley face icon - opens picker)
    ADD_EMOJI_BUTTON: str = "button.group:has(svg[viewBox='0 0 16 16'])"
    
    # Voting buttons (arrow up/down)
    VOTE_CONTAINER: str = "div:has(> button.group svg[viewBox='0 0 24 24'])"
    UPVOTE_BUTTON: str = "button.group:has(svg path[d='M12 4L4 14H9V20H15V14H20L12 4Z'])"
    DOWNVOTE_BUTTON: str = "button.group:has(svg path[d='M12 20L20 10H15V4H9V10H4L12 20Z'])"
    VOTE_COUNT: str = "span[style*='font-size: 16px'][style*='font-weight: 600']"
    
    # Save/Bookmark button
    SAVE_BUTTON: str = "button:has(svg.lucide-bookmark)"
    
    # Share/Repost button
    SHARE_BUTTON: str = "button:has(svg.lucide-repeat-2), button:has(svg.lucide-repeat2)"
    
    # More options (ellipsis menu)
    MORE_OPTIONS_BUTTON: str = "button[title='Thêm']:has(svg.lucide-ellipsis)"
    
    # For getting post URL from card
    POST_LINK: str = "a[href^='/post/']"


@dataclass(frozen=True) 
class PostCardInteractSelectors:
    """
    Detailed selectors for the interaction bar at bottom of post card.
    For testing emoji reactions, voting, save, share actions.
    """
    # Bottom interaction bar
    INTERACT_BAR: str = "div.border-t.border-t-\\[\\#FFC9DC\\]"
    
    # Left side - voting
    VOTE_SECTION: str = "div:has(> button.group):first-child"
    UPVOTE_BUTTON: str = "button.group:has(svg path[d*='M12 4L4 14'])"
    DOWNVOTE_BUTTON: str = "button.group:has(svg path[d*='M12 20L20 10'])"
    VOTE_COUNT: str = "span[style*='font-family: Quicksand']"
    
    # Right side - actions
    ACTIONS_SECTION: str = "div.flex.items-center.gap-4"
    SAVE_BUTTON: str = "button:has(svg.lucide-bookmark)"
    SHARE_BUTTON: str = "button:has(svg.lucide-repeat2)"
    MORE_BUTTON: str = "button[title='Thêm']"


# Export instances
POST_CARD = PostCardSelectors()
POST_CARD_INTERACT = PostCardInteractSelectors()