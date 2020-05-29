from __future__ import annotations
from typing import Dict, List

from pynamodb.attributes import UnicodeAttribute
from pynamodb.exceptions import DoesNotExist, DeleteError, UpdateError
from pynamodb.models import Model

from recipeasy.exceptions.NotFoundException import NotFoundException
from recipeasy.exceptions.RepositoryException import RepositoryException
from recipeasy.models.recipe import Recipe

class RecipeModel(Model):
    class Meta:
        table_name = "recipe_v1"
        region = "eu-west-1"
        write_capacity_units = 10
        read_capacity_units = 10

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()

    def fromRecipe(self, recipe:Recipe) -> RecipeModel:
        self.id = recipe.id
        self.name = recipe.name
        return self

    def toRecipe(self) -> Recipe:
        return Recipe(id=self.id, name=self.name)


class RecipesRepository:

    def __init__(self):
        if not RecipeModel.exists():
            RecipeModel.create_table(wait=True)

    def createRecipe(self, recipe: Recipe) -> None:
        RecipeModel().fromRecipe(recipe).save()

    def getRecipeById(self, id: str) -> Recipe:
        return self.__getRecipeModelById(id).toRecipe()

    def get_recipes(self) -> List[Recipe]:
        return [i.toRecipe() for i in RecipeModel.scan()]

    def updateRecipe(self, recipe: Recipe) -> None:
        try:
            self.__getRecipeModelById(recipe.id).update(actions=[
                RecipeModel.name.set(recipe.name)
            ])
        except UpdateError as e:
            raise RepositoryException("Failed to update recipe")

    def deleteRecipe(self, id: str) -> None:
        try:
            self.__getRecipeModelById(id).delete()
        except DeleteError as e:
            raise RepositoryException("Failed to delete recipe")

    def __getRecipeModelById(self, id: str) -> RecipeModel:
        try:
            return RecipeModel.get(id)
        except DoesNotExist as e:
            raise NotFoundException("Recipe not found")