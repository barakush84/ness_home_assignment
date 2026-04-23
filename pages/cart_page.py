"""Page object for shopping cart page interactions.

This module defines the CartPage class used to read cart totals and item
counts from the shopping cart page.
"""

import re
from pages.base_page import BasePage
from utils.price_utils import parse_price


class CartPage(BasePage):
    """Page object for the shopping cart page.

    Handles retrieval of the cart total and item counts.
    """

    URL = "https://ksp.co.il/cart/"
    TOTAL_PRICE_LOCATOR = "div[id='totalPriceInFinishOrder']"
    ITEMS_COUNT_LOCATOR = "span[class='text']"


    def __init__(self, page):
        """Initialize the CartPage with a Playwright page instance.

        Args:
            page: Playwright Page object.
        """
        super().__init__(page)

    def get_total(self):
        """Return the total price from the cart page.

        Returns:
            float: Parsed cart total price.
        """
        total_text = self.page.locator(self.TOTAL_PRICE_LOCATOR).inner_text().split('\n')[1]
        return parse_price(total_text)

    def get_items_count(self):
        """Return the number of items currently in the cart.

        Returns:
            int: Count of cart items.
        """
        text = self.page.locator(self.ITEMS_COUNT_LOCATOR).inner_text()
        numbers = re.findall(r"\d+", text)
        return int(numbers[0]) if numbers else 0