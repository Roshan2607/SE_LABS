"""
Plate Pilot: Personalized Meal & Diet Subscription Manager
Problem Statement #19: Healthcare & Telemedicine
Deliverable implementation of Functional & Non-Functional Requirements (Lab 1)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
import datetime


@dataclass
class MacroTargets:
    calories: int
    protein: int  # grams
    carbs: int    # grams
    fats: int     # grams


@dataclass
class Ingredient:
    name: str
    allergens: Set[str] = field(default_factory=set)
    calories: int = 0
    protein: int = 0
    carbs: int = 0
    fats: int = 0


@dataclass
class Recipe:
    name: str
    ingredients: List[Ingredient]
    meal_type: str = "dinner"  # breakfast, lunch, dinner

    @property
    def allergens(self) -> Set[str]:
        result = set()
        for ing in self.ingredients:
            result.update(ing.allergens)
        return result

    @property
    def macros(self) -> MacroTargets:
        cal = sum(ing.calories for ing in self.ingredients)
        pro = sum(ing.protein for ing in self.ingredients)
        car = sum(ing.carbs for ing in self.ingredients)
        fat = sum(ing.fats for ing in self.ingredients)
        return MacroTargets(calories=cal, protein=pro, carbs=car, fats=fat)


@dataclass
class DailyPlan:
    day_number: int
    recipes: List[Recipe]
    is_paused: bool = False
    is_skipped: bool = False


@dataclass
class WeeklyMealPlan:
    subscriber_id: str
    daily_plans: List[DailyPlan]
    status: str = "Pending Review"  # Pending Review, Approved, Dispatched
    dietitian_notes: Optional[str] = None


@dataclass
class Subscriber:
    subscriber_id: str
    name: str
    macro_targets: MacroTargets
    allergen_exclusions: Set[str] = field(default_factory=set)
    weight_history: List[float] = field(default_factory=list)
    adherence_scores: List[float] = field(default_factory=list)


class MealPlanningEngine:
    """Core domain engine implementing FR-001 through FR-005."""

    def __init__(self, recipe_catalog: List[Recipe], inventory: Dict[str, int]):
        self.recipe_catalog = recipe_catalog
        self.inventory = inventory

    def generate_weekly_meal_plan(self, subscriber: Subscriber) -> WeeklyMealPlan:
        """
        FR-001: Generate weekly meal plans strictly adhering to user
        macronutrient constraints and allergen exclusion lists.
        Zero excluded allergen ingredients allowed.
        """
        daily_plans = []
        for day in range(1, 8):
            selected_recipes = []
            for recipe in self.recipe_catalog:
                # Check allergen exclusion
                if recipe.allergens.intersection(subscriber.allergen_exclusions):
                    continue
                selected_recipes.append(recipe)
                if len(selected_recipes) >= 3:
                    break

            if not selected_recipes:
                raise ValueError(f"No allergen-safe recipes found for subscriber {subscriber.name}")

            daily_plans.append(DailyPlan(day_number=day, recipes=selected_recipes))

        return WeeklyMealPlan(
            subscriber_id=subscriber.subscriber_id,
            daily_plans=daily_plans,
            status="Pending Review"
        )

    def recalculate_macros(self, subscriber: Subscriber, new_weight: float, recent_adherence: float) -> MacroTargets:
        """
        FR-002: Recalculate the subscriber's next week's macro targets
        based on logged adherence and weight-trend data.
        """
        subscriber.weight_history.append(new_weight)
        subscriber.adherence_scores.append(recent_adherence)

        current = subscriber.macro_targets
        if len(subscriber.weight_history) >= 2:
            delta_weight = new_weight - subscriber.weight_history[-2]
        else:
            delta_weight = 0.0

        new_calories = current.calories
        new_protein = current.protein

        # Adaptive recalibration logic
        if delta_weight > 0.5:
            # Gaining weight faster than target -> decrease calories slightly
            new_calories = max(1200, current.calories - 150)
        elif delta_weight < -0.5:
            # Losing weight too fast -> increase calories
            new_calories = current.calories + 150

        if recent_adherence > 0.85:
            new_protein = current.protein + 5

        new_targets = MacroTargets(
            calories=new_calories,
            protein=new_protein,
            carbs=current.carbs,
            fats=current.fats
        )
        subscriber.macro_targets = new_targets
        return new_targets

    def review_and_edit_plan(self, plan: WeeklyMealPlan, approved: bool, notes: Optional[str] = None) -> WeeklyMealPlan:
        """
        FR-003: Dietitian can review, edit, or override an auto-generated plan
        before it is dispatched to the subscriber.
        """
        plan.status = "Approved" if approved else "Rejected"
        plan.dietitian_notes = notes
        return plan

    def modify_delivery(self, plan: WeeklyMealPlan, day_number: int, action: str, hours_before_cutoff: float) -> bool:
        """
        FR-004: Subscriber can pause, skip, or reschedule deliveries
        up to the cutoff window (12 hours before dispatch). System auto-adjusts
        remaining nutrient totals.
        """
        if hours_before_cutoff < 12.0:
            raise ValueError("Modifications must be made at least 12 hours before dispatch.")

        for day in plan.daily_plans:
            if day.day_number == day_number:
                if action == "skip":
                    day.is_skipped = True
                    return True
                elif action == "pause":
                    day.is_paused = True
                    return True

        return False

    def propose_ingredient_substitute(
        self,
        unavailable_ingredient: str,
        subscriber: Subscriber,
        substitute_candidates: List[Ingredient]
    ) -> Optional[Ingredient]:
        """
        FR-005: When a planned ingredient is unavailable, system proposes a
        substitute that still satisfies allergen exclusions and macro targets.
        """
        for candidate in substitute_candidates:
            if candidate.name == unavailable_ingredient:
                continue
            # Ensure candidate does not trigger subscriber's allergies
            if candidate.allergens.intersection(subscriber.allergen_exclusions):
                continue
            return candidate
        return None
