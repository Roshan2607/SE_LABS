# Lab 4: Scenario 18 — Blackjack vs Dealer (Vibe Coding / AI-Assisted Debugging)
**Course:** Software Engineering (UE24CS351A)  
**Student SRN:** PES1UG24CS387  

---

## 1. Overview
This lab focuses on AI-assisted debugging and iterative software enhancement using Large Language Models ("Vibe Coding"). The assigned scenario is **Scenario 18: Terminal Blackjack vs Dealer**.

The starter repository contained core logical defects in hand evaluation, round flow, bankroll persistence, and input validation.

---

## 2. Tasks & Implementation Summary

### Task 1: Correct Ace Scoring
- **Defect:** Aces were statically evaluated as 11, causing hands like `[A, 9, 5]` to bust at 25 instead of totaling 15.
- **Resolution:** Implemented dynamic ace deflation logic in `cards.py:hand_value`. Each Ace initially adds 11; if total hand score exceeds 21 and Aces are present, each Ace is successively decremented by 10 (evaluated as 1) until the total is $\le 21$ or all Aces are converted.
- **Verification:** Hands `[A, 9] = 20`, `[A, 9, 5] = 15`, `[A, A, 9] = 21`, `[A, A, A, A] = 14`.

### Task 2: Complete Round Resolution
- **Defect:** Rounds did not resolve natural blackjacks, dealer bust rules, or pushes correctly, and allowed continued actions after terminal states.
- **Resolution:** Handled natural blackjack detection at deal time (paying player immediately or pushing on mutual blackjacks). Implemented dealer drawing loop requiring hits until hand value $\ge 17$. Prevented player input after busts or 21.

### Task 3: Multi-Round Bankroll & Wager Mechanism
- **Defect:** Chip balances did not persist correctly, and wagers were not validated.
- **Resolution:** Starting bankroll initialized to 100 chips. Added input loop strictly validating wager range $1 \le \text{wager} \le \text{current chips}$. Rejection of non-numeric, negative, or excessive wagers without altering the bankroll.

### Task 4: Action Feedback & Robustness
- **Defect:** Lack of draw transparency and vulnerability to empty deck `pop()` exceptions.
- **Resolution:** Added real-time draw messages (`"Player drew ('10', 'H')"`). Added defensive exception handling for depleted decks to cleanly abort rounds without crashing the runtime.

---

## 3. Deliverables Included

1. `cards.py` — Fixed deck management and dynamic Ace hand scoring.
2. `game.py` — Complete round flow, wager validation, and bankroll engine.
3. `main.py` — Interactive game entry point.
4. `requirements.txt` — Project dependencies.
5. `test_blackjack.py` — Automated pytest suite (9 tests) verifying Tasks 1–4.
6. `PES1UG24CS387 Lab 4 – Vibe Coding Deliverable Submission.pdf` — Official submission deliverable.
7. `SE_LAB4_Prompts.pdf` — LLM prompt history record.

---

## 4. How to Run

### Interactive Play:
```bash
cd "Lab 4"
python main.py
```

### Automated Tests:
```bash
pytest test_blackjack.py -v
```
