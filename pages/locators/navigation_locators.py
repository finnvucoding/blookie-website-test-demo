from dataclasses import dataclass

@dataclass(frozen=True)
class SidebarSelectors:
    """Left sidebar navigation selectors - based on actual HTML."""
    # Sidebar container
    SIDEBAR: str = "div.sticky.w-\\[240px\\].h-screen.bg-\\[\\#FAF5F7\\]"
    SIDEBAR_CONTAINER: str = "div.sticky.top-0"
    
    # Logo
    LOGO: str = "img[alt='Blookie Logo']"
    LOGO_CONTAINER: str = "div.text-3xl.font-bold"
    
    # Close sidebar button (X icon)
    CLOSE_SIDEBAR_BUTTON: str = "button:has(svg path[d='M6 18L18 6M6 6l12 12'])"
    
    # Open sidebar button (hamburger menu - when sidebar is closed)
    OPEN_SIDEBAR_BUTTON: str = "button:has(svg path[fill-rule='evenodd'][d*='M3 5a1 1 0 011-1h12'])"
    
    # Create post button (gradient pink button)
    CREATE_POST_BUTTON: str = "button:has(span:text('Tạo bài viết'))"
    CREATE_POST_BUTTON_ALT: str = "div.mt-6.mb-4 button.bg-gradient-to-r"
    
    # Navigation links
    NAV_CONTAINER: str = "nav.mt-4"
    NAV_LIST: str = "nav ul.space-y-1"
    NAV_ITEM: str = "nav ul li"
    
    # Specific nav links
    HOME_LINK: str = "a[href='/']"
    SAVED_LINK: str = "a[href='/saved']"
    COMMUNITIES_LINK: str = "a[href='/me/my-communities']"
    
    # Nav link text
    HOME_TEXT: str = "a[href='/'] div:text('Trang chủ')"
    SAVED_TEXT: str = "a[href='/saved'] div:text('Đã lưu')"
    COMMUNITIES_TEXT: str = "a[href='/me/my-communities'] div:text('Nhóm')"


@dataclass(frozen=True)
class NavigationSelectors:
    """Main navigation/header selectors - based on actual HTML."""
    # Use sidebar selectors
    SIDEBAR: str = SidebarSelectors.SIDEBAR
    HOME_LINK: str = "a[href='/']"
    SAVED_POSTS_LINK: str = "a[href='/saved']"
    COMMUNITIES_LINK: str = "a[href='/me/my-communities']"
    
    # Open/close sidebar
    TOGGLE_SIDEBAR_BUTTON: str = "button:has(svg[viewBox='0 0 20 20'])"
    CLOSE_SIDEBAR_BUTTON: str = "button:has(svg path[d='M6 18L18 6M6 6l12 12'])"
    
    # Create post
    CREATE_POST_BUTTON: str = "button:has(span:text('Tạo bài viết'))"


# Export instances
SIDEBAR = SidebarSelectors()
NAVIGATION = NavigationSelectors()