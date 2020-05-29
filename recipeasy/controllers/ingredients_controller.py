from flask import Blueprint, request, abort, jsonify

from recipeasy.exceptions.BadRequestException import BadRequestException
from recipeasy.models.ingredient import Ingredient
from recipeasy.services.ingredients_service import IngredientsService


ingredients_service = IngredientsService()
controller = Blueprint('ingredients_controller', __name__)




#  curl -i localhost:5000/ingredients -X POST -d '{"name": "custom name"}'  -H 'Content-Type: application/json'

@controller.route('/', methods=['POST'])
def createIngredient():
    if not request.json:
        raise BadRequestException("No request body provided")
    if request.json["id"] is not None:
        raise BadRequestException("Id cannot be provided")
    if request.json["name"] is None:
        raise BadRequestException("Name must be provided")
    return jsonify(
        ingredients_service.createIngredient(Ingredient(
            id="",
            name=request.json["name"]
        ))
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

@controller.route('/', methods=['PUT'])
def updateIngredient():
    if not request.json:
        raise BadRequestException("No request body provided")
    if request.json["id"] is None:
        raise BadRequestException("Id must be provided")
    if request.json["name"] is None:
        raise BadRequestException("Name must be provided")
    return jsonify(
        ingredients_service.updateIngredient(Ingredient(
            id = request.json["id"],
            name = request.json["name"]
        ))
    )

@controller.route('/<ingredient_id>', methods=['DELETE'])
def deleteIngredient(ingredient_id: str):
    ingredients_service.deleteIngredient(ingredient_id)
    return jsonify(
        success=True
    )
