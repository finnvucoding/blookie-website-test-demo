from dataclasses import dataclass


@dataclass(frozen=True)
class PostDetailsSidebarSelectors:
    """Fixed sidebar with voting/actions on post details - based on actual HTML."""
    # Sidebar container (fixed left)
    SIDEBAR: str = "div[style*='position: fixed'][style*='left:']"
    
    # Voting section
    VOTE_SECTION: str = "div:has(> button.group svg path[d*='M12 4L4 14'])"
    UPVOTE_BUTTON: str = "button.group:has(svg path[d='M12 4L4 14H9V20H15V14H20L12 4Z'])"
    DOWNVOTE_BUTTON: str = "button.group:has(svg path[d='M12 20L20 10H15V4H9V10H4L12 20Z'])"
    VOTE_COUNT: str = "span[style*='font-size: 16px'][style*='font-weight: 600']"
    
    # Comment button
    COMMENT_BUTTON: str = "button:has(svg.lucide-message-circle)"
    
    # Bookmark/Save button
    SAVE_BUTTON: str = "button:has(svg.lucide-bookmark)"
    
    # More options (ellipsis)
    MORE_OPTIONS_BUTTON: str = "button[title='Thêm']:has(svg.lucide-ellipsis)"


@dataclass(frozen=True)
class PostDetailsContentSelectors:
    """Post content selectors - based on actual HTML."""
    # Content container
    CONTENT_CONTAINER: str = "div[style*='width: 800px'][style*='padding: 12px']"
    
    # Title and description
    POST_TITLE: str = "h1.w-full"
    POST_DESCRIPTION: str = "p.w-full[style*='font-style: italic']"
    
    # Author section
    AUTHOR_SECTION: str = "div.flex.items-center.gap-3.text-md.text-gray-500"
    AUTHOR_AVATAR: str = "img.rounded-full.object-cover"
    AUTHOR_LINK: str = "a.text-\\[\\#F295B6\\][href^='/profile/']"
    POST_TIMESTAMP: str = "div.text-md.text-gray-400"
    
    # Emoji reactions section
    REACTIONS_SECTION: str = "div.mt-10:has(button img[alt='emoji'])"
    EMOJI_REACTION_BUTTON: str = "button:has(img[alt='emoji'])"
    ADD_EMOJI_BUTTON: str = "button.group:has(svg[viewBox='0 0 16 16'])"
    
    # Content blocks grid
    BLOCKS_CONTAINER: str = "div[style*='width: 800px'] .react-grid-layout"
    BLOCK_ITEM: str = ".react-grid-item"
    
    # Text block
    TEXT_BLOCK: str = "div.text-block"
    TEXT_BLOCK_BY_ID: str = "div[id^='text-block-']"
    TEXT_BLOCK_CONTENT: str = "div.text-block p"
    
    # Image block
    IMAGE_BLOCK: str = "figure:has(img[alt='Blog image'])"
    IMAGE_BLOCK_IMAGE: str = "img[alt='Blog image']"
    
    # Block comment button (appears on hover)
    BLOCK_COMMENT_BUTTON: str = "button[aria-label='Open block comments']"
    BLOCK_COMMENT_ICON: str = "button[aria-label='Open block comments'] svg"


@dataclass(frozen=True)
class PostCommentsSelectors:
    """Post comments section selectors - based on actual HTML."""
    # Comments section container
    COMMENTS_SECTION: str = ".comments-section[data-comments-section='true']"
    COMMENTS_SECTION_ALT: str = "div.comments-section.space-y-6"
    
    # Comments header
    COMMENTS_HEADER: str = ".comments-header"
    COMMENTS_TITLE: str = "h3:has-text('Bình luận')"
    COMMENTS_COUNT: str = "h3.text-xl.font-semibold.text-gray-900"
    
    # Sort dropdown
    SORT_SECTION: str = "div:has(span:text('Sắp xếp theo:'))"
    SORT_LABEL: str = "span:text('Sắp xếp theo:')"
    SORT_DROPDOWN: str = "div#post-comments-sort button"
    SORT_DROPDOWN_TEXT: str = "div#post-comments-sort button span"
    
    # Comment form - scoped to main comments section (not drawer sidebars)
    COMMENT_FORM: str = "main div.comment-form form"
    COMMENT_TEXTAREA: str = "main textarea[placeholder='Bình luận về bài viết này...']"
    COMMENT_SUBMIT_BUTTON: str = "main div.comment-form button[type='submit']:has-text('Gửi')"
    
    # Comments list
    COMMENTS_LIST: str = "div.comments-list.space-y-6"
    COMMENT_ITEM: str = "div.border-b.border-gray-200.py-4"
    
    # Individual comment elements
    COMMENT_AVATAR: str = ".MuiAvatar-root"
    COMMENT_AUTHOR_NAME: str = "span.font-medium.text-gray-800"
    COMMENT_TIME: str = "span.text-xs.text-gray-400"
    COMMENT_OPTIONS_BUTTON: str = "button[title='Tùy chọn']:has(svg.lucide-ellipsis)"
    COMMENT_CONTENT: str = "p.mt-2.text-sm.text-gray-800"
    
    # Comment emoji button
    COMMENT_ADD_EMOJI: str = "button.group:has(svg[viewBox='0 0 16 16'])"
    
    # Comment actions
    REPLY_BUTTON: str = "button:has-text('Trả lời')"
    VIEW_REPLIES_BUTTON: str = "button:has(svg.lucide-message-circle) span"
    DELETE_BUTTON: str = "button:has-text('Xóa')"
    
    # Reply form (appears when clicking reply button on a comment)
    # Use a more flexible selector to match any reply textarea
    REPLY_TEXTAREA: str = "textarea[placeholder*='Trả lời'], textarea[placeholder*='reply'], textarea.reply-input"
    REPLY_SUBMIT_BUTTON: str = "button[type='submit']:has-text('Gửi')"
    
    # Nested replies
    REPLY_CONTAINER: str = "div.mt-4.space-y-3"
    REPLY_ITEM: str = "div.p-4.rounded-md.border-l-3.bg-\\[\\#FAFAFA\\]"
    REPLY_AUTHOR: str = "span.font-medium.text-gray-700.text-sm"
    REPLY_CONTENT: str = "p.mt-1.text-md.text-gray-800"
    REPLY_ARROW_ICON: str = "svg path[d*='M502.6 278.6']"
    REPLY_LEVEL_2: str = "div.bg-\\[\\#FAFAFA\\] p:has-text('Level 2 reply')"
    REPLY_LEVEL_EXIST: str = "text='Level 2 reply'"
    
    # Empty state
    EMPTY_STATE: str = "div.text-center.py-8.text-gray-500"
    EMPTY_STATE_TEXT: str = "p:has-text('Chưa có bình luận nào')"


@dataclass(frozen=True)
class BlockCommentSidebarSelectors:
    """Block comment sidebar (appears when clicking block comment icon) - based on actual HTML."""
    # Sidebar container - scoped to the VISIBLE dialog/drawer (not hidden modals)
    # Use > child selector to get the direct child, avoiding nested matches
    SIDEBAR: str = ".MuiDrawer-root:not(.MuiModal-hidden) > .MuiPaper-root"
    SIDEBAR_INNER: str = ".MuiDrawer-root:not(.MuiModal-hidden) > .MuiPaper-root > .MuiBox-root"
    
    # Header
    COMMENTS_TITLE: str = ".MuiDrawer-root:not(.MuiModal-hidden) h3:has-text('Bình luận')"
    
    # Comment form - scoped to visible drawer
    COMMENT_FORM: str = ".MuiDrawer-root:not(.MuiModal-hidden) div.comment-form form"
    COMMENT_TEXTAREA: str = ".MuiDrawer-root:not(.MuiModal-hidden) textarea[placeholder='Bình luận về block này...']"
    COMMENT_SUBMIT_BUTTON: str = ".MuiDrawer-root:not(.MuiModal-hidden) button[type='submit']:has-text('Gửi')"
    
    # Comments list - scoped to visible drawer
    COMMENTS_LIST: str = ".MuiDrawer-root:not(.MuiModal-hidden) div.comments-list.space-y-6"
    
    # Empty state - scoped to visible drawer
    EMPTY_STATE: str = ".MuiDrawer-root:not(.MuiModal-hidden) div.text-center.py-8.text-gray-500"
    EMPTY_STATE_TEXT: str = ".MuiDrawer-root:not(.MuiModal-hidden) p:has-text('Chưa có bình luận nào')"


@dataclass(frozen=True)
class PostDetailsSelectors:
    """Legacy combined selectors for backward compatibility."""
    # Main content
    POST_CONTAINER: str = PostDetailsContentSelectors.CONTENT_CONTAINER
    POST_TITLE: str = PostDetailsContentSelectors.POST_TITLE
    POST_CONTENT: str = PostDetailsContentSelectors.POST_DESCRIPTION
    AUTHOR_SECTION: str = PostDetailsContentSelectors.AUTHOR_SECTION
    
    # Blocks
    TEXT_BLOCK: str = PostDetailsContentSelectors.TEXT_BLOCK
    IMAGE_BLOCK: str = PostDetailsContentSelectors.IMAGE_BLOCK
    
    # Voting
    UPVOTE_BUTTON: str = PostDetailsSidebarSelectors.UPVOTE_BUTTON
    DOWNVOTE_BUTTON: str = PostDetailsSidebarSelectors.DOWNVOTE_BUTTON
    VOTE_COUNT: str = PostDetailsSidebarSelectors.VOTE_COUNT
    
    # Actions
    SAVE_BUTTON: str = PostDetailsSidebarSelectors.SAVE_BUTTON
    
    # Comments section
    COMMENTS_SECTION: str = PostCommentsSelectors.COMMENTS_SECTION
    COMMENT_INPUT: str = PostCommentsSelectors.COMMENT_TEXTAREA
    SUBMIT_COMMENT_BUTTON: str = PostCommentsSelectors.COMMENT_SUBMIT_BUTTON
    
    COMMENT_ITEM: str = PostCommentsSelectors.COMMENT_ITEM
    COMMENT_AUTHOR: str = PostCommentsSelectors.COMMENT_AUTHOR_NAME
    COMMENT_CONTENT: str = PostCommentsSelectors.COMMENT_CONTENT
    COMMENT_LEVEL_1: str = f"{COMMENT_CONTENT}:has-text('Level 1 comment')"
    COMMENT_TIME: str = PostCommentsSelectors.COMMENT_TIME
    COMMENT_REPLY_BUTTON: str = PostCommentsSelectors.REPLY_BUTTON

    COMMENT_DELETE_BUTTON: str = PostCommentsSelectors.DELETE_BUTTON
    
    # Nested replies
    REPLY_INPUT: str = PostCommentsSelectors.REPLY_TEXTAREA
    REPLY_SUBMIT: str = PostCommentsSelectors.REPLY_SUBMIT_BUTTON
    REPLIES_LIST: str = PostCommentsSelectors.REPLY_CONTAINER


# Export instances
POST_DETAILS_SIDEBAR = PostDetailsSidebarSelectors()
POST_DETAILS_CONTENT = PostDetailsContentSelectors()
POST_COMMENTS = PostCommentsSelectors()
BLOCK_COMMENT_SIDEBAR = BlockCommentSidebarSelectors()
POST_DETAILS = PostDetailsSelectors()