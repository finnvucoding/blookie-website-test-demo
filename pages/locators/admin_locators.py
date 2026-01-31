from dataclasses import dataclass
@dataclass(frozen=True)
class AdminDashboardSelectors:
    """Admin Dashboard page selectors - /admin/dashboard"""

    # Title section
    PAGE_TITLE: str = "h1.text-2xl.font-bold.text-gray-800"
    
    # Period filter buttons
    TODAY_BUTTON: str = "button:has-text('Hôm nay')"
    WEEK_BUTTON: str = "button:has-text('7 ngày qua')"
    MONTH_BUTTON: str = "button:has-text('30 ngày qua')"

@dataclass(frozen=True)
class AdminUsersSelectors:
    """Admin Users Management page selectors - /admin/users/list"""

    # Header
    PAGE_TITLE: str = "h1.text-2xl.font-bold"
    
    # Search and filters
    SEARCH_INPUT: str = "input[placeholder*='Tìm theo tên, email, ID']"
    
    # Users table
    TABLE_BODY: str = "tbody.MuiTableBody-root"
    USER_ROW: str = "tr.MuiTableRow-root"
    
    # Table cells
    CELL_ID: str = "td:nth-child(1)"
    CELL_USERNAME: str = "td:nth-child(2)"
    CELL_EMAIL: str = "td:nth-child(3)"
    CELL_ROLE: str = "td:nth-child(4)"
    CELL_STATUS: str = "td:nth-child(5)"
    CELL_ACTIONS: str = "td:nth-child(6)"
    
    # Action buttons in table row
    VIEW_USER_BUTTON: str = "button:has(svg[viewBox='0 0 576 512'])"  # Eye icon
    EDIT_USER_BUTTON: str = "button:has(svg path[d*='M402.6'])"  # Pencil icon
    LOCK_USER_BUTTON: str = "button:has(svg path[d*='M80 192V144'])"  # Lock icon
    DELETE_USER_BUTTON: str = "button:has(svg path[d*='M135.2'])"  # Trash icon
    
    # Status badges
    STATUS_ACTIVE: str = "span.bg-green-100.text-green-600"
    STATUS_BANNED: str = "span.bg-red-100.text-red-600"
    
    # Role badges
    ROLE_USER: str = "span.bg-blue-50.text-blue-600"
    ROLE_ADMIN: str = "span.bg-purple-50.text-purple-600"
    
    # Pagination
    PAGINATION_CONTAINER: str = "nav[aria-label='pagination navigation']"
    PAGINATION_PREV: str = "button[aria-label='Go to previous page']"
    PAGINATION_NEXT: str = "button[aria-label='Go to next page']"


@dataclass(frozen=True)
class AdminUserDialogSelectors:
    """Admin User Dialog selectors (View, Edit, Lock, Delete)"""
    # Common dialog
    DIALOG: str = "div.MuiDialog-paper[role='dialog']"
    DIALOG_TITLE: str = "h2.MuiDialogTitle-root"
    DIALOG_CONTENT: str = "div.MuiDialogContent-root"
    DIALOG_ACTIONS: str = "div.MuiDialogActions-root"
    
    # View User Dialog
    VIEW_DIALOG_TITLE: str = "h2:has-text('Thông tin chi tiết người dùng')"
    VIEW_FIELD_LABEL: str = "label.text-sm.font-semibold.text-gray-600"
    VIEW_FIELD_VALUE: str = "div.px-4.py-3.bg-\\[\\#FAF5F7\\] p"
    VIEW_BACK_BUTTON: str = "button:has-text('Quay về')"
    
    # Edit User Dialog
    EDIT_DIALOG_TITLE: str = "h2:has-text('Chỉnh sửa thông tin người dùng')"
    EDIT_USERNAME_INPUT: str = "input[placeholder='Nhập username']"
    EDIT_EMAIL_INPUT: str = "input[type='email'][placeholder='Nhập email']"
    EDIT_PHONE_INPUT: str = "input[type='tel'][placeholder='Nhập số điện thoại']"
    EDIT_ROLE_SELECT: str = "select"
    EDIT_ROLE_USER_OPTION: str = "option[value='USER']"
    EDIT_ROLE_ADMIN_OPTION: str = "option[value='ADMIN']"
    EDIT_CANCEL_BUTTON: str = "button.MuiButton-text:has-text('Hủy')"
    EDIT_SAVE_BUTTON: str = "button.MuiButton-contained:has-text('Lưu thay đổi')"
    
    # Lock User Dialog
    LOCK_DIALOG_TITLE: str = "h2:has-text('Khóa tài khoản')"
    LOCK_WARNING_TEXT: str = "p.text-sm.text-gray-600"
    LOCK_CANCEL_BUTTON: str = "button.MuiButton-text:has-text('Hủy')"
    LOCK_CONFIRM_BUTTON: str = "button.MuiButton-contained:has-text('Xác nhận khóa')"
    
    # Delete User Dialog
    DELETE_DIALOG_TITLE: str = "h2:has-text('Xác nhận xóa')"
    DELETE_WARNING_TEXT: str = "p.text-sm.text-gray-700"
    DELETE_NOTICE_TEXT: str = "p.text-sm.text-gray-500"
    DELETE_CANCEL_BUTTON: str = "button.MuiButton-text:has-text('Hủy')"
    DELETE_CONFIRM_BUTTON: str = "button.MuiButton-containedError:has-text('Xác nhận')"


@dataclass(frozen=True)
class AdminPostsSelectors:
    """Admin Posts Management page selectors - /admin/posts/list"""
    
    # Header
    PAGE_TITLE: str = "h1.text-4xl.text-\\[\\#6E344D\\]"
    PAGE_DESCRIPTION: str = "p.font-body.text-gray-500"
    REFRESH_BUTTON: str = "button:has-text('Làm mới')"
    
    # Stats cards
    STATS_CONTAINER: str = "div.grid.grid-cols-3.gap-4"
    TOTAL_POSTS_CARD: str = "div.bg-blue-50.border-blue-200"
    TOTAL_POSTS_VALUE: str = "div.bg-blue-50 p.text-blue-700.text-3xl"
    ACTIVE_POSTS_CARD: str = "div.bg-emerald-50.border-emerald-200"
    ACTIVE_POSTS_VALUE: str = "div.bg-emerald-50 p.text-emerald-700.text-3xl"
    HIDDEN_POSTS_CARD: str = "div.bg-slate-50.border-slate-200"
    HIDDEN_POSTS_VALUE: str = "div.bg-slate-50 p.text-slate-700.text-3xl"
    
    # Search and filters
    SEARCH_INPUT: str = "input[placeholder*='Tìm theo tiêu đề, tác giả']"
    STATUS_FILTER_SELECT: str = "select"
    STATUS_ALL_OPTION: str = "option[value='ALL']"
    STATUS_ACTIVE_OPTION: str = "option[value='ACTIVE']"
    STATUS_HIDDEN_OPTION: str = "option[value='HIDDEN']"
    
    # Posts table
    POSTS_TABLE: str = "table.MuiTable-root"
    TABLE_HEAD: str = "thead.MuiTableHead-root"
    TABLE_BODY: str = "tbody.MuiTableBody-root"
    POST_ROW: str = "tr.MuiTableRow-root"
            
    # Status badges
    STATUS_ACTIVE_BADGE: str = "span:has-text('ACTIVE')"
    STATUS_HIDDEN_BADGE: str = "span:has-text('HIDDEN')"
    
    # Action buttons - Toggle visibility (eye icons)
    TOGGLE_VISIBILITY_BUTTON: str = "button.MuiBox-root"
    # Icon for HIDE action (eye with slash - currently visible, click to hide)
    HIDE_POST_ICON: str = "svg path[d*='M12 7c2.76']"
    # Icon for SHOW action (open eye - currently hidden, click to show)
    SHOW_POST_ICON: str = "svg path[d*='M12 4.5C7']"
    
    # View reports button
    VIEW_REPORTS_BUTTON: str = "div[title='Xem chi tiết báo cáo']"
    
    # Pagination
    PAGINATION_CONTAINER: str = "div.flex.justify-center.items-center.gap-2"
    PAGINATION_INFO: str = "p.text-gray-600"
    FIRST_PAGE_BUTTON: str = "button[title='Về trang đầu']"
    PREV_PAGE_BUTTON: str = "button[title='Trang trước']"
    NEXT_PAGE_BUTTON: str = "button[title='Trang sau']"
    LAST_PAGE_BUTTON: str = "button[title='Đến trang cuối']"
    ACTIVE_PAGE_BUTTON: str = "button.bg-\\[\\#F295B6\\].text-white"
    PAGE_NUMBER_BUTTON: str = "button.px-4.py-2.rounded-lg"


@dataclass(frozen=True)
class AdminReportsSelectors:
    """Admin Reports Management page selectors - /admin/reports"""
    
    # Page title
    PAGE_TITLE: str = "h1:has-text('Quản lý Báo Cáo'), h1:has-text('Báo cáo')"
    
    # Reports table
    REPORTS_TABLE: str = "table.MuiTable-root"
    

@dataclass(frozen=True)
class AdminSidebarSelectors:
    """Admin Sidebar navigation selectors"""
    # Sidebar container
    SIDEBAR: str = "aside, nav.admin-sidebar, div[class*='sidebar']"
    
    # Navigation links
    DASHBOARD_LINK: str = "a[href='/admin/dashboard'], a:has-text('Dashboard'), a:has-text('Thống kê')"
    USERS_LINK: str = "a[href*='/admin/users'], a:has-text('Người dùng'), a:has-text('Quản lý người dùng')"
    POSTS_LINK: str = "a[href*='/admin/posts'], a:has-text('Bài đăng'), a:has-text('Quản lý bài đăng')"
    REPORTS_LINK: str = "a[href*='/admin/reports'], a:has-text('Báo cáo'), a:has-text('Quản lý báo cáo')"
    
    # Active link indicator
    ACTIVE_LINK: str = "a.active, a[aria-current='page'], a.bg-\\[\\#F295B6\\]"

# ============================================
# EXPORT ALL ADMIN LOCATORS
# ============================================

ADMIN_DASHBOARD = AdminDashboardSelectors()
ADMIN_USERS = AdminUsersSelectors()
ADMIN_USER_DIALOG = AdminUserDialogSelectors()
ADMIN_POSTS = AdminPostsSelectors()
ADMIN_REPORTS = AdminReportsSelectors()
ADMIN_SIDEBAR = AdminSidebarSelectors()
