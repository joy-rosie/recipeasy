from recipeasy.models.ingredient import Ingredient


def test_Ingredient_init():
    ing = Ingredient(id='1', name='test')
    assert isinstance(ing, Ingredient) and ing.name == 'test'
