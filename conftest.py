import pytest
from playwright.sync_api import sync_playwright
from utils.config_loader import load_test_data


@pytest.fixture(scope="session")
def test_data():
    return load_test_data("data/test_data.json")

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=300,
        )
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
