# Lab 1: Requirements Engineering
**Course:** Software Engineering (UE24CS351A)  
**Student SRN:** PES1UG24CS387  
**Problem Statement #19:** Healthcare & Telemedicine (Personalized Meal & Diet Subscription Manager — Plate Pilot)

---

## 1. Domain Overview
The **Plate Pilot** system is an automated, medically tailored meal and diet subscription management platform designed for patients managing chronic conditions (e.g., diabetes, renal disease, severe food allergies) and wellness subscribers aiming for targeted macronutrient goals.

The system bridges clinical dietary requirements with daily food fulfillment, ensuring all generated menus respect rigorous allergen constraints, recalibrate adaptively based on biometric trends, and undergo clinical review by licensed dietitians.

---

## 2. Requirements Specification Table

| Req ID | Requirement Type | Description | Priority | Acceptance Criteria | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-001** | Functional | The system shall generate weekly meal plans strictly adhering to user macronutrient constraints and allergen exclusion lists. | High | **Pass:** Generated menu contains zero excluded allergen ingredients.<br>**Fail:** Peanuts or listed allergen included for an allergic profile. | Core safety functionality preventing life-threatening allergic reactions and ensuring medical diet compliance. |
| **FR-002** | Functional | The system shall recalculate the subscriber's next week's macronutrient targets based on logged adherence and weight-trend data (adaptive recalibration). | High | **Pass:** Next week's macros are adjusted automatically based on previous week's logged weight and food intake.<br>**Fail:** Macros remain static despite logged changes. | Ensures the diet plan remains clinically effective and adapts dynamically to subscriber progress. |
| **FR-003** | Functional | The system shall allow an assigned Dietitian to review, edit, or override an auto-generated plan before it is dispatched to the subscriber. | Medium | **Pass:** Dietitian edits are saved and reflected in the user's dispatched plan.<br>**Fail:** Auto-generated plan is dispatched ignoring dietitian edits. | Provides professional clinical oversight to guarantee automated meal suggestions are practical and medically sound. |
| **FR-004** | Functional | The system shall allow a Subscriber to pause, skip, or reschedule deliveries up to a 12-hour cutoff window before dispatch, auto-adjusting remaining nutrient totals. | Medium | **Pass:** User skips a delivery, and remaining week's deliveries are adjusted to meet weekly macro targets.<br>**Fail:** Weekly targets are missed due to a skipped delivery without adjustment, or modifications allowed past cutoff. | Offers real-world flexibility for subscribers while maintaining overall nutritional outcomes and operational logistics. |
| **FR-005** | Functional | The system shall propose a valid ingredient substitute when a planned item is unavailable, strictly satisfying allergen exclusions and macro targets. | Low | **Pass:** System suggests a valid substitute meeting macros and allergen rules.<br>**Fail:** No substitute suggested or substitute violates allergen rules. | Prevents fulfillment halts and maintains dietary consistency during supply-chain stockouts. |
| **NFR-001** | Non-Functional (Performance) | The system shall process schedule modifications (pause, skip, reschedule) in under 5 seconds during peak server load. | High | **Pass:** Benchmarking confirms `< 5s` latency for update requests under simulated peak load.<br>**Fail:** Latency exceeds 5 seconds, causing UI timeouts. | Ensures high responsiveness and timely updates for logistics and kitchen dispatch pipelines. |
| **NFR-002** | Non-Functional (Security & Privacy) | All patient metabolic/health data (allergies, diabetic limits, weight logs) must be encrypted at rest and in transit, with access restricted to the owning subscriber and assigned dietitian. | High | **Pass:** Penetration and audit tests confirm zero unauthorized read access to health records.<br>**Fail:** Any role outside subscriber/dietitian can query raw health data. | Protects sensitive health information and complies with health data privacy regulations (e.g., HIPAA). |

---

## 3. Deliverables Included

1. `plate_pilot.py` — Executable Python domain implementation representing all 5 functional requirements.
2. `test_plate_pilot.py` — Pytest validation suite verifying:
   - Zero allergen leakage in weekly plans (FR-001)
   - Dynamic macro adjustment on weight trend changes (FR-002)
   - Dietitian approval & override workflow (FR-003)
   - 12-hour cutoff enforcement on delivery pauses/skips (FR-004)
   - Allergen-safe ingredient substitution (FR-005)
3. `Level 1_Labs_PES1UG24CS387.pdf` — Original submitted deliverable document.

---

## 4. How to Execute Tests

```bash
cd "Lab 1"
pytest test_plate_pilot.py -v
```
