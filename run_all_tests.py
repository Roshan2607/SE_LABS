"""
Master Test Runner for SE Lab Submissions (Labs 1 through 7)
Course: Software Engineering (UE24CS351A)
Student: Roshan (PES1UG24CS387)
"""

import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

LABS = [
    {
        "name": "Lab 1: Requirements Engineering",
        "dir": ROOT / "Lab 1",
        "cmd": [sys.executable, "-m", "pytest", "test_plate_pilot.py", "-q"],
    },
    {
        "name": "Lab 2: UML Use-Case Modelling",
        "dir": ROOT / "Lab 2",
        "cmd": [sys.executable, "-m", "pytest", "test_use_cases.py", "-q"],
    },
    {
        "name": "Lab 3: Architecture & Component Modelling",
        "dir": ROOT / "Lab 3",
        "cmd": [sys.executable, "-m", "pytest", "test_architecture.py", "-q"],
    },
    {
        "name": "Lab 4: Vibe Coding - Blackjack vs Dealer",
        "dir": ROOT / "Lab 4",
        "cmd": [sys.executable, "-m", "pytest", "test_blackjack.py", "-q"],
    },
    {
        "name": "Lab 5: Static Analysis - Bike Share Stations",
        "dir": ROOT / "Lab 5",
        "cmd": [sys.executable, "-m", "pytest", "test_bike_share_stations.py", "-q"],
    },
    {
        "name": "Lab 6: Line & Branch Coverage - Shopping Cart",
        "dir": ROOT / "Lab 6",
        "cmd": [sys.executable, "-m", "pytest", "CodeCoverageTest_23_shopping_cart.py", "BranchCoverageTest_23_shopping_cart.py", "-q"],
    },
    {
        "name": "Lab 7: Fuzz Testing - Shopping Cart / Hypothesis",
        "dir": ROOT / "Lab 7",
        "cmd": [sys.executable, "-m", "pytest", "test_shopping_cart.py", "test_processor.py", "-q"],
    },
]


def main():
    print("=" * 70)
    print("       SOFTWARE ENGINEERING LAB SUBMISSIONS MASTER TEST RUNNER")
    print("       Student SRN: PES1UG24CS387 | GitHub: Roshan2607")
    print("=" * 70)

    results = []
    all_passed = True

    for lab in LABS:
        print(f"\n[RUNNING] {lab['name']}...")
        proc = subprocess.run(lab["cmd"], cwd=lab["dir"], capture_output=True, text=True)
        passed = (proc.returncode == 0)
        status_text = "PASSED" if passed else "FAILED"
        results.append((lab["name"], status_text, proc.stdout.strip()))

        if passed:
            print(f"  -> [OK] {proc.stdout.strip().splitlines()[-1] if proc.stdout else 'PASSED'}")
        else:
            all_passed = False
            print(f"  -> [FAIL] {proc.stderr or proc.stdout}")

    print("\n" + "=" * 70)
    print(f"{'Lab':<48} | {'Status':<15}")
    print("-" * 70)
    for name, status, _ in results:
        print(f"{name:<48} | {status:<15}")
    print("=" * 70)

    if all_passed:
        print("\nALL LABS EXECUTED AND PASSED SUCCESSFULLY! (7 / 7)")
        sys.exit(0)
    else:
        print("\nSOME LAB TESTS FAILED. PLEASE INSPECT OUTPUT ABOVE.")
        sys.exit(1)


if __name__ == "__main__":
    main()
