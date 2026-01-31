from dataclasses import dataclass

@dataclass(frozen=True)
class CommunitySelectors:
    """
    Community pages selectors based on actual HTML structure (Tailwind CSS).
    """
    # 1. Sidebar Navigation
    SIDEBAR_COMMUNITIES_LINK: str = "a[href='/me/my-communities']"

    # 2. My Communities Page (List Page)
    HEADER_TITLE: str = "h1.saved-posts-header__title" # "Cộng đồng của bạn"
    CREATE_COMMUNITY_BTN: str = "button.community-save-btn:has-text('Tạo cộng đồng mới')"
    
    # List & Cards
    COMMUNITY_LIST_CONTAINER: str = "div.space-y-6"
    
    # Một card cộng đồng (thẻ button)
    COMMUNITY_CARD: str = "button.bg-white.text-gray-900"
    
    # Các element bên trong Card (dùng relative locator)
    CARD_NAME: str = "div.text-2xl.font-bold"
    CARD_DESC: str = "div.text-sm.text-gray-600.line-clamp-2"
    CARD_ROLE_BADGE: str = "span.rounded-full" # Chứa text 'Admin', 'Member'
    
    # 3. Community Detail Page
    # Header Info
    DETAIL_TITLE: str = "h1.community-title"
    DETAIL_DESC: str = "p.community-sub"
    MEMBER_COUNT_BADGE: str = "div[title*='thành viên']"
    
    # Actions (Header)
    MANAGE_BTN: str = "button.btn-manage"
    LEAVE_BTN: str = "button.btn:has-text('Rời cộng đồng')"
    JOIN_BTN: str = "button.btn:has-text('Tham gia')" # Giả định (dựa trên pattern btn)
    
    # Tabs Navigation
    TAB_POSTS: str = "nav.community-tabs-nav a:has-text('Bài viết')"
    TAB_MEMBERS: str = "nav.community-tabs-nav a:has-text('Thành viên')"
    
    # Content Area
    # Nút tạo bài viết (nằm trong tab bài viết)
    CREATE_POST_BTN: str = "button.btn-outline:has-text('Tạo bài viết')"
    
    # Empty State (khi chưa có bài viết)
    EMPTY_POSTS_MSG: str = "div.community-card:has-text('Chưa có bài viết nào')"

COMMUNITY = CommunitySelectors()