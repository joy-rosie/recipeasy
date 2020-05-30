from __future__ import annotations

from typing import List

from pynamodb.attributes import UnicodeAttribute
from pynamodb.exceptions import DoesNotExist, DeleteError, UpdateError
from pynamodb.models import Model

from recipeasy.exceptions.NotFoundException import NotFoundException
from recipeasy.exceptions.RepositoryException import RepositoryException
from recipeasy.models.recipe_details import RecipeDetails


class RecipeDetailsModel(Model):
    class Meta:
        table_name = "recipe_details_v1"
        region = "eu-west-1"
        write_capacity_units = 10
        read_capacity_units = 10

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()

    def from_recipe(self, recipe: RecipeDetails) -> RecipeDetailsModel:
        self.id = recipe.id
        self.name = recipe.name
        return self

    def to_recipe(self) -> RecipeDetails:
        return RecipeDetails(id=self.id, name=self.name)


class RecipeDetailsRepository:

    def __init__(self):
        if not RecipeDetailsModel.exists():
            RecipeDetailsModel.create_table(wait=True)

    def create_recipe_detail(self, recipe: RecipeDetails) -> None:
        RecipeDetailsModel().from_recipe(recipe).save()

    def get_recipe_detail_by_id(self, recipe_id: str) -> RecipeDetails:
        return self.__get_recipe_detail_model_by_id(recipe_id).to_recipe()

    def get_recipe_details(self) -> List[RecipeDetails]:
        return [i.to_recipe() for i in RecipeDetailsModel.scan()]

    def update_recipe_detail(self, recipe: RecipeDetails) -> None:
        try:
            self.__get_recipe_detail_model_by_id(recipe.id).update(actions=[
                RecipeDetailsModel.name.set(recipe.name)
            ])
        except UpdateError:
            raise RepositoryException(f"Failed to update recipe {recipe.id}")

    def delete_recipe_detail(self, recipe_id: str) -> None:
        try:
            self.__get_recipe_detail_model_by_id(recipe_id).delete()
        except DeleteError:
            raise RepositoryException(f"Failed to delete recipe {recipe_id}")

    def __get_recipe_detail_model_by_id(self, recipe_id: str) -> RecipeDetailsModel:
        try:
            return RecipeDetailsModel.get(recipe_id)
        except DoesNotExist:
            raise NotFoundException(f"Recipe {recipe_id} not found")
