import uuid
from typing import List

from recipeasy.models.ingredient import Ingredient
from recipeasy.repositorys.ingredients_repository import IngredientsRepository


class IngredientsService:

    def __init__(self):
        self.ingredientsRepository = IngredientsRepository()

    def createIngredient(self, ingredient:Ingredient) -> Ingredient:
        """
        :return: None
        """
        ingredient.id = str(uuid.uuid4())
        self.ingredientsRepository.createIngredient(ingredient)
        return ingredient

    def getIngredientById(self, id: str) -> Ingredient:
        """
        :return: Ingredient object if found
        :raises: NotFoundException if ingredient not found
        """
        return self.ingredientsRepository.getIngredientById(id)

    def get_ingredients(self) -> List[Ingredient]:
        """
        :return: List of ingredients in database
        """
        return self.ingredientsRepository.get_ingredients()

    def updateIngredient(self, ingredient: Ingredient) -> Ingredient:
        """
        :return: None
        :raises: NotFoundException if ingredient id not found
        """
        self.ingredientsRepository.updateIngredient(ingredient)
        return ingredient

    def deleteIngredient(self, id: str) -> None:
        """
        :return: None
        :raises: NotFoundException if ingredient id not found
        """
        # TODO: should add a check that no recipes use this ingredient (in which case return 422)
        self.ingredientsRepository.deleteIngredient(id)