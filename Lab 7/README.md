# Lab 7: Fuzz Testing for Input Validation Bugs
**Course:** Software Engineering (UE24CS351A)  
**Student SRN:** PES1UG24CS387  
**Fuzzing Library:** `Hypothesis`

---

## 1. Overview
This lab explores property-based fuzz testing as an automated quality assurance and security technique. By generating hundreds of pseudo-random, edge-case, and malformed inputs, fuzzing uncovers unhandled exceptions (`TypeError`, `ValueError`, `IndexError`, crash states) in user-facing parsers.

The target functions under fuzzing are:
1. `cart_total(cart)` — Parses item entries like `'pen:10x2,book:250x1'`.
2. `promo_percent(code)` — Extracts discount percentages like `'OFF20'`.
3. `delivery_zone(pincode)` — Resolves 6-digit postal codes to geographic zones.

---

## 2. Unhandled Bugs Uncovered by Fuzzing
During initial fuzzing of the baseline code with `@given(st.text() | st.none())`, the following critical edge-case crashes were reproduced:
- **`None` / Non-String Inputs:** Crashed immediately on `.split()` with `AttributeError`.
- **Malformed Item Separators:** Inputs like `'item'` or `'item:10'` crashed on unpacking `.split(':')` with `ValueError: not enough values to unpack`.
- **Invalid Quantity Multipliers:** Strings like `'book:250'` missing `'x'` crashed with `ValueError`.
- **Negative Quantities/Prices:** Accepted negative totals or produced invalid negative balances.
- **Pincode Format Bypass:** Unicode digits or string lengths $\ne 6$ resulted in `KeyError` or returned invalid zones.

---

## 3. Hardening & Defenses Implemented

In `shopping_cart.py` (and `processor.py`), all functions were defensively hardened:
1. **Type & Null Verification:** Immediate type-check `if not isinstance(..., str) or not s.strip(): return 0`.
2. **Defensive Delimiter Extraction:** Robust regex / partition splitting with boundary checks on item count.
3. **Value Sanitization:** Strict parsing of integers within try-catch blocks, discarding negative quantities and bounding promo discounts strictly to $[0, 100]$.
4. **Pincode Verification:** Checked `len(pincode) == 6` and `pincode.isdigit()`, returning `"Unknown"` for unrecognized codes.

---

## 4. Hypothesis Test Suites

- **Fuzzing Tests (`@given(st.text() | st.none())`):**
  - `test_cart_total_no_crash` — Passes thousands of arbitrary Unicode strings and nulls without throwing unhandled exceptions.
  - `test_promo_percent_no_crash` — Verifies return value is always $0 \le \text{discount} \le 100$.
  - `test_delivery_zone_no_crash` — Ensures reliable fallback without raising `KeyError`.
- **Property Invariant Tests:**
  - `test_cart_total_valid_items` — Property-based generation of valid CSV tuples verifying exact mathematical sum equality.
  - `test_promo_percent_valid_codes` — Generates integers $0..100$ prepended with `"OFF"` confirming accurate extraction.

---

## 5. Deliverables Included

1. `shopping_cart.py` / `processor.py` — Hardened application code.
2. `test_shopping_cart.py` / `test_processor.py` — Hypothesis property-based and fuzzing test suites.
3. `PES1UG24CS387_LAB7_SE.pdf` — Official submission deliverable.
4. `Lab_7_FuzzTesting_Student_Handout.pdf` — Reference student handout.

---

## 6. How to Run Fuzz Tests

```bash
cd "Lab 7"
pytest test_shopping_cart.py -v
```
