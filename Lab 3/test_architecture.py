"""
Verification tests for Layered Architecture and Component Boundaries (Lab 3).
Validates NFR-001 (< 5s latency) and NFR-002 (Security & Role Isolation).
"""

import pytest
import time
from architecture_components import (
    DatabaseAccessComponent,
    SecurityGatekeeperComponent,
    MealPlanningEngineComponent,
    SubscriberUIComponent,
    DietitianUIComponent,
)


@pytest.fixture
def layered_system():
    db = DatabaseAccessComponent()
    gatekeeper = SecurityGatekeeperComponent()
    engine = MealPlanningEngineComponent(db=db, gatekeeper=gatekeeper)

    # Setup patient record
    db.save_patient_health_data("SUB-999", '{"allergies": ["peanuts", "shellfish"], "weight": 74.5}')
    # Assign dietitian
    gatekeeper.assign_dietitian("SUB-999", "DIETITIAN-01")

    sub_ui = SubscriberUIComponent(engine=engine, subscriber_id="SUB-999")
    diet_ui = DietitianUIComponent(engine=engine, dietitian_id="DIETITIAN-01")
    unassigned_diet_ui = DietitianUIComponent(engine=engine, dietitian_id="DIETITIAN-99")

    return {
        "db": db,
        "engine": engine,
        "sub_ui": sub_ui,
        "diet_ui": diet_ui,
        "unassigned_diet_ui": unassigned_diet_ui
    }


def test_nfr001_performance_schedule_modification_under_5_seconds(layered_system):
    """NFR-001: System processes schedule modifications in under 5 seconds."""
    sub_ui = layered_system["sub_ui"]
    start = time.perf_counter()

    # Process modification 24 hours before dispatch
    result = sub_ui.request_delivery_skip(day_number=2, hours_left=24.0)
    total_elapsed = time.perf_counter() - start

    assert result["status"] == "success"
    assert total_elapsed < 5.0, f"Expected < 5.0s latency, got {total_elapsed:.4f}s"
    assert result["elapsed_seconds"] < 1.0


def test_nfr002_security_patient_data_access_control(layered_system):
    """NFR-002: Access restricted to owning subscriber and assigned dietitian."""
    sub_ui = layered_system["sub_ui"]
    diet_ui = layered_system["diet_ui"]
    unassigned_diet_ui = layered_system["unassigned_diet_ui"]

    # 1. Owning subscriber CAN read their data
    record = sub_ui.view_my_health_profile()
    assert "peanuts" in record

    # 2. Assigned dietitian CAN read patient data
    record_diet = diet_ui.review_patient_health("SUB-999")
    assert "peanuts" in record_diet

    # 3. Unassigned dietitian CANNOT read patient data
    with pytest.raises(PermissionError) as exc_info:
        unassigned_diet_ui.review_patient_health("SUB-999")
    assert "Access denied" in str(exc_info.value)


def test_data_encryption_at_rest(layered_system):
    """NFR-002: Ensure raw health records are encrypted in database storage."""
    db = layered_system["db"]
    # Check internal storage: raw plaintext must NOT appear
    raw_storage = db._encrypted_health_records["SUB-999"]
    assert b"allergies" not in raw_storage  # Base64 encoded, not plaintext
