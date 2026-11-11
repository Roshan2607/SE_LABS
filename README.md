# Software Engineering Laboratory Submissions (Labs 1 – 7)

**Student Name:** Roshan  
**Student SRN:** PES1UG24CS387  
**Course Code:** UE24CS351A — Software Engineering  
**Department:** Computer Science & Engineering  

---

## 📋 Repository Overview

This repository consolidates all individual Software Engineering (SE) laboratory submissions (Labs 1 through 7) into a unified, cleanly structured, and fully reproducible codebase. Each lab is self-contained in its dedicated directory, containing all executable source code, automated test suites, design diagrams, analysis reports, and official submission deliverables.

---

## 🗂️ Laboratory Directory Structure

```text
SE-Labs/
├── Lab 1/                   # Requirements Engineering (Plate Pilot)
│   ├── Level 1_Labs_PES1UG24CS387.pdf
│   ├── plate_pilot.py       # Domain implementation of FR-001 through FR-005
│   ├── test_plate_pilot.py  # Pytest validation suite
│   └── README.md
├── Lab 2/                   # UML Use-Case Modelling (Plate Pilot)
│   ├── use_case_diagram.png # Rendered UML Use Case diagram
│   ├── use_case_diagram.pdf # Vector PDF deliverable
│   ├── use_case_diagram.mermaid # Mermaid diagram source
│   ├── test_use_cases.py    # Pytest suite validating all use case flows
│   └── README.md
├── Lab 3/                   # Architecture & Component Modelling (Plate Pilot)
│   ├── PES1UG24CS387_LAB3.pdf
│   ├── component_diagram.png# UML Component diagram
│   ├── architecture_components.py # 3-Tier Layered Architecture implementation
│   ├── test_architecture.py # Validates NFR-001 (<5s latency) & NFR-002 (security)
│   └── README.md
├── Lab 4/                   # AI-Assisted Debugging / Vibe Coding (Blackjack)
│   ├── cards.py             # Fixed Ace hand scoring logic (Tasks 1-4)
│   ├── game.py              # Round flow, wagers, and multi-round bankroll
│   ├── main.py              # Interactive game loop
│   ├── requirements.txt
│   ├── test_blackjack.py    # Automated test suite (9 test cases)
│   ├── PES1UG24CS387 Lab 4 – Vibe Coding Deliverable Submission.pdf
│   ├── SE_LAB4_Prompts.pdf
│   └── README.md
├── Lab 5/                   # Static Code Analysis (Bike Share Stations)
│   ├── bike_share_stations.py # Refactored code (Pylint 10/10, Bandit 0 issues)
│   ├── issues.md            # Static analysis defect ledger
│   ├── reflection.md        # Technical reflection report
│   ├── reports/
│   │   ├── before/          # Baseline reports (Bandit, Flake8, Pylint)
│   │   └── after/           # Remediated clean reports
│   ├── test_bike_share_stations.py # Functional test suite
│   ├── Lab_5_Static_Code_Analysis_Student_handout.pdf
│   └── README.md
├── Lab 6/                   # Code & Branch Coverage (Shopping Cart)
│   ├── shopping_cart.py     # Application under test
│   ├── test_shopping_cart.py# Baseline tests
│   ├── CodeCoverageTest_23_shopping_cart.py   # 100% Statement Coverage
│   ├── BranchCoverageTest_23_shopping_cart.py # 100% Branch Coverage
│   ├── PES1UG24CS387_SE_LAB6.pdf
│   ├── PES1UG24CS387_SE_LAB6.docx
│   └── README.md
├── Lab 7/                   # Fuzz Testing for Input Validation (Shopping Cart)
│   ├── shopping_cart.py     # Hardened against arbitrary fuzz inputs & None
│   ├── processor.py         # Course handout alias
│   ├── test_shopping_cart.py# Hypothesis property-based fuzz tests
│   ├── test_processor.py    # Test runner alias
│   ├── PES1UG24CS387_LAB7_SE.pdf
│   ├── Lab_7_FuzzTesting_Student_Handout.pdf
│   └── README.md
├── .gitignore
├── README.md                # Master documentation
└── run_all_tests.py         # Automated runner across all 7 labs
```

---

## 📊 Summary of Labs & Verification Status

| Lab | Title / Topic | Assigned Scenario | Deliverables & Artifacts | Test Status |
| :--- | :--- | :--- | :--- | :---: |
| **Lab 1** | Requirements Engineering | Plate Pilot (#19) | Requirements Table, FRs, NFRs, `plate_pilot.py`, `Level 1_Labs_PES1UG24CS387.pdf` | **5 / 5 PASSED** |
| **Lab 2** | UML Use-Case Modelling | Plate Pilot (#19) | Actors, Use Cases UC-01 to UC-07, `use_case_diagram.png`, `test_use_cases.py` | **6 / 6 PASSED** |
| **Lab 3** | Architecture & Component Modelling | Plate Pilot (#19) | Layered Pattern Justification, `component_diagram.png`, `test_architecture.py` | **3 / 3 PASSED** |
| **Lab 4** | AI-Assisted Vibe Coding | Scenario 18: Blackjack | Fixed Ace evaluation, round resolution, bankroll wager validation, `test_blackjack.py` | **9 / 9 PASSED** |
| **Lab 5** | Static Code Analysis | Bike Share Stations | Pylint (10.00/10), Bandit (0 issues), Flake8 clean, `reports/`, `test_bike_share_stations.py` | **5 / 5 PASSED** |
| **Lab 6** | Code & Branch Coverage | Shopping Cart | 100% Statement Coverage, 100% Branch Coverage (22/22 branches), `PES1UG24CS387_SE_LAB6.pdf` | **17 / 17 PASSED** |
| **Lab 7** | Fuzz Testing with Hypothesis | Shopping Cart / Fuzzer | Input validation hardening against arbitrary strings and nulls, `PES1UG24CS387_LAB7_SE.pdf` | **6 / 6 PASSED** |

---

## 🚀 Quick Start & Execution

### 1. Run All Tests Across All Labs (One Command)
A master test script is provided in the repository root to execute test suites across all 7 laboratories sequentially:

```bash
python run_all_tests.py
```

### 2. Run Individual Labs

#### **Lab 1: Requirements Engineering**
```bash
cd "Lab 1"
pytest test_plate_pilot.py -v
```

#### **Lab 2: UML Use-Case Modelling**
```bash
cd "Lab 2"
pytest test_use_cases.py -v
```

#### **Lab 3: Architecture & Component Modelling**
```bash
cd "Lab 3"
pytest test_architecture.py -v
```

#### **Lab 4: Scenario 18 — Blackjack**
```bash
cd "Lab 4"
# Run automated tests:
pytest test_blackjack.py -v
# Or play the interactive game:
python main.py
```

#### **Lab 5: Static Code Analysis — Bike Share Stations**
```bash
cd "Lab 5"
pylint bike_share_stations.py
bandit -r bike_share_stations.py
pytest test_bike_share_stations.py -v
```

#### **Lab 6: Code & Branch Coverage**
```bash
cd "Lab 6"
# Line / Statement Coverage (100%):
python -m coverage erase
python -m coverage run -m pytest CodeCoverageTest_23_shopping_cart.py
python -m coverage report -m

# Branch Coverage (100%):
python -m coverage erase
python -m coverage run --branch -m pytest BranchCoverageTest_23_shopping_cart.py
python -m coverage report -m
```

#### **Lab 7: Fuzz Testing (Hypothesis)**
```bash
cd "Lab 7"
pytest test_shopping_cart.py -v
```
