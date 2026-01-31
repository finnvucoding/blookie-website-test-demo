from dataclasses import dataclass # xong

@dataclass(frozen=True)
class ProfileSelectors:
    # 1. Navigation to Profile (Từ Header/Avatar)
    # Avatar button trên header (thường góc phải)
    HEADER_AVATAR_BTN: str = "button:has(.MuiAvatar-root)"
    # Menu item trong dropdown
    VIEW_PROFILE_MENU_ITEM: str = "li[role='menuitem']:has-text('Xem trang cá nhân')"

    # 2. Profile Header Info
    # Tên hiển thị (H1 to và đậm)
    DISPLAY_NAME: str = "h1.text-3xl.font-bold"
    
    # Email (Tìm div chứa icon mail hoặc text pattern email)
    # Strategy: Tìm text chứa @ trong phần header
    EMAIL: str = "div.profile-card-header div.text-gray-500:has-text('@')"
    
    # Avatar Lớn trong trang Profile
    PROFILE_AVATAR: str = "div.profile-card-header .MuiAvatar-root"
    
    # Ảnh bìa (Cover Image) - Div có chiều cao cố định
    COVER_IMAGE_CONTAINER: str = "div.profile-card-header div.h-\[200px\]"

    # 3. Stats (Thống kê)
    # Tìm theo label text để xác định đúng số liệu
    # Cấu trúc: div (cha) -> div (value) + div (label)
    # Locator: Tìm div cha mà có con là div chứa text "Người theo dõi"
    STAT_FOLLOWERS: str = "div.flex.gap-6 div:has(div.profile-stat-label:has-text('Người theo dõi')) .profile-stat-value"
    STAT_FOLLOWING: str = "div.flex.gap-6 div:has(div.profile-stat-label:has-text('Đang theo dõi')) .profile-stat-value"
    
    # 4. Tabs Navigation
    TAB_POSTS: str = "button.profile-tab-nav-item:has-text('Bài viết')"
    TAB_COMMUNITIES: str = "button.profile-tab-nav-item:has-text('Cộng đồng')"
    # Class active để check tab nào đang chọn
    TAB_ACTIVE_CLASS: str = "profile-tab-nav-item-active"

    # 5. Content List
    # Container chứa danh sách
    TAB_CONTENT: str = "div.profile-tab-content"
    
    # Card bài viết trong profile (tái sử dụng cấu trúc newsfeed card)
    POST_CARD: str = "article.newsfeed-card"
    
    # Tiêu đề bài viết đầu tiên (để verify content)
    FIRST_POST_TITLE: str = f"{TAB_CONTENT} {POST_CARD} h2.newsfeed-card__title >> nth=0"

PROFILE = ProfileSelectors()