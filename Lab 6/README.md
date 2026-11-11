# Lab 6: Code and Branch Coverage — Shopping Cart
**Course:** Software Engineering (UE24CS351A)  
**Student SRN:** PES1UG24CS387  
**Repository Scenario:** `L6_L7_23_shopping_cart`

---

## 1. Overview
This lab focuses on dynamic testing and coverage measurement using `pytest` and `coverage.py`.
The target application is `shopping_cart.py`, providing three core functions:
- `cart_total(cart)`: Parses CSV input format `item:pricexqty` and sums total.
- `promo_percent(code)`: Extracts percentage discount from `OFF<pct>` promo strings.
- `delivery_zone(pincode)`: Maps 6-digit postal codes to geographic zones based on leading digit.

---

## 2. Testing Objectives & Coverage Metrics

### Stage 1: Statement / Line Coverage
- **Target:** 100% statement execution coverage.
- **Suite:** `CodeCoverageTest_23_shopping_cart.py` (7 tests).
- **Result:**
  ```text
  Name                                   Stmts   Miss  Cover
  ----------------------------------------------------------
  CodeCoverageTest_23_shopping_cart.py      23      0   100%
  shopping_cart.py                          32      0   100%
  ----------------------------------------------------------
  TOTAL                                     55      0   100%
  ```

### Stage 2: Branch Coverage
- **Target:** 100% decision branch coverage (evaluating both `True` and `False` outcomes for all conditional paths).
- **Suite:** `BranchCoverageTest_23_shopping_cart.py` (10 tests).
- **Result:**
  ```text
  Name                                     Stmts   Miss Branch BrPart  Cover
  --------------------------------------------------------------------------
  BranchCoverageTest_23_shopping_cart.py      29      0      0      0   100%
  shopping_cart.py                            32      0     22      0   100%
  --------------------------------------------------------------------------
  TOTAL                                       61      0     22      0   100%
  ```

---

## 3. Deliverables Included

1. `shopping_cart.py` — Target application under test.
2. `test_shopping_cart.py` — Baseline test suite.
3. `CodeCoverageTest_23_shopping_cart.py` — Full statement coverage suite.
4. `BranchCoverageTest_23_shopping_cart.py` — Full branch coverage suite.
5. `PES1UG24CS387_SE_LAB6.pdf` — Official submission lab report.
6. `PES1UG24CS387_SE_LAB6.docx` — Source editable lab document.

---

## 4. How to Execute Coverage Tests

### Measure Line Coverage:
```bash
cd "Lab 6"
python -m coverage erase
python -m coverage run -m pytest CodeCoverageTest_23_shopping_cart.py
python -m coverage report -m
```

### Measure Branch Coverage:
```bash
cd "Lab 6"
python -m coverage erase
python -m coverage run --branch -m pytest BranchCoverageTest_23_shopping_cart.py
python -m coverage report -m
```
