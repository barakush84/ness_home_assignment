import allure
from allure_commons.types import AttachmentType

from utils.logger import get_logger
logger = get_logger()

class BasePage:
    """Base class for all page objects in the test framework.

    Provides common functionality such as navigation and screenshot saving
    for Playwright-based page objects.
    """

    def __init__(self, page):
        """Initialize the BasePage with a Playwright page instance.

        Args:
            page: Playwright Page object representing the browser page.
        """
        self.page = page
        self.logger = logger

    def navigate(self, force=False):
        """Navigate to the page's URL if not already there, or force navigation.

        Args:
            force (bool): If True, navigate even if already on the page.
        """
        if hasattr(self, 'URL'):
            if self.page.url != self.URL or force:
                self.logger.info(f"Navigating to {self.URL}")
                self.page.goto(self.URL)

    def save_screenshot(self, filename="cart", locator=None):
        """Save a screenshot of the page or a specific locator and attach to Allure.

        Args:
            filename (str): Name for the screenshot attachment.
            locator (str): CSS selector for the element to screenshot; if None, screenshots the whole page.
        """
        try:
            element_to_capture = self.page.locator(locator) if locator else self.page

            allure.attach(element_to_capture.screenshot(), name=filename, attachment_type=AttachmentType.PNG)
            self.logger.info(f"Screenshot captures and save in Allure for: {self.__class__.__name__}")
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {e}")