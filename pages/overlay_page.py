"""Page object for overlay dialogs on the shopping site.

This module provides the OverlayPage class used to interact with the
confirmation overlay displayed after adding items to the cart.
"""

from pages.base_page import BasePage


class OverlayPage(BasePage):
    """Page object for overlay dialogs that appear after adding items to the cart.

    Handles interactions with the overlay, such as continuing shopping or going to cart.
    """

    CONTINUE_SHOPPING_BUTTON = "[data-faro-user-action-name='click-continue-shopping']"

    def __init__(self, page):
        """Initialize the OverlayPage with a Playwright page instance.

        Args:
            page: Playwright Page object.
        """
        super().__init__(page)

    def wait_for_overlay(self):
        """Wait for the overlay dialog to appear."""
        self.page.wait_for_selector(self.CONTINUE_SHOPPING_BUTTON, timeout=5000)

    def continue_shopping(self):
        """Click the continue shopping button on the overlay."""
        self.wait_for_overlay()
        self.page.locator(self.CONTINUE_SHOPPING_BUTTON).click()
