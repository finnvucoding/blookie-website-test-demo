from dataclasses import dataclass

@dataclass(frozen=True)
class NewsfeedSelectors:
    """Newsfeed/Homepage selectors - based on actual HTML."""
    # Page header
    PAGE_TITLE: str = "h1.text-3xl.text-\\[\\#F295B6\\]"
    
    # Post cards container
    POSTS_CONTAINER: str = ".newsfeed-masonry-item"
    POST_CARD: str = "article.newsfeed-card"
    
    # Post card elements
    POST_THUMBNAIL_LINK: str = "a.newsfeed-card__thumbnail"
    POST_THUMBNAIL_IMAGE: str = "img.newsfeed-card__image"
    POST_CONTENT_LINK: str = "a.newsfeed-card__content"
    POST_TITLE: str = "h2.newsfeed-card__title"
    POST_AUTHOR_SECTION: str = ".newsfeed-card__author"
    POST_AUTHOR_AVATAR: str = "img.newsfeed-card__avatar"
    POST_AUTHOR_USERNAME: str = "span.newsfeed-card__username"
    POST_TIMESTAMP: str = "time.newsfeed-card__time"
    
    # Interaction section
    INTERACT_SECTION: str = ".newsfeed-card__interact"
    
    # Emoji reactions - existing emoji buttons with count
    EMOJI_REACTION_BUTTON: str = "button:has(img[alt='emoji'])"
    EMOJI_REACTION_COUNT: str = "button:has(img[alt='emoji']) span.text-sm"
    
    # Add emoji button (opens picker)
    ADD_EMOJI_BUTTON: str = "button.group:has(svg[viewBox='0 0 16 16'])"
    
    # Voting buttons
    UPVOTE_BUTTON: str = "button.group:has(svg path[d='M12 4L4 14H9V20H15V14H20L12 4Z'])"
    DOWNVOTE_BUTTON: str = "button.group:has(svg path[d='M12 20L20 10H15V4H9V10H4L12 20Z'])"
    VOTE_COUNT: str = "div:has(> button.group) > span"
    
    # Action buttons
    SAVE_BUTTON: str = "button:has(svg.lucide-bookmark)"
    SHARE_BUTTON: str = "button:has(svg.lucide-repeat-2), button:has(svg.lucide-repeat2)"
    MORE_OPTIONS_BUTTON: str = "button[title='Thêm']:has(svg.lucide-ellipsis)"


@dataclass(frozen=True)
class EmojiPickerSelectors:
    """Emoji picker dialog selectors."""
    # Dialog container
    DIALOG: str = "div[style*='box-shadow'][style*='border-radius: 12px']"
    
    # Search input
    SEARCH_INPUT: str = "input[placeholder*='Tìm emoji']"
    
    # Category buttons
    CATEGORY_BUTTON: str = "button[title]"
    CATEGORY_SMILEYS: str = "button[title='Smileys & Emotion']"
    CATEGORY_PEOPLE: str = "button[title='People & Body']"
    CATEGORY_ANIMALS: str = "button[title='Animals & Nature']"
    CATEGORY_FOOD: str = "button[title='Food & Drink']"
    CATEGORY_ACTIVITIES: str = "button[title='Activities']"
    CATEGORY_SYMBOLS: str = "button[title='Symbols']"
    CATEGORY_FLAGS: str = "button[title='Flags']"
    
    # Emoji buttons (grid of emojis)
    EMOJI_BUTTON: str = "button:has(img[src*='twemoji'])"
    EMOJI_IMAGE: str = "img[src*='twemoji']"
    
    # First emoji in grid
    FIRST_EMOJI: str = "button:has(img[src*='twemoji']):first-child"


# Export instances
NEWSFEED = NewsfeedSelectors()
EMOJI_PICKER = EmojiPickerSelectors()