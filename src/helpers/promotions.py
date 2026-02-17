"""Helpers for promotion price calculations."""


def calculate_current_price(base_price: int, discount_percent: int) -> int:
    """Calculate current price with discount applied."""
    if discount_percent <= 0:
        return base_price
    return int(base_price * (100 - discount_percent) / 100)
