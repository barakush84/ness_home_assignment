"""Utility for loading structured test configuration data.

This module reads JSON test data files used by fixtures and tests.
"""

import json

def load_test_data(file_path):
    """Load test data from the JSON file.

    Returns:
        dict: The test data dictionary.
    """
    if not file_path:
        raise ValueError("File path must be provided to load test data.")

    with open(file_path) as f:
        return json.load(f)