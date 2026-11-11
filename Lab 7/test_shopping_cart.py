from hypothesis import given, strategies as st
import pytest

try:
    from processor import cart_total, promo_percent, delivery_zone, ZONES
except ImportError:
    from shopping_cart import cart_total, promo_percent, delivery_zone, ZONES

# ---------------------------------------------------------------------------
# Core Fuzzing Tests (Required Starter Tests)
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
def test_cart_total_no_crash(s):
    """Fuzz cart_total with arbitrary text and None to ensure no unhandled crash."""
    result = cart_total(s)
    assert isinstance(result, (int, float))
    assert result >= 0


@given(st.text() | st.none())
def test_promo_percent_no_crash(s):
    """Fuzz promo_percent with arbitrary text and None to ensure no unhandled crash."""
    result = promo_percent(s)
    assert isinstance(result, (int, float))
    assert 0 <= result <= 100


@given(st.text() | st.none())
def test_delivery_zone_no_crash(s):
    """Fuzz delivery_zone with arbitrary text and None to ensure no unhandled crash."""
    result = delivery_zone(s)
    assert result is None or isinstance(result, str)


# ---------------------------------------------------------------------------
# Additional Property-Based Edge Case Tests Uncovered by Fuzzing
# ---------------------------------------------------------------------------

@given(
    st.lists(
        st.tuples(
            st.text(alphabet=st.characters(blacklist_categories=("Cs",), blacklist_characters=":,xX\n\r\t "), min_size=1, max_size=10),
            st.integers(min_value=0, max_value=10000),
            st.integers(min_value=0, max_value=500),
        ),
        min_size=1,
        max_size=10,
    )
)
def test_cart_total_valid_items(items):
    """Valid items formatted as name:pricexqty should compute correct sum."""
    cart_str = ",".join(f"{name}:{price}x{qty}" for name, price, qty in items)
    expected = sum(price * qty for _, price, qty in items)
    assert cart_total(cart_str) == expected


@given(st.integers(min_value=0, max_value=100))
def test_promo_percent_valid_codes(pct):
    """Valid promo codes formatted as OFF<pct> should return pct."""
    assert promo_percent(f"OFF{pct}") == pct
    assert promo_percent(f"off{pct}") == pct


@given(
    st.sampled_from(["1", "2", "3", "4", "5", "6", "7", "8"]),
    st.text(alphabet="0123456789", min_size=5, max_size=5),
)
def test_delivery_zone_valid_pincodes(first_digit, rest):
    """Valid 6-digit pincodes starting with 1-8 should return the assigned zone."""
    pincode = first_digit + rest
    assert delivery_zone(pincode) == ZONES[first_digit]
