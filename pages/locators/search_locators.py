from dataclasses import dataclass # xong

@dataclass(frozen=True)
class SearchSelectors:
    """Search page selectors."""
    SEARCH_INPUT: str = "input[placeholder='Tìm kiếm...']"
    # SEARCH_INPUT: str = "div:has(button > svg) > input"
    # SEARCH_INPUT: str = "div:has(button[aria-label='Search']) > input"
    
    SEARCH_BUTTON: str = "button[aria-label='Search']"
    
    SUGGESTIONS_DROPDOWN: str = "div.absolute.top-full"
    
    SUGGEST_POST_BTN: str = f"{SUGGESTIONS_DROPDOWN} button:has-text('Bài viết có chứa')"
    SUGGEST_USER_BTN: str = f"{SUGGESTIONS_DROPDOWN} button:has-text('Người dùng tên')"
    SUGGEST_COMMUNITY_BTN: str = f"{SUGGESTIONS_DROPDOWN} button:has-text('Cộng đồng')"
    SUGGEST_HASHTAG_BTN: str = f"{SUGGESTIONS_DROPDOWN} button:has-text('Hashtag')"
    
    # Empty State (Khi không có kết quả)
    # Tìm thẻ P có text chính xác
    NO_RESULTS_MESSAGE: str = "p:has-text('Không tìm thấy kết quả nào.')"
    

SEARCH = SearchSelectors()