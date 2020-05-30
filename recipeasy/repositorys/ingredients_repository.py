from __future__ import annotations
from typing import List

from pynamodb.attributes import UnicodeAttribute
from pynamodb.exceptions import DoesNotExist, UpdateError, DeleteError
from pynamodb.models import Model

from recipeasy.exceptions.NotFoundException import NotFoundException
from recipeasy.exceptions.RepositoryException import RepositoryException
from recipeasy.models.ingredient import Ingredient


class IngredientModel(Model):
    class Meta:
        table_name = "ingredients_v1"
        region = "eu-west-1"
        write_capacity_units = 10
        read_capacity_units = 10

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()

    def from_ingredient(self, ingredient: Ingredient) -> IngredientModel:
        self.id = ingredient.id
        self.name = ingredient.name
        return self

    def to_ingredient(self) -> Ingredient:
        return Ingredient(id=self.id, name=self.name)


class IngredientsRepository:

    def __init__(self):
        if not IngredientModel.exists():
            IngredientModel.create_table(wait=True)

    def create_ingredient(self, ingredient: Ingredient) -> None:
        IngredientModel().from_ingredient(ingredient).save()

    def get_ingredient_by_id(self, ingredient_id: str) -> Ingredient:
        return self.__get_ingredient_model_by_id(ingredient_id).to_ingredient()

    def get_ingredients(self) -> List[Ingredient]:
        return [i.to_ingredient() for i in IngredientModel.scan()]

    def update_ingredient(self, ingredient: Ingredient) -> None:
        try:
            self.__get_ingredient_model_by_id(ingredient.id).update(actions=[
                IngredientModel.name.set(ingredient.name)
            ])
        except UpdateError:
            raise RepositoryException(f"Failed to update ingredient {ingredient.id}")

    def delete_ingredient(self, ingredient_id: str) -> None:
        try:
            self.__get_ingredient_model_by_id(ingredient_id).delete()
        except DeleteError:
            raise RepositoryException(f"Failed to delete ingredient {ingredient_id}")

    def __get_ingredient_model_by_id(self, ingredient_id: str) -> IngredientModel:
        try:
            return IngredientModel.get(ingredient_id)
        except DoesNotExist:
            raise NotFoundException(f"Ingredient {ingredient_id} not found")
