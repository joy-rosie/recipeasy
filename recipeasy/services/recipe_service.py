import uuid

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
        self.recipe_ingredients_respository = RecipeIngredientsRepository()
        self.ingredients_repository = IngredientsRepository()

    def createRecipe(self, recipe:Recipe) -> Recipe:
        if recipe.id != "":
            raise ValidationException("Id must not be provided for create recipe")
        recipe.id = str(uuid.uuid4())
        for ingredient_id, _ in recipe.ingredients.items():
            try:
                self.ingredients_repository.getIngredientById(ingredient_id)
            except NotFoundException as e:
                raise ValidationException("Ingredient id provided does not exist")
        recipe_detail = RecipeDetails(
            id=recipe.id,
            name=recipe.name
        )
        self.recipe_details_repository.createRecipeDetail(recipe_detail)
        recipe_ingredients = [RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ingredient_id,
            quantity=quantity
        ) for ingredient_id, quantity in recipe.ingredients.items()]
        for recipe_ingredient in recipe_ingredients:
            self.recipe_ingredients_respository.upsertIngredientToRecipe(recipe_ingredient)
        return recipe

    def getRecipeById(self, id) -> Recipe:
        recipe_detail = self.recipe_details_repository.getRecipeDetailById(id)
        recipe_ingredients = self.recipe_ingredients_respository.getRecipeIngredients(id)
        return Recipe(
            id=recipe_detail.id,
            name=recipe_detail.name,
            ingredients={ri.ingredient_id: ri.quantity for ri in recipe_ingredients}
        )

    def updateRecipe(self, recipe: Recipe) -> Recipe:
        if recipe.id == "":
            raise ValidationException("Id must be provided for create recipe")
        for ingredient_id, _ in recipe.ingredients.items():
            try:
                self.ingredients_repository.getIngredientById(ingredient_id)
            except NotFoundException as e:
                raise ValidationException("Ingredient id provided does not exist")
        recipe_detail = RecipeDetails(
            id=recipe.id,
            name=recipe.name
        )
        self.recipe_details_repository.updateRecipeDetail(recipe_detail)

        old_recipe_ingredient_ids = [ri.ingredient_id for ri in self.recipe_ingredients_respository.getRecipeIngredients(recipe.id)]
        ingredient_ids_to_delete = [id for id in old_recipe_ingredient_ids if id not in recipe.ingredients]
        for ingredient_id_to_delete in ingredient_ids_to_delete:
            self.recipe_ingredients_respository.removeIngredientFromRecipe(recipe.id, ingredient_id_to_delete)
        for ingredient_id, quantity in recipe.ingredients.items():
            self.recipe_ingredients_respository.upsertIngredientToRecipe(RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient_id,
                quantity=quantity
            ))
        return recipe

    def deleteRecipe(self, id) -> None:
        self.recipe_ingredients_respository.removeRecipe(id)
        self.recipe_details_repository.deleteRecipeDetail(id)

