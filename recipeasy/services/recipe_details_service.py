from typing import List

from recipeasy.models.recipe_details import RecipeDetails
from recipeasy.repositorys.recipe_details_repository import RecipeDetailsRepository


class RecipeDetailsService:

    def __init__(self):
        self.recipe_details_repository = RecipeDetailsRepository()

    def getRecipeDetails(self) -> List[RecipeDetails]:
        return self.recipe_details_repository.get_recipe_details()
