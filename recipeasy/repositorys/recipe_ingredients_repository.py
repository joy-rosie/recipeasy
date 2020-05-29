from __future__ import annotations
from typing import List

from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.exceptions import DoesNotExist, DeleteError, UpdateError
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

    def fromRecipeIngredient(self, recipeIngredient: RecipeIngredient) -> RecipeIngredientModel:
        self.recipe_id = recipeIngredient.recipe_id
        self.ingredient_id = recipeIngredient.ingredient_id
        self.quantity = recipeIngredient.quantity
        return self

    def toRecipeIngredient(self) -> RecipeIngredient:
        return RecipeIngredient(recipe_id=self.recipe_id, ingredient_id=self.ingredient_id, quantity=self.quantity)




class RecipeIngredientsRepository:

    def addIngredientToRecipe(self, recipeIngredient: RecipeIngredient) -> None:
        RecipeIngredientModel().fromRecipeIngredient(recipeIngredient).save()

    def getRecipeIngredient(self, recipe_id:str, ingredient_id:str) -> RecipeIngredient:
        return self.__getRecipeIngredientModelById(recipe_id, ingredient_id).toRecipeIngredient()

    def getRecipeIngredients(self, recipe_id:str) -> List[RecipeIngredient]:
        return [r.toRecipeIngredient() for r in RecipeIngredientModel.query(hash_key=recipe_id)]

    def updateRecipeIngredient(self, recipeIngredient: RecipeIngredient) -> None:
        try:
            self.__getRecipeIngredientModelById(recipeIngredient.recipe_id, recipeIngredient.ingredient_id).update(actions=[
                RecipeIngredientModel.quantity.set(recipeIngredient.quantity)
            ])
        except UpdateError as e:
            raise RepositoryException("Failed to update recipe ingredient")

    def removeIngredientFromRecipe(self, recipeIngredient: RecipeIngredient) -> None:
        try:
            self.__getRecipeIngredientModelById(recipeIngredient.recipe_id, recipeIngredient.ingredient_id).delete()
        except DeleteError as e:
            raise RepositoryException("Failed to delete recipe ingredient")

    def removeRecipe(self, recipe_id) -> None:
        for recipe_ingredient_model in RecipeIngredientModel.query(hash_key=recipe_id):
            try:
                recipe_ingredient_model.delete()
            except:
                # Ignore error and carry on
                pass

    def __getRecipeIngredientModelById(self, recipeId:str, ingredientId:str) -> RecipeIngredientModel:
        try:
            return RecipeIngredientModel.query(
                hash_key=recipeId,
                range_key_condition=Comparison("=", "ingredient_id", ingredientId)
            ).next()
        except StopIteration as e:
            raise NotFoundException("Ingredient usage not found")
