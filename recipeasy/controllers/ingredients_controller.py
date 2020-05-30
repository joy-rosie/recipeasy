from flask import Blueprint, request, jsonify

from recipeasy.models.ingredient import Ingredient
from recipeasy.services.ingredients_service import IngredientsService

ingredients_service = IngredientsService()
controller = Blueprint('ingredients_controller', __name__)




@controller.route('', methods=['POST'])
def createIngredient():
    return jsonify(
        ingredients_service.createIngredient(Ingredient.fromJson(request.json))
    )

@controller.route('/<ingredient_id>', methods=['GET'])
def getIngredient(ingredient_id: str):
    return jsonify(
        ingredients_service.getIngredientById(ingredient_id)
    )

@controller.route('/all', methods=['GET'])
def getAllIngredients():
    return jsonify(
        ingredients_service.get_ingredients()
    )

@controller.route('', methods=['PUT'])
def updateIngredient():
    return jsonify(
        ingredients_service.updateIngredient(Ingredient.fromJson(request.json))
    )

@controller.route('/<ingredient_id>', methods=['DELETE'])
def deleteIngredient(ingredient_id: str):
    ingredients_service.deleteIngredient(ingredient_id)
    return jsonify(
        success=True
    )
