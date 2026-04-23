# Ness Home Assignment

## Description

This project is an end-to-end testing framework for a shopping website's cart functionality. It automates the process of searching for items under a specified price, adding them to the cart, and verifying the cart totals and item counts. The framework uses Playwright for browser automation, pytest for test execution, and Allure for generating detailed test reports.

## Features

- Automated e2e tests for shopping cart flow
- Search for items by name under a maximum price
- Add selected items to cart
- Verify cart total does not exceed budget
- Verify cart total matches calculated price
- Verify number of items in cart
- Detailed Allure reports with step-by-step logging

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ness_home_assignment
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```
   playwright install
   ```

## Usage

### Running Tests

- Run all tests:
  ```
  pytest
  ```

- Run tests with Allure reporting:
  ```
  pytest --alluredir=reports
  ```

### Generating Allure Report

After running tests with the `--alluredir` option, generate and serve the Allure report:
```
allure serve reports
```

This will open a web browser with the detailed test report.

## Project Structure

- `tests/`: Contains test files, including the main e2e cart flow test
- `flows/`: Business logic flows, such as the shopping flow
- `pages/`: Page object models for different website pages (home, search results, product, cart, overlay)
- `utils/`: Utility functions for configuration loading, logging, and price parsing
- `data/`: Test data files, such as `test_data.json`
- `reports/`: Directory for Allure report output include screenshots (`reports/screenshots`)
- `logs/`: Directory for log files generated during test execution

## Configuration

- Test data is loaded from `data/test_data.json`, which includes:
  - `search_term`: The term to search for (e.g., "shoes")
  - `max_price`: Maximum price per item (e.g., 350)
  - `limit`: Maximum number of items to add to cart (e.g., 5)

- Pytest configuration is in `pytest.ini`, which sets up Allure reporting and other options.

## Technologies Used

- **Playwright**: For browser automation and e2e testing
- **pytest**: Test framework
- **Allure**: Test reporting
- **Python**: Programming language

## Limitations & Assumptions

- **Authentication**: Tests are performed as a guest user; no login or user account is required or stubbed.
- **Currency**: All price values are assumed to be in Israeli Shekel (ILS).
- **Test Data**: Product availability and prices may change on the live site, which can affect test stability.
- **Environment**: Tests are designed for desktop browsers and may not be compatible with mobile layouts.
- **Third-party Dependencies**: The framework relies on Playwright, pytest, and Allure; ensure all are installed and compatible with your Python version.
- **Browser Support**: Playwright browsers must be installed prior to running tests (`playwright install`).
- **Timeouts**: Some actions may be slow due to network or site performance; timeouts are handled, but excessive delays may cause test failures.
