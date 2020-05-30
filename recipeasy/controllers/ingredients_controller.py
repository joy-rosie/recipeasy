from flask import Blueprint, request, jsonify

from recipeasy.exceptions.ValidationException import ValidationException
from recipeasy.models.ingredient import Ingredient
from recipeasy.services.ingredients_service import IngredientsService

ingredients_service = IngredientsService()
controller = Blueprint('ingredients_controller', __name__)


@controller.route('', methods=['POST'])
def create_ingredient():
    if not request.json:
        raise ValidationException("Request body is expected")
    return jsonify(
        ingredients_service.create_ingredient(Ingredient.from_json(request.json))
    )


@controller.route('/<ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id: str):
    return jsonify(
        ingredients_service.get_ingredient_by_id(ingredient_id)
    )


@controller.route('/all', methods=['GET'])
def get_all_ingredients():
    return jsonify(
        ingredients_service.get_ingredients()
    )


@controller.route('', methods=['PUT'])
def update_ingredient():
    if not request.json:
        raise ValidationException("Request body is expected")
    return jsonify(
        ingredients_service.update_ingredient(Ingredient.from_json(request.json))
    )


@controller.route('/<ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id: str):
    ingredients_service.delete_ingredient(ingredient_id)
    return jsonify(
        success=True
    )
