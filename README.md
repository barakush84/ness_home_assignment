# Ness Home Assignment - E2E Shopping Cart Test Framework

## 📋 Overview

This project is a comprehensive end-to-end (E2E) testing framework designed to validate the shopping cart functionality of an e-commerce website (ksp.co.il - Israeli shoe retailer). The framework automates the complete shopping workflow: searching for products under a specified price threshold, adding them to cart with random size variants, and verifying cart totals and item counts.

Built using modern testing practices with the Page Object Model (POM) pattern, the framework ensures maintainable, reliable, and scalable test automation.

## 🎯 Key Features

- **Complete E2E Shopping Flow**: Automated search → selection → cart addition → verification
- **Price-Based Filtering**: Finds products under specified maximum price per item
- **Random Variant Selection**: Automatically selects available sizes for each product
- **Comprehensive Assertions**: Validates cart totals, item counts, and budget constraints
- **Detailed Reporting**: Allure integration with step-by-step test execution logs
- **Screenshot Capture**: Automatic screenshots for debugging and reporting
- **Robust Error Handling**: Retry mechanisms for flaky operations
- **Configurable Test Data**: JSON-based configuration for easy test parameterization

## 🏗️ Architecture & Design Patterns

### Page Object Model (POM)
The framework implements the Page Object Model pattern for better maintainability:
- **BasePage**: Common functionality (navigation, screenshots)
- **HomePage**: Search functionality
- **SearchResultsPage**: Product extraction with pagination support
- **ProductPage**: Individual product interactions with retry logic
- **CartPage**: Cart verification and assertions
- **OverlayPage**: Post-add-to-cart overlay handling

### Business Logic Layer
- **ShoppingFlow**: Orchestrates the entire shopping workflow
- Centralized business logic separate from UI interactions

### Test Layer
- **Pytest Fixtures**: Browser and page lifecycle management
- **Allure Integration**: Detailed step-by-step reporting
- **Helper Functions**: Decorated test steps for better traceability

## 📁 Project Structure

```
ness_home_assignment/
├── tests/
│   └── test_e2e_cart_flow.py      # Main E2E test suite
├── flows/
│   └── shopping_flow.py          # Business logic orchestration
├── pages/                        # Page Object Models
│   ├── base_page.py              # Base page with common functionality
│   ├── home_page.py              # Home page search
│   ├── search_results_page.py    # Search results with pagination
│   ├── product_page.py           # Product details and cart addition
│   ├── cart_page.py              # Cart verification
│   └── overlay_page.py           # Post-add overlay handling
├── utils/                        # Utility modules
│   ├── config_loader.py          # JSON configuration loading
│   ├── logger.py                 # Logging configuration
│   └── price_utils.py            # Price parsing utilities
├── data/
│   └── test_data.json            # Test configuration data
├── reports/                      # Allure report outputs
├── logs/                        # Application logs
├── conftest.py                   # Pytest fixtures and configuration
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Python dependencies
├── README.md                     # This documentation
└── ReadMeAIBugs.md              # Known issues and fixes documentation
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Git

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ness_home_assignment
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**:
   ```bash
   playwright install
   ```

## 🧪 Running Tests

### Basic Test Execution
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_e2e_cart_flow.py
```

### Allure Reporting
```bash
# Run tests with Allure reporting
pytest --alluredir=reports

# Generate and serve Allure report
allure serve reports
```

### Test Configuration
Tests are configured via `data/test_data.json`:
```json
{
  "search_term": "shoes",
  "max_price": 400,
  "limit": 5
}
```

## 🔧 Configuration Details

### Test Data Configuration (`data/test_data.json`)
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `search_term` | string | Product search keyword | "shoes" |
| `max_price` | number | Maximum price per item (ILS) | 400 |
| `limit` | number | Maximum items to add to cart | 5 |

### Pytest Configuration (`pytest.ini`)
- Enables Allure reporting (`--alluredir=reports`)
- Configures async test execution
- Sets up CLI logging

### Logging Configuration (`utils/logger.py`)
- File-based logging with timestamps
- Configurable log levels
- Automatic log directory creation

## 🛠️ Technologies & Dependencies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Playwright** | Latest | Browser automation and E2E testing |
| **pytest** | Latest | Test framework and execution |
| **pytest-asyncio** | Latest | Async test support |
| **allure-pytest** | Latest | Test reporting and visualization |
| **tenacity** | Latest | Retry mechanisms for flaky operations |

## 📊 Test Flow & Assertions

### Complete Shopping Workflow

1. **Search Phase**:
   - Navigate to home page
   - Enter search term
   - Extract products under price limit
   - Handle pagination for complete results

2. **Selection Phase**:
   - Visit individual product pages
   - Extract pricing information
   - Select random available sizes
   - Add products to cart

3. **Verification Phase**:
   - Navigate to cart page
   - Assert total price ≤ budget (max_price × item_count)
   - Assert total price matches calculated sum
   - Assert item count matches expected quantity

### Key Assertions
- **Budget Compliance**: Cart total doesn't exceed `max_price × limit`
- **Price Accuracy**: Cart total matches sum of individual item prices
- **Item Count**: Cart contains expected number of items
- **Product Availability**: Successfully finds and adds specified number of items

## 🐛 Known Issues & Limitations

### Current Limitations
- **Guest User Only**: Tests run as anonymous users without authentication
- **Single Browser**: Currently configured for Chromium only
- **Desktop Focused**: Optimized for desktop viewport, may not work on mobile
- **Site Dependencies**: Relies on ksp.co.il site structure and availability including availability of product selected by other customers
- **Price Volatility**: Live site prices may change, affecting test stability

### Potential Improvements
- Add type hints throughout codebase
- Implement parameterized tests for different scenarios
- Add console logging alongside file logging
- Extract hardcoded timeouts to configuration
- Add more comprehensive error handling

## 📈 Reporting & Debugging

### Allure Reports
- Step-by-step test execution visualization
- Screenshots captured at key points
- Detailed failure information with stack traces
- Historical test trends and analytics

### Logging
- Comprehensive file-based logging
- Timestamped log files in `logs/` directory
- Debug information for troubleshooting

### Screenshots
- Automatic screenshot capture and add to Allure reports on test steps
- Saved to `reports/` directory
- Useful for debugging and documentation

## 🤝 Contributing

1. Follow the existing Page Object Model structure
2. Add appropriate logging for new functionality
3. Include Allure steps for test actions
4. Update documentation for significant changes
5. Ensure all tests pass before submitting

## 📄 License

This project is part of the Ness Home Assignment and is intended for educational and demonstration purposes.

---

**Note**: This framework is specifically designed for the ksp.co.il e-commerce platform and may require updates if the site structure changes.
