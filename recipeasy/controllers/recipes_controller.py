from flask import Blueprint
from recipeasy.services.recipes_service import RecipesService


recipes_service: RecipesService = None

def setRecipesService(recipesService: RecipesService) -> None:
    global recipes_service
    recipes_service = recipesService

controller = Blueprint('recipes_controller', __name__)


@controller.route('/<recipe_id>', methods=['GET'])
def getRecipe(recipe_id: str):
    return recipes_service.getRecipeById(recipe_id)

# TODO

