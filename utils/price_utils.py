import re

def parse_price(text):
    """Parse a price string and return the numeric value.

    Removes commas and extracts the first numeric value (integer or float).

    Args:
        text (str): The price text to parse.

    Returns:
        float: The parsed price, or 0.0 if no number found.
    """
    # remove commas
    text = text.replace(",", "")

    # extract number with optional decimal
    match = re.search(r"\d+(\.\d+)?", text)

    return float(match.group()) if match else 0.0