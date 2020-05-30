from flask import Blueprint, jsonify, request

from recipeasy.models.recipe import Recipe
from recipeasy.services.ingredients_service import IngredientsService
from recipeasy.services.recipe_service import RecipeService

recipes_service = RecipeService()
ingredients_service = IngredientsService()

controller = Blueprint('recipes_controller', __name__)


@controller.route('/<recipe_id>', methods=['GET'])
def getRecipe(recipe_id: str):
    return jsonify(
        recipes_service.getRecipeById(recipe_id)
    )

@controller.route('', methods=['POST'])
def createRecipe():
    return jsonify(
        recipes_service.createRecipe(Recipe.fromJson(request.json))
    )

@controller.route('', methods=['PUT'])
def updateRecipe():
    return jsonify(
        recipes_service.updateRecipe(Recipe.fromJson(request.json))
    )


@controller.route('/<recipe_id>', methods=['DELETE'])
def deleteRecipe(recipe_id:str):
    recipes_service.deleteRecipeDetails(recipe_id)
    return jsonify(
        success=True
    )

# TODO

