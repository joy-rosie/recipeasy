from flask import Blueprint, jsonify, request

from recipeasy.exceptions.ValidationException import ValidationException
from recipeasy.models.recipe import Recipe
from recipeasy.services.ingredients_service import IngredientsService
from recipeasy.services.recipe_details_service import RecipeDetailsService
from recipeasy.services.recipe_service import RecipeService

recipes_service = RecipeService()
recipe_details_service = RecipeDetailsService()
ingredients_service = IngredientsService()

controller = Blueprint('recipes_controller', __name__)


@controller.route('/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id: str):
    return jsonify(
        recipes_service.get_recipe_by_id(recipe_id)
    )


@controller.route('', methods=['POST'])
def create_recipe():
    if not request.json:
        raise ValidationException("Request body is expected")
    return jsonify(
        recipes_service.create_recipe(Recipe.from_json(request.json))
    )


@controller.route('', methods=['PUT'])
def update_recipe():
    if not request.json:
        raise ValidationException("Request body is expected")
    return jsonify(
        recipes_service.update_recipe(Recipe.from_json(request.json))
    )


@controller.route('/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id: str):
    recipes_service.delete_recipe(recipe_id)
    return jsonify(
        success=True
    )


@controller.route('/names', methods=['GET'])
def get_all_recipe_details():
    return jsonify(
        recipe_details_service.get_recipe_details()
    )


@controller.route('/totalIngredients', methods=['GET'])
def get_total_ingredients():
    if not request.json:
        raise ValidationException("Request body is expected")
    if "recipe_ids" not in request.json:
        raise ValidationException("recipe_ids not provided")
    return jsonify(
        recipes_service.get_total_ingredients(request.json["recipe_ids"])
    )
