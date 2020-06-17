from typing import Optional, Tuple, Dict
from dataclasses import dataclass, field
import os
import json
from recipeasy.food import FoodElement


@dataclass(frozen=True)
class FoodElementWithData(FoodElement):
    cofid_food_code: Optional[str] = None
    description: Optional[str] = None
    alternative_names: Optional[Tuple[str]] = field(default_factory=tuple())


def get_foods(path: Optional[str] = None) -> Dict[str, FoodElementWithData]:

    if path is None:
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'food.json')

    with open(path, 'r') as json_file:
        food_data = json.load(json_file)

    for index, item in enumerate(food_data):
        if item['alternative_names'][0] == '':
            food_data[index]['alternative_names'] = tuple()
        else:
            food_data[index]['alternative_names'] = tuple(item['alternative_names'])

    food_data = {item['name']: FoodElementWithData(**item) for item in food_data}

    return food_data
