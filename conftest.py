"""Pytest fixture definitions for browser and test data setup.

This module provides shared fixtures used by the end-to-end tests,
including browser setup and test data loading.
"""

import pytest
from playwright.sync_api import sync_playwright
from utils.config_loader import load_test_data


@pytest.fixture(scope="session")
def test_data():
    """Load shared test data for the test session.

    Returns:
        dict: The JSON test data used by the E2E tests.
    """
    return load_test_data("data/test_data.json")


@pytest.fixture(scope="session")
def browser():
    """Create and yield a Playwright browser instance for the test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=300,
        )
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Create and yield a new Playwright page for each test."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
