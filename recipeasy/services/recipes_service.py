from recipeasy.models.recipe import Recipe
from recipeasy.repositorys.recipes_repository import RecipesRepository
from recipeasy.repositorys.recipe_ingredients_repository import RecipeIngredientsRepository
from recipeasy.repositorys.ingredients_repository import IngredientsRepository


class RecipesService:

    def __init__(self):
        self.recipes_repository = RecipesRepository()
        self.recipe_ingredients_repository = RecipeIngredientsRepository()
        self.ingredients_repository = IngredientsRepository()

    def createRecipe(self, recipe: Recipe):
        for ingredient, quantity in recipe.ingredients.items():
            # Ensure that the ingredient exists
            self.ingredients_repository.getIngredientById(ingredient.id)
        self.recipes_repository.createRecipe(recipe)
        for ingredient, quantity in recipe.ingredients.items():
            self.recipe_ingredients_repository.addIngredientToRecipe(recipe.id, ingredient.id, quantity)

    def getRecipeById(self, id:str):
        recipe = self.recipes_repository.getRecipeById(id)
        recipe.ingredients = {}
        ingredientDict = self.recipe_ingredients_repository.getIngredientIdsForRecipe(id)
        for ingredientId, quantity in ingredientDict:
            recipe.ingredients[
                self.ingredients_repository.getIngredientById(ingredientId)
            ] = quantity

    def updateRecipe(self, recipe: Recipe):
        for ingredient, quantity in recipe.ingredients.items():
            # Ensure that the ingredient exists
            self.ingredients_repository.getIngredientById(ingredient.id)
        self.recipes_repository.updateRecipe(recipe)
        self.recipe_ingredients_repository.removeRecipe(recipe.id)
        for ingredient, quantity in recipe.ingredients.items():
            self.recipe_ingredients_repository.addIngredientToRecipe(recipe.id, ingredient.id, quantity)

    def deleteRecipe(self, id):
        self.recipes_repository.deleteRecipe(id)
        self.recipe_ingredients_repository.removeRecipe(id)