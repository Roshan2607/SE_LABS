"""
Unit tests validating Functional Requirements FR-001 through FR-005 for Plate Pilot (Lab 1).
"""

import pytest
from plate_pilot import (
    MacroTargets,
    Ingredient,
    Recipe,
    Subscriber,
    MealPlanningEngine,
)


@pytest.fixture
def sample_catalog():
    i_chicken = Ingredient(name="Grilled Chicken", allergens=set(), calories=300, protein=40, carbs=0, fats=10)
    i_rice = Ingredient(name="Brown Rice", allergens=set(), calories=200, protein=5, carbs=45, fats=2)
    i_peanut_sauce = Ingredient(name="Peanut Sauce", allergens={"peanuts"}, calories=150, protein=4, carbs=10, fats=12)
    i_olive_oil = Ingredient(name="Olive Oil", allergens=set(), calories=120, protein=0, carbs=0, fats=14)
    i_almond_sauce = Ingredient(name="Almond Dressing", allergens={"tree_nuts"}, calories=140, protein=3, carbs=8, fats=12)

    r_chicken_rice = Recipe(name="Chicken & Rice", ingredients=[i_chicken, i_rice, i_olive_oil])
    r_peanut_noodles = Recipe(name="Peanut Noodles", ingredients=[i_rice, i_peanut_sauce])
    r_plain_bowl = Recipe(name="Plain Energy Bowl", ingredients=[i_rice, i_olive_oil])
    r_protein_plate = Recipe(name="Protein Plate", ingredients=[i_chicken, i_olive_oil])

    return [r_chicken_rice, r_peanut_noodles, r_plain_bowl, r_protein_plate]


@pytest.fixture
def subscriber_peanut_allergic():
    targets = MacroTargets(calories=2000, protein=150, carbs=200, fats=65)
    return Subscriber(
        subscriber_id="SUB-001",
        name="Alex Smith",
        macro_targets=targets,
        allergen_exclusions={"peanuts"},
        weight_history=[72.0],
        adherence_scores=[0.90]
    )


def test_fr001_allergen_free_meal_plan(sample_catalog, subscriber_peanut_allergic):
    """FR-001: Meal plan must contain ZERO excluded allergens."""
    engine = MealPlanningEngine(recipe_catalog=sample_catalog, inventory={})
    plan = engine.generate_weekly_meal_plan(subscriber_peanut_allergic)

    assert len(plan.daily_plans) == 7
    for day in plan.daily_plans:
        for recipe in day.recipes:
            assert "peanuts" not in recipe.allergens


def test_fr002_macro_recalculation(sample_catalog, subscriber_peanut_allergic):
    """FR-002: System recalculates macros based on logged weight & adherence."""
    engine = MealPlanningEngine(recipe_catalog=sample_catalog, inventory={})
    old_cals = subscriber_peanut_allergic.macro_targets.calories
    # Weight increased by 1.0kg with high adherence
    new_targets = engine.recalculate_macros(subscriber_peanut_allergic, new_weight=73.0, recent_adherence=0.92)

    assert new_targets.calories < old_cals
    assert len(subscriber_peanut_allergic.weight_history) == 2


def test_fr003_dietitian_review_override(sample_catalog, subscriber_peanut_allergic):
    """FR-003: Dietitian can approve/reject/override weekly plan before dispatch."""
    engine = MealPlanningEngine(recipe_catalog=sample_catalog, inventory={})
    plan = engine.generate_weekly_meal_plan(subscriber_peanut_allergic)
    assert plan.status == "Pending Review"

    updated = engine.review_and_edit_plan(plan, approved=True, notes="Macros balanced well.")
    assert updated.status == "Approved"
    assert updated.dietitian_notes == "Macros balanced well."


def test_fr004_delivery_cutoff_enforcement(sample_catalog, subscriber_peanut_allergic):
    """FR-004: Delivery changes allowed only up to 12h cutoff window."""
    engine = MealPlanningEngine(recipe_catalog=sample_catalog, inventory={})
    plan = engine.generate_weekly_meal_plan(subscriber_peanut_allergic)

    # 15 hours before dispatch -> Allowed
    success = engine.modify_delivery(plan, day_number=2, action="skip", hours_before_cutoff=15.0)
    assert success is True
    assert plan.daily_plans[1].is_skipped is True

    # 4 hours before dispatch -> Rejected
    with pytest.raises(ValueError):
        engine.modify_delivery(plan, day_number=3, action="pause", hours_before_cutoff=4.0)


def test_fr005_ingredient_substitution_allergen_safe(sample_catalog, subscriber_peanut_allergic):
    """FR-005: Suggested substitute must strictly avoid allergen exclusions."""
    engine = MealPlanningEngine(recipe_catalog=sample_catalog, inventory={})
    peanut_butter = Ingredient(name="Peanut Butter", allergens={"peanuts"})
    sunflower_butter = Ingredient(name="Sunflower Seed Butter", allergens=set())

    substitute = engine.propose_ingredient_substitute(
        unavailable_ingredient="Peanut Sauce",
        subscriber=subscriber_peanut_allergic,
        substitute_candidates=[peanut_butter, sunflower_butter]
    )

    assert substitute is not None
    assert substitute.name == "Sunflower Seed Butter"
    assert "peanuts" not in substitute.allergens
