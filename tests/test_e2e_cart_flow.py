import allure
from flows.shopping_flow import ShoppingFlow

from utils.logger import get_logger
logger = get_logger()


@allure.step("Initialize shopping flow")
def init_flow(page):
    logger.info("Initializing shopping flow")
    return ShoppingFlow(page)


@allure.step("Search for items by name under specified price")
def search_items(flow, data):
    logger.info(f"Searching for items with term '{data['search_term']}' under price {data['max_price']}")
    return flow.search_items_by_name_under_price(
        data["search_term"],
        data["max_price"],
        data["limit"]
    )


@allure.step("Add items to cart from URLs")
def add_items_to_cart(flow, urls):
    logger.info(f"Adding {len(urls)} items to cart")
    return flow.add_items_to_cart(urls)


@allure.step("Assert cart total does not exceed budget")
def assert_cart_total_not_exceeds(flow, data, num_of_items):
    logger.info(f"Asserting cart total does not exceed budget: {data['max_price']} * {num_of_items} = {data['max_price'] * num_of_items}")
    flow.assert_cart_total_not_exceeds(
        data["max_price"],
        num_of_items
    )

@allure.step("Assert cart total equals calculated total")
def assert_cart_total_equal_to_total(flow, data, num_of_items, total_price):
    logger.info(f"Asserting cart total equals calculated total: {total_price}")
    flow.assert_cart_total_equal_to_total(
        data["max_price"],
        num_of_items,
        total_price
    )

@allure.step("Assert number of items in cart matches expected count")
def assert_number_of_items_in_cart(flow, num_of_items):
    logger.info(f"Asserting number of items in cart: {num_of_items}")
    flow.assert_cart_items_count(num_of_items)


@allure.step("Take cart screenshot")
def take_cart_screenshot(flow):
    logger.info("Taking screenshot of cart")
    return flow.cart.save_screenshot(filename="final_cart")


@allure.title("E2E Cart Flow Test")
@allure.description("Test the end-to-end cart flow including searching items under price, adding to cart with random variants, and verifying cart totals.")
def test_e2e_cart_flow(page, test_data):
    logger.info("TEST STARTED")

    flow = init_flow(page)
    
    urls = search_items(flow, test_data)
    logger.info(f"Found {len(urls)} products to add to cart: {urls}")
    
    total_price = add_items_to_cart(flow, urls)

    try:
        assert_cart_total_not_exceeds(flow, test_data, len(urls))
        assert_number_of_items_in_cart(flow, len(urls))
        assert_cart_total_equal_to_total(flow, test_data, len(urls), total_price)
    except AssertionError as e:
        raise e
    finally:
        logger.info("Taking final cart screenshot regardless of test outcome")
        take_cart_screenshot(flow)
    
    logger.info("TEST COMPLETED SUCCESSFULLY")
