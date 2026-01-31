from dataclasses import dataclass


@dataclass(frozen=True)
class LoginPageSelectors:
    # Form inputs
    EMAIL_INPUT: str = "input[autocomplete='username']"  # Accepts email OR username
    PASSWORD_INPUT: str = "input[type='password'][autocomplete='current-password']"
    
    # Buttons
    LOGIN_BUTTON: str = "button[type='submit']:has-text('Đăng nhập')"
    REGISTER_LINK: str = "a[href='/register']"
    FORGOT_PASSWORD_LINK: str = "a[href='/forgot-password']"
    VERIFY_EMAIL_LINK: str = "a[href='/verify-email']"
    
    # Form container
    FORM: str = "form"
    TITLE: str = "h2:has-text('ĐĂNG NHẬP')"
    
    # Toast notifications (error/success) - based on actual HTML
    ERROR_MESSAGE: str = "div[class*='bg-[#FEF2F2]'] p"

    BELL_ICON: str = "span.MuiBadge-root button" 

LOGIN_PAGE = LoginPageSelectors()