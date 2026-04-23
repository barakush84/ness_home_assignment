"""Page object for the home page of the shopping site.

This module contains the HomePage class used to perform search actions
from the site homepage.
"""

from pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for the home page of the shopping website.

    Handles search functionality on the home page.
    """
    URL = "https://www.ksp.co.il"
    SEARCH_INPUT = "input[id='searchTextBox']"

    def __init__(self, page):
        """Initialize the HomePage with a Playwright page instance.

        Args:
            page: Playwright Page object.
        """
        super().__init__(page)

    def search(self, query):
        """Perform a search query on the home page.

        Args:
            query (str): The search term to enter.
        """
        self.page.fill(self.SEARCH_INPUT, query)
        self.page.press(self.SEARCH_INPUT, "Enter")