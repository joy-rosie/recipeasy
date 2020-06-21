import pytest
import recipeasy

@pytest.mark.parametrize('inputs, expected', [
    ({'string': 'apple'}, 'apple'),
    ({'string': '3 grams of salt'}, 'salt'),
    ({'string': '3 grams of television'}, 'no matching ingredient found!'),
])
def test_getIngredient(inputs, expected):
    food = recipeasy.foodLink.getIngredient(**inputs)
    assert food == expected


