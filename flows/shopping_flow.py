from pages.home_page import HomePage
from pages.cart_page import CartPage
from pages.overlay_page import OverlayPage
from pages.product_page import ProductPage
from pages.search_results_page import SearchResultsPage

from utils.logger import get_logger
logger = get_logger()


class ShoppingFlow:
    """Orchestrates the end-to-end shopping flow for the test framework.

    Handles searching for products, adding them to cart, and verifying cart contents.
    """

    def __init__(self, page):
        """Initialize the ShoppingFlow with a Playwright page and page objects.

        Args:
            page: Playwright Page object.
        """
        self.page = page
        self.home = HomePage(page)
        self.results = SearchResultsPage(page)
        self.cart = CartPage(page)
        self.overlay = OverlayPage(page)
        self.product = ProductPage(page)

    def search_items_by_name_under_price(self, query, max_price, limit=5):
        """Search for items by name under the specified max price and return their URLs.

        Args:
            query (str): Search term.
            max_price (float): Maximum price per item.
            limit (int): Maximum number of URLs to return.

        Returns:
            list: List of product URLs.
        """
        logger.info(f"Starting search for '{query}' with max_price={max_price}, limit={limit}")

        self.home.navigate()
        self.home.search(query)

        self.results.wait_for_results()

        urls = self.results.get_product_urls(max_price, limit)

        logger.info(f"Search completed. Found and extracted {len(urls)} product URLs")
        return urls

    def add_items_to_cart(self, urls):
        """Add items from the provided URLs to the cart and return the total price.

        Args:
            urls (list): List of product URLs to add.

        Returns:
            float: Total price of added items.
        """
        logger.info(f"Starting to add {len(urls)} items to cart")

        total_price = 0.0

        for index, url in enumerate(urls, 1):
            try:
                logger.info(f"Processing item {index}/{len(urls)}: {url}")

                # Navigate to product page
                self.page.goto(url)
                self.page.wait_for_load_state('load')

                price = self.product.get_price()

                # Select random variants
                self.product.select_random_variant()

                # Add to cart
                if self.product.add_to_cart():
                    logger.info(f"Successfully added item {index} to cart")

                    self.page.wait_for_load_state('load')

                    total_price += price
                    logger.info(f"Item price: {price}, Running total: {total_price}")

                    # Take screenshot
                    self.product.save_screenshot(f"item_{index}")

                    # Handle overlay
                    self.overlay.continue_shopping()
                else:
                    logger.warning(f"Failed to add item {index} to cart, skipping continue_shopping")

            except Exception as e:
                logger.error(f"Error processing item {index}: {e}")
                continue

        logger.info(f"Finished adding items to cart. Total price: {total_price}")
        return total_price

    def assert_cart_total_not_exceeds(self, budget_per_item, items_count):
        """Assert that the cart total does not exceed the budget.

        Args:
            budget_per_item (float): Maximum price per item.
            items_count (int): Number of items in cart.
        """
        logger.info(f"Verifying cart total: budget_per_item={budget_per_item}, items_count={items_count}")

        self.cart.navigate()
        total = self.cart.get_total()

        expected = budget_per_item * items_count
        logger.info(f"Cart total: {total}, Expected max: {expected}")

        assert total <= expected, f"Cart total {total} exceeds budget {expected}"
        logger.info("Cart total is within budget")

    def assert_cart_total_equal_to_total(self, budget_per_item, items_count, total_price):
        """Assert that the cart total matches the expected total price.

        Args:
            budget_per_item (float): Maximum price per item.
            items_count (int): Number of items.
            total_price (float): Expected total price.
        """
        logger.info(f"Verifying cart total: budget_per_item={budget_per_item}, items_count={items_count}, expected_total={total_price}")

        self.cart.navigate()
        total = self.cart.get_total()

        expected = budget_per_item * items_count
        logger.info(f"Cart total: {total}, Expected total: {total_price}, Expected max: {expected}")

        assert total == total_price, f"Cart total {total} does not match expected total {total_price}"
        logger.info("Cart total matches expected total")

    def assert_cart_items_count(self, expected_count):
        """Assert that the number of items in the cart matches the expected count.

        Args:
            expected_count (int): Expected number of items.
        """
        logger.info(f"Verifying cart items count: {expected_count}")

        self.cart.navigate()
        count = self.cart.get_items_count()

        logger.info(f"Items in cart: {count}, Expected: {expected_count}")

        assert count == expected_count, f"Expected {expected_count} items in cart, but found {count}"
        logger.info(f"Cart contains expected {expected_count} items")
