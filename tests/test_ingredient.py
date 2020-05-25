from recipeasy import ingredient


def test_Ingredient_init():
    ing = ingredient.Ingredient(name='test')
    assert isinstance(ing, ingredient.Ingredient) and ing.name == 'test'
