import re

ZONES = {
    "1": "North", "2": "North", "3": "West", "4": "West",
    "5": "South", "6": "South", "7": "East", "8": "East"
}

def cart_total(cart):
    """
    Computes total cart value from CSV input like 'pen:10x2,book:250x1'.
    Hardened against None, non-string, empty strings, invalid formats,
    negative values, and arbitrary fuzz inputs.
    """
    if not isinstance(cart, str) or not cart.strip():
        return 0

    total = 0
    items = cart.split(',')
    for item in items:
        item = item.strip()
        if not item:
            continue
        if ':' not in item:
            return 0
        parts = item.split(':')
        if len(parts) != 2:
            return 0
        name, rest = parts[0].strip(), parts[1].strip()
        if 'x' not in rest and 'X' not in rest:
            return 0
        qty_parts = re.split(r'[xX]', rest)
        if len(qty_parts) != 2:
            return 0
        try:
            price = int(qty_parts[0].strip())
            qty = int(qty_parts[1].strip())
        except (ValueError, TypeError):
            return 0
        if price < 0 or qty < 0:
            return 0
        total += price * qty
    return total

def promo_percent(code):
    """
    Extracts discount percentage from code like 'OFF20'.
    Hardened against None, non-string, empty strings, invalid suffixes,
    negative numbers, and numbers greater than 100.
    """
    if not isinstance(code, str) or not code.strip():
        return 0

    code = code.strip().upper()
    if 'OFF' not in code:
        return 0

    parts = code.split('OFF', 1)
    discount_str = parts[1].strip()
    if not discount_str:
        return 0

    try:
        discount = int(discount_str)
    except (ValueError, TypeError):
        return 0

    if 0 <= discount <= 100:
        return discount
    return 0

def delivery_zone(pincode):
    """
    Determines delivery zone from 6-digit pincode.
    Hardened against None, non-string, empty, invalid length,
    non-numeric characters, and unknown starting digits.
    """
    if not isinstance(pincode, str):
        return "Unknown"

    pincode = pincode.strip()
    if len(pincode) != 6 or not pincode.isdigit():
        return "Unknown"

    return ZONES.get(pincode[0], "Unknown")

def main():
    print("==== Running cart_total ====")
    user_input = input("Enter cart as name:pricexqty CSV (e.g. pen:10x2,book:250x1): ")
    result = cart_total(user_input)
    print("Cart Total:", result)

    print("\n==== Running promo_percent ====")
    user_input = input("Enter a promo code (e.g. OFF20): ")
    result = promo_percent(user_input)
    print("Discount Percent:", result)

    print("\n==== Running delivery_zone ====")
    user_input = input("Enter a 6 digit pincode (e.g. 560085): ")
    result = delivery_zone(user_input)
    print("Delivery Zone:", result)

if __name__ == "__main__":
    main()
