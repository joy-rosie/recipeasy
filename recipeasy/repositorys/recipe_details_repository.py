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

    def fromRecipe(self, recipe:RecipeDetails) -> RecipeDetailsModel:
        self.id = recipe.id
        self.name = recipe.name
        return self

    def toRecipe(self) -> RecipeDetails:
        return RecipeDetails(id=self.id, name=self.name)


class RecipeDetailsRepository:

    def __init__(self):
        if not RecipeDetailsModel.exists():
            RecipeDetailsModel.create_table(wait=True)

    def createRecipeDetail(self, recipe: RecipeDetails) -> None:
        RecipeDetailsModel().fromRecipe(recipe).save()

    def getRecipeDetailById(self, id: str) -> RecipeDetails:
        return self.__getRecipeDetailModelById(id).toRecipe()

    def get_recipe_details(self) -> List[RecipeDetails]:
        return [i.toRecipe() for i in RecipeDetailsModel.scan()]

    def updateRecipeDetail(self, recipe: RecipeDetails) -> None:
        try:
            self.__getRecipeDetailModelById(recipe.id).update(actions=[
                RecipeDetailsModel.name.set(recipe.name)
            ])
        except UpdateError as e:
            raise RepositoryException("Failed to update recipe")

    def deleteRecipeDetail(self, id: str) -> None:
        try:
            self.__getRecipeDetailModelById(id).delete()
        except DeleteError as e:
            raise RepositoryException("Failed to delete recipe")

    def __getRecipeDetailModelById(self, id: str) -> RecipeDetailsModel:
        try:
            return RecipeDetailsModel.get(id)
        except DoesNotExist as e:
            raise NotFoundException("Recipe not found")