"""Page object for product details and add-to-cart behavior.

This module defines the ProductPage class, including pricing, variant
selection, and cart addition logic for a product details page.
"""

import random
from tenacity import retry, stop_after_attempt, wait_random

from pages.base_page import BasePage
from utils.price_utils import parse_price


RETRY_LIMIT = 3

class ProductPage(BasePage):
    """Page object for the product details page.

    Handles price retrieval, variant selection, and add-to-cart interactions.
    """
    # Primary selector - target size selector buttons more specifically
    SIZE_SELECTOR = "[data-type='מידת_נעליים']"
    ADD_TO_CART_BUTTON = "button[data-faro-user-action-name='click-add-to-cart']"
    PRICE_SELECTOR = "div[class*='current-']"

    def __init__(self, page):
        """Initialize the ProductPage with a Playwright page instance.

        Args:
            page: Playwright Page object.
        """
        super().__init__(page)

    @retry(stop=stop_after_attempt(RETRY_LIMIT), wait=wait_random(1, 2))
    def get_price(self):
        """Retrieve the current product price from the page.

        Returns:
            float: Parsed price of the product.
        """
        # Use shorter timeout (5 seconds instead of default 30) to fail fast
        price_text = self.page.locator(self.PRICE_SELECTOR).first.inner_text(timeout=5000)
        price = parse_price(price_text)
        if price == 0.0:
            raise Exception("Price extracted as 0.0, retrying...")
        return price

    def get_available_size_options(self):
        """Return all available size variant locators for the current product.

        Returns:
            list: Playwright locators for available size variants.
        """
        try:
            sizes = self.page.locator(self.SIZE_SELECTOR).all()
            valid_sizes = []

            for size in sizes:
                try:
                    disabled = size.get_attribute("disabled")

                    # ❌ skip out-of-stock
                    if disabled is not None:
                        continue

                    valid_sizes.append(size)

                except Exception as e:
                    self.logger.debug(f"Error checking size: {e}")
                    continue

            self.logger.debug(f"Found {len(valid_sizes)} valid size options")
            return valid_sizes

        except Exception as e:
            self.logger.error(f"Error getting size options: {e}")
            return []

    def is_size_selected(self, size):
        """Check whether a given size option is already selected.

        Args:
            size: Playwright locator for a size option.

        Returns:
            bool: True if the size option is selected, False otherwise.
        """
        class_attr = size.get_attribute("class") or ""
        return "activeTag" in class_attr

    def select_random_variant(self):
        """Select a random unselected size variant if available.

        Returns:
            bool: True when a variant was selected or selection was skipped gracefully, False on error.
        """
        try:
            sizes = self.get_available_size_options()

            if not sizes:
                self.logger.warning("No valid size options available")
                return False

            selected_sizes = []
            unselected_sizes = []

            for size in sizes:
                if self.is_size_selected(size):
                    selected_sizes.append(size)
                else:
                    unselected_sizes.append(size)

            # ✅ Prefer unselected sizes
            if unselected_sizes:
                selected_size = random.choice(unselected_sizes)
                selected_size.click()

                size_text = selected_size.inner_text().strip()
                self.logger.info(f"Selected new size: {size_text}")

                self.page.wait_for_timeout(300)
                return True

            # ⚠️ fallback (should not happen)
            self.logger.info("No unselected sizes available, skipping")
            return True

        except Exception as e:
            self.logger.error(f"Error during variant selection: {e}")
            return False

    @retry(stop=stop_after_attempt(RETRY_LIMIT), wait=wait_random(1, 2))
    def add_to_cart(self):
        """Click the add-to-cart button with retry logic.

        Returns:
            bool: True if the item was added successfully, False otherwise.
        """
        add_btn = self.page.locator(self.ADD_TO_CART_BUTTON)
        if add_btn.count() > 0:
            # Wait for button to be visible (with shorter timeout)
            add_btn.first.wait_for(state='visible', timeout=3000)

            # Check if button is disabled
            is_disabled = add_btn.first.get_attribute("disabled")
            if is_disabled and is_disabled.lower() == "true":
                raise Exception("Add to cart button is disabled, retrying...")

            # Click the button
            add_btn.first.click()
            self.logger.info("Added item to cart")
            self.page.wait_for_timeout(500)
            return True

        self.logger.warning("Add to cart button not found")
        return False
