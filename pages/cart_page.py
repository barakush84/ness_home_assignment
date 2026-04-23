import re
from pages.base_page import BasePage
from utils.price_utils import parse_price


class CartPage(BasePage):

    URL = "https://ksp.co.il/cart/"
    TOTAL_PRICE_LOCATOR = "div[id='totalPriceInFinishOrder']"
    ITEMS_COUNT_LOCATOR = "span[class='text']"


    def __init__(self, page):
        super().__init__(page)

    def get_total(self):
        total_text = self.page.locator(self.TOTAL_PRICE_LOCATOR).inner_text().split('\n')[1]
        return parse_price(total_text)

    def get_items_count(self):
        text = self.page.locator(self.ITEMS_COUNT_LOCATOR).inner_text()
        numbers = re.findall(r"\d+", text)
        return int(numbers[0]) if numbers else 0