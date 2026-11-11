import pytest
from shopping_cart import item_total, cart_discount, shipping_fee


def test_item_total_valid_regular():
    assert item_total("food", 100, 2) == 210


def test_item_total_bulk():
    assert item_total("electronics", 100, 10) == 1062


def test_item_total_unknown_category():
    with pytest.raises(ValueError, match="unknown category"):
        item_total("toys", 100, 1)


def test_item_total_negative_price():
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", -1, 2)


def test_item_total_zero_quantity():
    with pytest.raises(ValueError, match="invalid price or quantity"):
        item_total("food", 100, 0)


def test_cart_discount_all_tiers():
    assert cart_discount(6000, True, "FLAT10") == 1200
    assert cart_discount(3000, False, "NOPE") == 200
    assert cart_discount(500, False, "NOPE") == 0


def test_shipping_lines():
    assert shipping_fee(100, True, True) == 50
    assert shipping_fee(1000, False, False) == 0
    assert shipping_fee(100, False, True) == 140



def test_coupon_threshold_false_branch():
    # Correct coupon, but cart value is below 1000.
    assert cart_discount(500, False, "FLAT10") == 0


def test_express_prime_false_nested_branch():
    # Express delivery for a non-Prime customer.
    assert shipping_fee(100, False, True) == 140


def test_item_total_valid_price_and_quantity():
    # Valid price and positive quantity.
    assert item_total("clothing", 100, 1) == 112
