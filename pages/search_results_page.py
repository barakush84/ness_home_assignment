"""Page object for search results and product listing interactions.

This module defines the SearchResultsPage class used to handle search result
locators, pagination, and product URL extraction.
"""

from pages.base_page import BasePage
from utils.price_utils import parse_price


class SearchResultsPage(BasePage):
    """Page object for the search results page of the shopping website.

    Handles waiting for results, extracting product information, and pagination.
    """
    BASE_URL = "https://ksp.co.il"
    PRODUCT_LINK_SELECTOR = "div[class*='product-']"
    PRICE_SELECTOR = "div[class*='currentPrice']"
    NEXT_PAGE_BUTTON = "a[aria-label*='next'], button[aria-label*='next'], a:has-text('Next'), button:has-text('Next')"

    def __init__(self, page):
        """Initialize the SearchResultsPage with a Playwright page instance.

        Args:
            page: Playwright Page object.
        """
        super().__init__(page)

    def wait_for_results(self):
        """Wait for search results to load on the page."""
        self.page.wait_for_selector(self.PRODUCT_LINK_SELECTOR, timeout=10000)

    def get_items(self):
        """Get all product item locators on the page.

        Returns:
            Locator: Playwright locator for product items.
        """
        return self.page.locator(self.PRODUCT_LINK_SELECTOR)

    def get_price(self, container):
        """Extract the price text from a product container.

        Args:
            container: Playwright locator for the product container.

        Returns:
            str: The price text.
        """
        return container.locator(self.PRICE_SELECTOR).first.inner_text()

    def get_items_under_price(self, max_price):
        """Get a list of product containers for items under the specified max price.

        Args:
            max_price (float): Maximum price threshold.

        Returns:
            list: List of product container locators under max_price.
        """
        items_under_price = []
        items = self.get_items()
        count = items.count()
        
        for i in range(count):
            try:
                item = items.nth(i)
                price_text = self.get_price(item)
                price = parse_price(price_text)
                
                if price <= max_price:
                    items_under_price.append(item)
                    self.logger.debug(f"Found item under price: {price} <= {max_price}")
            except Exception as e:
                self.logger.warning(f"Error processing item {i}: {e}")
                continue
        
        self.logger.info(f"Found {len(items_under_price)} items under max price {max_price}")
        return items_under_price

    def get_product_url(self, container):
        """Extract the product URL from a product container.

        Args:
            container: Playwright locator for the product container.

        Returns:
            str or None: The full product URL, or None if extraction fails.
        """
        try:
            link = container.locator("a").first
            url = link.get_attribute("href")
            
            if url:
                if url.startswith("http"):
                    return url
                elif url.startswith("/"):
                    return self.BASE_URL + url
                else:
                    return self.BASE_URL + "/" + url
            return None
        except Exception as e:
            self.logger.warning(f"Failed to extract URL from item: {e}")
            return None

    def get_product_urls(self, max_price, limit=5):
        """Extract up to limit product URLs for items under max_price, paginating if needed.

        Args:
            max_price (float): Maximum price per item.
            limit (int): Maximum number of URLs to extract.

        Returns:
            list: List of product URLs.
        """
        urls = []
        
        while len(urls) < limit:
            items_under_price = self.get_items_under_price(max_price)
            
            for item in items_under_price:
                if len(urls) >= limit:
                    break
                
                url = self.get_product_url(item)
                if url and url not in urls:
                    urls.append(url)
                    self.logger.info(f"Extracted URL {len(urls)}/{limit}: {url}")
            
            if len(urls) >= limit:
                self.logger.info(f"Reached limit of {limit} URLs")
                break
            
            if self.has_next_page():
                self.logger.info("Going to next page to find more items")
                self.go_to_next_page()
                self.wait_for_results()
            else:
                self.logger.info("No more pages available")
                break
        
        self.logger.info(f"Total URLs extracted: {len(urls)}")
        return urls

    def has_next_page(self):
        """Check if there is an enabled next page button.

        Returns:
            bool: True if next page is available, False otherwise.
        """
        try:
            next_btn = self.page.locator(self.NEXT_PAGE_BUTTON)
            if next_btn.count() > 0:
                is_disabled = next_btn.first.get_attribute("disabled")
                is_enabled = (is_disabled is None or is_disabled == "false")
                self.logger.debug(f"Next page button found, enabled: {is_enabled}")
                return is_enabled
            self.logger.debug("Next page button not found")
            return False
        except Exception as e:
            self.logger.warning(f"Error checking for next page: {e}")
            return False

    def go_to_next_page(self):
        """Click the next page button to navigate to the next page.

        Returns:
            bool: True if clicked successfully, False otherwise.
        """
        try:
            next_btn = self.page.locator(self.NEXT_PAGE_BUTTON)
            if next_btn.count() > 0:
                next_btn.first.click()
                self.logger.info("Clicked next page button")
                self.page.wait_for_timeout(1000)
                return True
            else:
                self.logger.warning("Next page button not found")
                return False
        except Exception as e:
            self.logger.error(f"Error clicking next page: {e}")
            return False
