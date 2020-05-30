import uuid
from typing import List, Dict

from recipeasy.exceptions.NotFoundException import NotFoundException
from recipeasy.exceptions.ValidationException import ValidationException
from recipeasy.models.recipe import Recipe
from recipeasy.models.recipe_details import RecipeDetails
from recipeasy.models.recipe_ingredient import RecipeIngredient
from recipeasy.repositorys.ingredients_repository import IngredientsRepository
from recipeasy.repositorys.recipe_details_repository import RecipeDetailsRepository
from recipeasy.repositorys.recipe_ingredients_repository import RecipeIngredientsRepository


class RecipeService:

    def __init__(self):
        self.recipe_details_repository = RecipeDetailsRepository()
        self.recipe_ingredients_repository = RecipeIngredientsRepository()
        self.ingredients_repository = IngredientsRepository()

    def create_recipe(self, recipe: Recipe) -> Recipe:
        if recipe.id != "":
            raise ValidationException("Id must not be provided for create recipe")
        recipe.id = str(uuid.uuid4())
        for ingredient_id, _ in recipe.ingredients.items():
            try:
                self.ingredients_repository.get_ingredient_by_id(ingredient_id)
            except NotFoundException:
                raise ValidationException("Ingredient id provided does not exist")
        recipe_detail = RecipeDetails(
            id=recipe.id,
            name=recipe.name
        )
        self.recipe_details_repository.create_recipe_detail(recipe_detail)
        recipe_ingredients = [RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ingredient_id,
            quantity=quantity
        ) for ingredient_id, quantity in recipe.ingredients.items()]
        for recipe_ingredient in recipe_ingredients:
            self.recipe_ingredients_repository.upsert_ingredient_to_recipe(recipe_ingredient)
        return recipe

    def get_recipe_by_id(self, recipe_id) -> Recipe:
        recipe_detail = self.recipe_details_repository.get_recipe_detail_by_id(recipe_id)
        recipe_ingredients = self.recipe_ingredients_repository.get_recipe_ingredients(recipe_id)
        return Recipe(
            id=recipe_detail.id,
            name=recipe_detail.name,
            ingredients={ri.ingredient_id: ri.quantity for ri in recipe_ingredients}
        )

    def update_recipe(self, recipe: Recipe) -> Recipe:
        if recipe.id == "":
            raise ValidationException("Id must be provided for create recipe")
        for ingredient_id, _ in recipe.ingredients.items():
            try:
                self.ingredients_repository.get_ingredient_by_id(ingredient_id)
            except NotFoundException:
                raise ValidationException("Ingredient id provided does not exist")
        recipe_detail = RecipeDetails(
            id=recipe.id,
            name=recipe.name
        )
        self.recipe_details_repository.update_recipe_detail(recipe_detail)

        old_recipe_ingredient_ids = [ri.ingredient_id for ri in
                                     self.recipe_ingredients_repository.get_recipe_ingredients(recipe.id)]
        ingredient_ids_to_delete = [recipe_id for recipe_id in old_recipe_ingredient_ids if
                                    recipe_id not in recipe.ingredients]
        for ingredient_id_to_delete in ingredient_ids_to_delete:
            self.recipe_ingredients_repository.remove_ingredient_from_recipe(recipe.id, ingredient_id_to_delete)
        for ingredient_id, quantity in recipe.ingredients.items():
            self.recipe_ingredients_repository.upsert_ingredient_to_recipe(RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient_id,
                quantity=quantity
            ))
        return recipe

    def delete_recipe(self, recipe_id) -> None:
        self.recipe_ingredients_repository.remove_recipe(recipe_id)
        self.recipe_details_repository.delete_recipe_detail(recipe_id)

    def get_total_ingredients(self, recipe_ids: List[str]) -> Dict[str, float]:
        total_ingredients = {}
        for recipe_id in recipe_ids:
            self.recipe_details_repository.get_recipe_detail_by_id(recipe_id)  # check recipe exists first
            recipe_ingredients = self.recipe_ingredients_repository.get_recipe_ingredients(recipe_id)
            for recipe_ingredient in recipe_ingredients:
                if recipe_ingredient.ingredient_id not in total_ingredients:
                    total_ingredients[recipe_ingredient.ingredient_id] = 0
                total_ingredients[recipe_ingredient.ingredient_id] += recipe_ingredient.quantity
        return total_ingredients
