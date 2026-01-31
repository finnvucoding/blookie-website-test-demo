from enum import Enum
from playwright.sync_api import Browser, BrowserContext, Page
from core.logger import log
from config.settings import settings

logger = log()
class BrowserType(Enum):
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"

class BrowserFactory:
    @staticmethod
    def create_context(browser: Browser, **kwargs) -> BrowserContext:
        """
        Tạo Browser Context với cấu hình chuẩn từ Settings.
        Args:
            browser: Instance browser đã được Pytest khởi tạo.
            **kwargs: Các override options nếu cần.
        """
        # 1. Lấy config mặc định từ settings.py
        default_options = {
            "viewport": settings.browser.VIEWPORT,
            "locale": settings.browser.LOCALE,
            # Video & Trace quay lại khi lỗi
            "record_video_dir": "logs/videos/" if settings.browser.RECORD_VIDEO else None,
        }
        
        # 2. Merge với kwargs (ưu tiên kwargs)
        context_options = {**default_options, **kwargs}
        
        logger.info(f"Creating Browser Context with options: {context_options}")
        
        # 3. Tạo context
        context = browser.new_context(**context_options)
        
        # 4. Set default timeout
        context.set_default_timeout(settings.timeouts.DEFAULT)
        
        return context

    @staticmethod
    def create_page(browser: Browser, **kwargs) -> Page:
        """Helper nhanh để tạo Page (gồm cả Context)"""
        context = BrowserFactory.create_context(browser, **kwargs)
        return context.new_page()