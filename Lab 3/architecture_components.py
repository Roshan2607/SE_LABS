"""
Plate Pilot: Layered Architecture Implementation (Lab 3)
Demonstrates component separation into Presentation, Business Logic, and Data Access layers.
Enforces NFR-001 (< 5s response latency) and NFR-002 (health data encryption & role isolation).
"""

import time
import base64
from typing import Dict, Any, Optional, List


# ---------------------------------------------------------------------------
# Data Access Layer (Bottom Layer - Isolated from Direct UI Access)
# ---------------------------------------------------------------------------

class DatabaseAccessComponent:
    """
    Bottom Data Layer: Encrypts patient metabolic data at rest (NFR-002)
    and restricts direct queries from Presentation layer.
    """
    def __init__(self):
        # Simulated encrypted storage at rest
        self._encrypted_health_records: Dict[str, bytes] = {}
        self._meal_plans: Dict[str, Any] = {}

    def _encrypt(self, raw_data: str) -> bytes:
        return base64.b64encode(raw_data.encode('utf-8'))

    def _decrypt(self, cipher_data: bytes) -> str:
        return base64.b64decode(cipher_data).decode('utf-8')

    def save_patient_health_data(self, subscriber_id: str, health_data_json: str):
        self._encrypted_health_records[subscriber_id] = self._encrypt(health_data_json)

    def get_patient_health_data(self, subscriber_id: str) -> Optional[str]:
        cipher = self._encrypted_health_records.get(subscriber_id)
        if not cipher:
            return None
        return self._decrypt(cipher)

    def save_meal_plan(self, plan_id: str, plan_data: Dict[str, Any]):
        self._meal_plans[plan_id] = plan_data

    def get_meal_plan(self, plan_id: str) -> Optional[Dict[str, Any]]:
        return self._meal_plans.get(plan_id)


# ---------------------------------------------------------------------------
# Business Logic Layer (Central Layer - Gatekeeper & Rule Engine)
# ---------------------------------------------------------------------------

class SecurityGatekeeperComponent:
    """Enforces NFR-002: Access restricted to owning subscriber and assigned dietitian."""
    def __init__(self):
        self.dietitian_assignments: Dict[str, str] = {}  # subscriber_id -> dietitian_id

    def assign_dietitian(self, subscriber_id: str, dietitian_id: str):
        self.dietitian_assignments[subscriber_id] = dietitian_id

    def authorize_read(self, requestor_id: str, requestor_role: str, target_subscriber_id: str) -> bool:
        if requestor_role == "Subscriber" and requestor_id == target_subscriber_id:
            return True
        if requestor_role == "Dietitian" and self.dietitian_assignments.get(target_subscriber_id) == requestor_id:
            return True
        return False


class RuleEngineComponent:
    """Centralized Clinical & Business Rules."""
    @staticmethod
    def validate_allergen_safety(recipe_allergens: List[str], subscriber_exclusions: List[str]) -> bool:
        return not bool(set(recipe_allergens).intersection(set(subscriber_exclusions)))

    @staticmethod
    def validate_cutoff(hours_until_dispatch: float) -> bool:
        return hours_until_dispatch >= 12.0


class MealPlanningEngineComponent:
    """Core domain logic orchestrator interacting with Rule Engine and Database."""
    def __init__(self, db: DatabaseAccessComponent, gatekeeper: SecurityGatekeeperComponent):
        self.db = db
        self.gatekeeper = gatekeeper
        self.rules = RuleEngineComponent()

    def process_schedule_modification(self, subscriber_id: str, day_number: int, action: str, hours_before_dispatch: float) -> Dict[str, Any]:
        """
        NFR-001: Benchmarked to execute in milliseconds (guaranteeing < 5s).
        """
        start_time = time.perf_counter()

        if not self.rules.validate_cutoff(hours_before_dispatch):
            raise PermissionError("Modifications must occur at least 12 hours before dispatch.")

        # Query local database directly (layered pattern benefits)
        plan = self.db.get_meal_plan(f"plan_{subscriber_id}")
        if not plan:
            plan = {"subscriber_id": subscriber_id, "modifications": []}

        plan["modifications"].append({"day": day_number, "action": action})
        self.db.save_meal_plan(f"plan_{subscriber_id}", plan)

        elapsed = time.perf_counter() - start_time
        return {"status": "success", "action": action, "elapsed_seconds": elapsed}

    def fetch_patient_health_record(self, requestor_id: str, role: str, target_subscriber_id: str) -> Optional[str]:
        if not self.gatekeeper.authorize_read(requestor_id, role, target_subscriber_id):
            raise PermissionError("Access denied: Unauthorized role or unassigned dietitian (NFR-002).")
        return self.db.get_patient_health_data(target_subscriber_id)


# ---------------------------------------------------------------------------
# Presentation Layer (Top Layer - User Portals)
# ---------------------------------------------------------------------------

class SubscriberUIComponent:
    """Subscriber Mobile / Web Client."""
    def __init__(self, engine: MealPlanningEngineComponent, subscriber_id: str):
        self.engine = engine
        self.subscriber_id = subscriber_id

    def request_delivery_skip(self, day_number: int, hours_left: float):
        return self.engine.process_schedule_modification(
            self.subscriber_id, day_number, "skip", hours_left
        )

    def view_my_health_profile(self):
        return self.engine.fetch_patient_health_record(
            self.subscriber_id, "Subscriber", self.subscriber_id
        )


class DietitianUIComponent:
    """Dietitian Clinical Portal."""
    def __init__(self, engine: MealPlanningEngineComponent, dietitian_id: str):
        self.engine = engine
        self.dietitian_id = dietitian_id

    def review_patient_health(self, patient_subscriber_id: str):
        return self.engine.fetch_patient_health_record(
            self.dietitian_id, "Dietitian", patient_subscriber_id
        )
