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

    def fromIngredient(self, ingredient:Ingredient) -> IngredientModel:
        self.id = ingredient.id
        self.name = ingredient.name
        return self

    def toIngredient(self) -> Ingredient:
        return Ingredient(id=self.id, name=self.name)


class IngredientsRepository:

    def __init__(self):
        if not IngredientModel.exists():
            IngredientModel.create_table(wait=True)

    def createIngredient(self, ingredient:Ingredient) -> None:
        IngredientModel().fromIngredient(ingredient).save()

    def getIngredientById(self, id: str) -> Ingredient:
        return self.__getIngredientModelById(id).toIngredient()

    def get_ingredients(self) -> List[Ingredient]:
        return [i.toIngredient() for i in IngredientModel.scan()]

    def updateIngredient(self, ingredient: Ingredient) -> None:
        try:
            self.__getIngredientModelById(ingredient.id).update(actions=[
                IngredientModel.name.set(ingredient.name)
            ])
        except UpdateError as e:
            raise RepositoryException("Failed to update ingredient")

    def deleteIngredient(self, id: str) -> None:
        try:
            self.__getIngredientModelById(id).delete()
        except DeleteError as e:
            raise RepositoryException("Failed to delete ingredient")

    def __getIngredientModelById(self, id:str) -> IngredientModel:
        try:
            return IngredientModel.get(id)
        except DoesNotExist as e:
            raise NotFoundException("Ingredient not found")