import pytest
from recipeasy.food import FoodState, FoodElement, Food


@pytest.mark.parametrize('inputs, expected', [
    (dict(), FoodState()),
    (dict(name='deshelled'), FoodState(name='deshelled')),
    (dict(name='cooked'), FoodState(name='cooked')),
    (dict(name='chopped'), FoodState(name='chopped')),
])
def test_food_state(inputs, expected):
    food_state = FoodState(**inputs)
    assert food_state == expected


@pytest.mark.parametrize('inputs, expected', [
    (dict(name='apple'), FoodElement(name='apple')),
    (
        dict(name='apple', state=FoodState('chopped')),
        FoodElement(name='apple', state=FoodState('chopped'))
    ),
    (
        dict(name='apple', state=FoodState('chopped'), previous=FoodElement(name='apple')),
        FoodElement(name='apple', state=FoodState('chopped'), previous=FoodElement(name='apple')),
    ),
])
def test_food_element(inputs, expected):
    food_element = FoodElement(**inputs)
    assert food_element == expected


@pytest.mark.parametrize('food_element, inputs, expected', [
    (
        FoodElement(name='apple'),
        dict(new_state=FoodState('chopped')),
        FoodElement(name='apple', state=FoodState('chopped'), previous=FoodElement(name='apple')),
    ),
])
def test_food_element_change_state(food_element, inputs, expected):
    food_element_changed_state = food_element.change_state(**inputs)
    assert food_element_changed_state == expected


@pytest.mark.parametrize('inputs, expected', [
    (
        dict(elements=frozenset({FoodElement(name='apple')})),
        Food(elements=frozenset({FoodElement(name='apple')})),
    ),
])
def test_food(inputs, expected):
    food = Food(**inputs)
    assert food == expected


@pytest.mark.parametrize('food, inputs, expected', [
    (
        Food(elements=frozenset({FoodElement(name='apple')})),
        dict(new_state=FoodState('chopped')),
        Food(
            elements=frozenset({
                FoodElement(name='apple', state=FoodState('chopped'), previous=FoodElement(name='apple')),
            }),
            previous=frozenset({Food(elements=frozenset({FoodElement(name='apple')}))}),
        ),
    ),
])
def test_food_change_state(food, inputs, expected):
    food_changed_state = food.change_state(**inputs)
    assert food_changed_state == expected


@pytest.mark.parametrize('food, inputs, expected', [
    (
        Food(elements=frozenset({FoodElement(name='apple')})),
        dict(other=Food(elements=frozenset({FoodElement(name='banana')})),),
        Food(
            elements=frozenset({
                FoodElement(name='apple'),
                FoodElement(name='banana'),
            }),
            previous=frozenset({
                Food(elements=frozenset({FoodElement(name='apple')})),
                Food(elements=frozenset({FoodElement(name='banana')})),
            }),
        ),
    ),
])
def test_food_mix(food, inputs, expected):
    food_mixed = food.mix(**inputs)
    assert food_mixed == expected


@pytest.mark.parametrize('food, inputs, expected', [
    (
        Food(elements=frozenset({FoodElement(name='apple'), FoodElement(name='banana')})),
        dict(food_element=FoodElement(name='banana')),
        Food(
            elements=frozenset({FoodElement(name='apple')}),
            previous=frozenset({Food(
                elements=frozenset({FoodElement(name='apple'), FoodElement(name='banana')}),
            )}),
        ),
    ),
])
def test_food_remove(food, inputs, expected):
    food_removed = food.remove(**inputs)
    assert food_removed == expected
