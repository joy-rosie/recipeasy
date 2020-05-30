import uuid
from typing import List

from recipeasy.exceptions.ValidationException import ValidationException
from recipeasy.models.ingredient import Ingredient
from recipeasy.repositorys.ingredients_repository import IngredientsRepository


class IngredientsService:

    def __init__(self):
        self.ingredientsRepository = IngredientsRepository()

    def createIngredient(self, ingredient:Ingredient) -> Ingredient:
        """
        :raises ValidationException if id provided
        """
        if ingredient.id != "":
            raise ValidationException("Id must not be provided for create ingredient")
        ingredient.id = str(uuid.uuid4())
        self.ingredientsRepository.createIngredient(ingredient)
        return ingredient

    def getIngredientById(self, id: str) -> Ingredient:
        """
        :raises: NotFoundException if ingredient not found
        """
        return self.ingredientsRepository.getIngredientById(id)

    def get_ingredients(self) -> List[Ingredient]:
        return self.ingredientsRepository.get_ingredients()

    def updateIngredient(self, ingredient: Ingredient) -> Ingredient:
        """
        :raises: ValidationException if ingredient id not provided
        :raises: NotFoundException if ingredient id not found
        """
        if ingredient.id != "":
            raise ValidationException("Id must be provided for create ingredient")
        self.ingredientsRepository.updateIngredient(ingredient)
        return ingredient

    def deleteIngredient(self, id: str) -> None:
        """
        :raises: NotFoundException if ingredient id not found
        """
        # TODO: should add a check that no recipes use this ingredient (in which case return 422)
        self.ingredientsRepository.deleteIngredient(id)