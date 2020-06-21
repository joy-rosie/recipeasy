# import pytest

import recipeasy.data.util as data_util


def test_get_foods():
    food_data = data_util.get_foods()
    assert isinstance(food_data, dict)
