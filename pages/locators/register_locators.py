from dataclasses import dataclass # xong

@dataclass(frozen=True)
class RegisterPageSelectors:
    """
    Locators for Registration Page - UPDATED based on actual HTML.
    Fields: Name, Email, Password, Confirm Password
    """
    # Form inputs
    FULLNAME_INPUT: str = "input[autocomplete='name']"
    EMAIL_INPUT: str = "input[type='email'][autocomplete='email']"
    PASSWORD_INPUT: str = "input[autocomplete='new-password']:first-of-type"
    CONFIRM_PASSWORD_INPUT: str = "input[autocomplete='new-password']:last-of-type"
    
    # Alternative: By placeholder
    PASSWORD_BY_PLACEHOLDER: str = "input[placeholder*='Tối thiểu 8 ký tự, có chữ hoa, thường và số']"
    CONFIRM_PASSWORD_BY_PLACEHOLDER: str = "input[placeholder='Nhập lại mật khẩu']"
    
    # Buttons
    REGISTER_BUTTON: str = "button[type='submit']:has-text('Đăng ký')"
    LOGIN_LINK: str = "a[href='/login']"
    
    # Form container
    FORM: str = "form"
    TITLE: str = "h2:has-text('ĐĂNG KÝ')"

REGISTER_PAGE = RegisterPageSelectors()