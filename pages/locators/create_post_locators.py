from dataclasses import dataclass

@dataclass(frozen=True)
class CreatePostButtonSelectors:
    """Buttons to open create post page - based on actual HTML."""
    # Personal post - sidebar button (gradient pink)
    SIDEBAR_CREATE_BUTTON: str = "div.mt-6.mb-4 button:has(span:text('Tạo bài viết'))"
    SIDEBAR_CREATE_BUTTON_ALT: str = "button.bg-gradient-to-r:has(span:text('Tạo bài viết'))"
    
    # Community post button
    COMMUNITY_CREATE_BUTTON: str = "button.btn-outline:has-text('Tạo bài viết')"


@dataclass(frozen=True)
class CreatePostPageSelectors:
    """Create post page selectors - based on actual HTML."""
    # Page container
    PAGE_CONTAINER: str = "div.w-full.relative.p-9"
    
    # Title input (MUI textarea)
    TITLE_INPUT: str = "textarea[placeholder='Nhập tiêu đề bài viết...']"
    TITLE_CONTAINER: str = ".MuiInputBase-root:has(textarea[placeholder='Nhập tiêu đề bài viết...'])"
    
    # Description input
    DESCRIPTION_INPUT: str = "textarea[placeholder='Nhập mô tả ngắn về bài viết...']"
    DESCRIPTION_CONTAINER: str = ".MuiInputBase-root:has(textarea[placeholder='Nhập mô tả ngắn về bài viết...'])"
    
    # Blocks panel (right side)
    BLOCKS_PANEL: str = "div.fixed.right-4:has(p:text('Blocks'))"
    BLOCKS_LABEL: str = "p.text-xs:text('Blocks')"
    
    # Draggable block items
    TEXT_BLOCK_DRAG: str = "div[draggable='true'][title*='Text']"
    IMAGE_BLOCK_DRAG: str = "div[draggable='true'][title*='Image']"
    
    # Block grid layout
    BLOCK_GRID: str = ".react-grid-layout"
    BLOCK_ITEM: str = ".react-grid-item"
    
    # Text block (TipTap editor)
    TEXT_BLOCK: str = "div.text-block"
    TEXT_EDITOR: str = ".tiptap.ProseMirror"
    TEXT_EDITOR_PLACEHOLDER: str = "p[data-placeholder='Viết câu chuyện của bạn...']"
    
    # Image block
    IMAGE_BLOCK: str = "div:has(input[accept='image/*'])"
    IMAGE_UPLOAD_INPUT: str = "input[accept='image/*'][type='file']"
    IMAGE_PLACEHOLDER_ICON: str = "div.w-14.h-14.rounded-full:has(svg)"
    IMAGE_PLACEHOLDER_TEXT: str = "p:text('Kéo thả hoặc nhấn để chọn')"
    IMAGE_SIZE_HINT: str = "p:text('PNG, JPG, GIF. Tối đa 5MB')"
    
    # Next step button
    NEXT_STEP_BUTTON: str = "button:has-text('Bước tiếp theo')"
    NEXT_STEP_BUTTON_ALT: str = "button.btn-default:has-text('Bước tiếp theo')"


@dataclass(frozen=True)
class PostOptionsDialogSelectors:
    """Post options dialog (after clicking Next Step) - based on actual HTML."""
    # Dialog container
    DIALOG: str = ".MuiDialog-paper"
    DIALOG_TITLE: str = ".MuiDialogTitle-root, h2:text('Tùy chỉnh bài viết')"
    
    # Close button
    CLOSE_BUTTON: str = ".MuiDialogTitle-root button:has(svg[data-testid='CloseIcon'])"
    
    # Thumbnail upload
    THUMBNAIL_SECTION: str = "div.mb-4:has(p:text('Ảnh bìa'))"
    THUMBNAIL_LABEL: str = "p:text('Ảnh bìa (Thumbnail)')"
    THUMBNAIL_UPLOAD_INPUT: str = "input#thumbnail-upload[type='file']"
    THUMBNAIL_UPLOAD_AREA: str = "label[for='thumbnail-upload']"
    THUMBNAIL_UPLOAD_TEXT: str = "span:text('Tải ảnh bìa lên')"
    
    # Visibility toggle (Public switch)
    VISIBILITY_SECTION: str = "div.p-3.bg-gray-50:has(.MuiSwitch-root)"
    VISIBILITY_SWITCH: str = ".MuiSwitch-switchBase input[type='checkbox']"
    VISIBILITY_LABEL: str = "p:text('Công khai')"
    VISIBILITY_DESCRIPTION: str = "p:text('Mọi người đều có thể xem bài viết này')"
    
    # Hashtags
    HASHTAGS_SECTION: str = "div.mt-4:has(p:text('Hashtags'))"
    HASHTAGS_LABEL: str = "p:text('Hashtags')"
    HASHTAGS_INPUT: str = "input[placeholder='Nhập hashtag và nhấn Enter']"
    HASHTAGS_HINT: str = "p:text('Thêm hashtag để bài viết dễ tìm kiếm hơn')"
    
    # Dialog actions
    DIALOG_ACTIONS: str = ".MuiDialogActions-root"
    CANCEL_BUTTON: str = "button.btn-outline:has-text('Hủy')"
    PUBLISH_BUTTON: str = "button.btn-default:has-text('Đăng bài')"


@dataclass(frozen=True)
class CreatePostSelectors:
    """Legacy combined selectors for backward compatibility."""
    # Buttons
    CREATE_POST_BUTTON: str = CreatePostButtonSelectors.SIDEBAR_CREATE_BUTTON
    
    # Form inputs
    TITLE_INPUT: str = CreatePostPageSelectors.TITLE_INPUT
    DESCRIPTION_INPUT: str = CreatePostPageSelectors.DESCRIPTION_INPUT
    
    # Editor
    EDITOR: str = CreatePostPageSelectors.TEXT_EDITOR
    
    # Blocks
    TEXT_BLOCK_DRAG: str = CreatePostPageSelectors.TEXT_BLOCK_DRAG
    IMAGE_BLOCK_DRAG: str = CreatePostPageSelectors.IMAGE_BLOCK_DRAG
    
    # Actions
    NEXT_STEP_BUTTON: str = CreatePostPageSelectors.NEXT_STEP_BUTTON
    PUBLISH_BUTTON: str = PostOptionsDialogSelectors.PUBLISH_BUTTON
    CANCEL_BUTTON: str = PostOptionsDialogSelectors.CANCEL_BUTTON
    
    # Hashtags
    HASHTAG_INPUT: str = PostOptionsDialogSelectors.HASHTAGS_INPUT


# Export instances
CREATE_POST_BUTTONS = CreatePostButtonSelectors()
CREATE_POST_PAGE = CreatePostPageSelectors()
POST_OPTIONS_DIALOG = PostOptionsDialogSelectors()
CREATE_POST = CreatePostSelectors()