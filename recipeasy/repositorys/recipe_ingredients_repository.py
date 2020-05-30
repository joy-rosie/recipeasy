from __future__ import annotations

from typing import List

from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.exceptions import DeleteError
from pynamodb.expressions.condition import Comparison
from pynamodb.models import Model

from recipeasy.exceptions.NotFoundException import NotFoundException
from recipeasy.exceptions.RepositoryException import RepositoryException
from recipeasy.models.recipe_ingredient import RecipeIngredient


class RecipeIngredientModel(Model):
    class Meta:
        table_name = "recipe_ingredients_v1"
        region = "eu-west-1"
        write_capacity_units = 10
        read_capacity_units = 10

    recipe_id = UnicodeAttribute(hash_key=True)
    ingredient_id = UnicodeAttribute(range_key=True)
    quantity = NumberAttribute(default=0)

    def from_recipe_ingredient(self, recipe_ingredient: RecipeIngredient) -> RecipeIngredientModel:
        self.recipe_id = recipe_ingredient.recipe_id
        self.ingredient_id = recipe_ingredient.ingredient_id
        self.quantity = recipe_ingredient.quantity
        return self

    def to_recipe_ingredient(self) -> RecipeIngredient:
        return RecipeIngredient(recipe_id=self.recipe_id, ingredient_id=self.ingredient_id, quantity=self.quantity)


class RecipeIngredientsRepository:

    def __init__(self):
        if not RecipeIngredientModel.exists():
            RecipeIngredientModel.create_table(wait=True)

    def upsert_ingredient_to_recipe(self, recipe_ingredient: RecipeIngredient) -> None:
        RecipeIngredientModel().from_recipe_ingredient(recipe_ingredient).save()

    def get_recipe_ingredient(self, recipe_id: str, ingredient_id: str) -> RecipeIngredient:
        return self.__get_recipe_ingredient_model_by_id(recipe_id, ingredient_id).to_recipe_ingredient()

    def get_recipe_ingredients(self, recipe_id: str) -> List[RecipeIngredient]:
        return [r.to_recipe_ingredient() for r in RecipeIngredientModel.query(hash_key=recipe_id)]

    def remove_ingredient_from_recipe(self, recipe_id: str, ingredient_id: str) -> None:
        try:
            self.__get_recipe_ingredient_model_by_id(recipe_id, ingredient_id).delete()
        except DeleteError:
            raise RepositoryException(f"Failed to delete ingredient {ingredient_id} for recipe {recipe_id}")

    def remove_recipe(self, recipe_id) -> None:
        for recipe_ingredient_model in RecipeIngredientModel.query(hash_key=recipe_id):
            try:
                recipe_ingredient_model.delete()
            except DeleteError:
                # Ignore error and carry on
                pass

    def __get_recipe_ingredient_model_by_id(self, recipe_id: str, ingredient_id: str) -> RecipeIngredientModel:
        try:
            return RecipeIngredientModel.query(
                hash_key=recipe_id,
                range_key_condition=Comparison("=", "ingredient_id", ingredient_id)
            ).next()
        except StopIteration:
            raise NotFoundException(f"Ingredient {ingredient_id} usage not found for recipe {recipe_id}")
