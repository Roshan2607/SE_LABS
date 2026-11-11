"""
Executable validation for UML Use Cases UC-01 through UC-07 (Lab 2).
Models the interaction of Actors (Subscriber, Dietitian, System).
"""

import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Lab 1")))
from plate_pilot import (
    MacroTargets,
    Ingredient,
    Recipe,
    Subscriber,
    MealPlanningEngine,
)


class AuthManager:
    """UC-01: Authenticate User."""
    def __init__(self):
        self.sessions = {}

    def authenticate(self, user_id: str, token: str) -> bool:
        if token == f"valid_token_for_{user_id}":
            self.sessions[user_id] = True
            return True
        return False

    def is_authenticated(self, user_id: str) -> bool:
        return self.sessions.get(user_id, False)


def test_uc01_authenticate_user():
    auth = AuthManager()
    assert auth.authenticate("SUB-001", "valid_token_for_SUB-001") is True
    assert auth.authenticate("SUB-002", "wrong_token") is False
    assert auth.is_authenticated("SUB-001") is True


def test_uc02_and_uc06_generate_meal_plan_and_recalc_extension():
    """UC-02: Generate Weekly Meal Plan with UC-06 Recalculate Macro Targets extension."""
    auth = AuthManager()
    auth.authenticate("SUB-101", "valid_token_for_SUB-101")
    assert auth.is_authenticated("SUB-101")

    sub = Subscriber(
        subscriber_id="SUB-101",
        name="Jordan",
        macro_targets=MacroTargets(calories=2200, protein=160, carbs=220, fats=70),
        allergen_exclusions={"peanuts"},
        weight_history=[75.0],
        adherence_scores=[0.95]
    )

    ing_beef = Ingredient("Lean Beef", calories=250, protein=35, carbs=0, fats=10)
    ing_pot = Ingredient("Sweet Potato", calories=150, protein=3, carbs=35, fats=0)
    catalog = [Recipe("Beef & Sweet Potato", [ing_beef, ing_pot])]

    engine = MealPlanningEngine(recipe_catalog=catalog, inventory={})

    # Step 4 extension: Recalculate macros
    new_targets = engine.recalculate_macros(sub, new_weight=74.2, recent_adherence=0.96)
    assert new_targets.calories > 2200  # lost weight rapidly -> calories increase

    # Main plan generation
    plan = engine.generate_weekly_meal_plan(sub)
    assert len(plan.daily_plans) == 7
    assert plan.status == "Pending Review"


def test_uc03_manage_deliveries():
    """UC-03: Manage Deliveries (Pause, Skip, Reschedule)."""
    sub = Subscriber(
        subscriber_id="SUB-102",
        name="Taylor",
        macro_targets=MacroTargets(2000, 140, 200, 60),
        allergen_exclusions=set()
    )
    ing = Ingredient("Oatmeal", calories=180, protein=6, carbs=32, fats=3)
    engine = MealPlanningEngine([Recipe("Oatmeal Bowl", [ing])], {})
    plan = engine.generate_weekly_meal_plan(sub)

    # Manage delivery: pause day 3
    engine.modify_delivery(plan, day_number=3, action="pause", hours_before_cutoff=24.0)
    assert plan.daily_plans[2].is_paused is True


def test_uc04_log_adherence_and_weight():
    """UC-04: Log Adherence & Weight."""
    sub = Subscriber(
        subscriber_id="SUB-103",
        name="Sam",
        macro_targets=MacroTargets(2100, 150, 210, 65),
        weight_history=[80.0],
        adherence_scores=[]
    )
    # Log 7-day adherence and weight update
    sub.weight_history.append(79.5)
    sub.adherence_scores.append(0.92)

    assert len(sub.weight_history) == 2
    assert sub.adherence_scores[-1] == 0.92


def test_uc05_review_and_edit_meal_plan():
    """UC-05: Review & Edit Meal Plan (Dietitian workflow)."""
    ing = Ingredient("Fish", calories=220, protein=30, carbs=0, fats=8)
    engine = MealPlanningEngine([Recipe("Fish Fillet", [ing])], {})
    sub = Subscriber("SUB-104", "Morgan", MacroTargets(1900, 130, 190, 55))
    plan = engine.generate_weekly_meal_plan(sub)

    # Dietitian reviews and signs off
    engine.review_and_edit_plan(plan, approved=True, notes="Verified low sodium profile.")
    assert plan.status == "Approved"
    assert "low sodium" in plan.dietitian_notes


def test_uc07_propose_ingredient_substitute():
    """UC-07: Propose Ingredient Substitute (Alternate flow extension)."""
    engine = MealPlanningEngine([], {})
    sub = Subscriber("SUB-105", "Casey", MacroTargets(2000, 140, 200, 60), allergen_exclusions={"dairy"})

    butter = Ingredient("Butter", allergens={"dairy"})
    olive_oil = Ingredient("Olive Oil", allergens=set())

    substitute = engine.propose_ingredient_substitute(
        unavailable_ingredient="Butter",
        subscriber=sub,
        substitute_candidates=[butter, olive_oil]
    )
    assert substitute.name == "Olive Oil"
