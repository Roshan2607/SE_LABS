# Lab 5: Static Code Analysis — Bike Share Stations
**Course:** Software Engineering (UE24CS351A)  
**Student SRN:** PES1UG24CS387  

---

## 1. Overview
This lab focuses on automated code quality, formatting, and security auditing using static analysis tools:
- **Pylint:** Logic errors, coding standards, refactoring suggestions. Target score: $\ge 9.5/10$.
- **Bandit:** Common security vulnerabilities (insecure pseudo-random number generators, SQL injections, hardcoded credentials).
- **Flake8:** PEP 8 compliance, line lengths, unused imports.

The assigned script was `bike_share_stations.py`.

---

## 2. Remediation Summary

1. **Security Fixes (Bandit):**
   - Replaced insecure `random.randint` used for authentication tokens/pins with cryptographically strong `secrets.randbelow`.
   - Ensured parameterized SQL queries with `?` placeholders to eliminate SQL injection risks.
2. **Code Quality & Architecture (Pylint):**
   - Added complete module and function docstrings.
   - Eliminated mutable default arguments (`log=[]` replaced with `log=None`).
   - Fixed naming conventions to match PEP 8.
   - **Achieved Score:** `10.00 / 10`.
3. **Style & PEP 8 (Flake8):**
   - Corrected whitespace, blank lines, and line-length constraints.

---

## 3. Tool Verification Results

| Tool | Before Refactor | After Refactor | Status |
| :--- | :--- | :--- | :--- |
| **Pylint** | ~4.2 / 10 | **10.00 / 10** | PASS |
| **Bandit** | High severity security issues | **0 issues detected** | PASS |
| **Flake8** | Multiple formatting violations | **Clean** | PASS |

---

## 4. Deliverables Included

1. `bike_share_stations.py` — Refactored application code.
2. `issues.md` — Detailed issue tracking and resolution ledger.
3. `reflection.md` — Reflection on the role of static code analysis in the SDLC.
4. `reports/before/` — Initial reports (`bandit_report.txt`, `flake8_report.txt`, `pylint_report.txt`).
5. `reports/after/` — Remediated clean reports.
6. `test_bike_share_stations.py` — Pytest verification suite.
7. `Lab_5_Static_Code_Analysis_Student_handout.pdf` — Reference student handout.

---

## 5. How to Run

### Run Application:
```bash
cd "Lab 5"
python bike_share_stations.py
```

### Run Static Analysis Audits:
```bash
pylint bike_share_stations.py
bandit -r bike_share_stations.py
```

### Run Automated Tests:
```bash
pytest test_bike_share_stations.py -v
```
