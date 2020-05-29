from dataclasses import dataclass


@dataclass
class RecipeIngredient:
    recipe_id: str
    ingredient_id: str
    quantity: float
