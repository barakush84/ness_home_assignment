from pages.base_page import BasePage


class OverlayPage(BasePage):
    """Page object for overlay dialogs that appear after adding items to the cart.

    Handles interactions with the overlay, such as continuing shopping or going to cart.
    """

    CONTINUE_SHOPPING_BUTTON = "[data-faro-user-action-name='click-continue-shopping']"
    GO_TO_CART_BUTTON = "[data-faro-user-action-name='click-go-to-cart']"
    PRICE_SELECTOR = "p[class*='price-']"

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

    def go_to_cart(self):
        """Click the goto cart button on the overlay."""
        self.wait_for_overlay()
        self.page.locator(self.GO_TO_CART_BUTTON).click()
