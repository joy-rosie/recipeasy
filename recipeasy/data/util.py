from typing import Optional, Tuple, Dict, List, NoReturn
from dataclasses import dataclass
import os
import json
import csv
import copy
from recipeasy.food import FoodElement


@dataclass(frozen=True)
class FoodElementWithData(FoodElement):
    cofid_food_code: Optional[str] = None
    description: Optional[str] = None
    all_names: Optional[Tuple[str]] = None


def get_foods(
        path: Optional[str] = None,
        **kwargs
) -> Dict[str, FoodElementWithData]:

    if path is None:
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'food.json')

    _, file_extension = os.path.splitext(path)

    if file_extension == '.json':
        raw_food_data = get_raw_foods_from_json(path=path, **kwargs)
    elif file_extension == '.csv':
        raw_food_data = get_raw_foods_from_json(path=path, **kwargs)
    else:
        raise NotImplementedError(f'File extension "{file_extension}" not yet implemented.')

    for index, item in enumerate(raw_food_data):
        raw_food_data[index]['all_names'] = tuple(item['all_names'])

    food_data = {item['all_names']: FoodElementWithData(**item) for item in raw_food_data}

    food_data = {item: value for key, value in food_data.items() for item in key}

    return food_data


def get_raw_foods_from_json(
        path: Optional[str] = None,
        **kwargs,
) -> List[Dict]:

    if path is None:
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'food.json')

    with open(path, 'r') as json_file:
        raw_food_data = json.load(json_file)

    return raw_food_data


def raw_foods_to_json(
        raw_food_data: List[Dict],
        path: Optional[str] = None,
        **kwargs,
) -> NoReturn:

    if path is None:
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'food.json')

    with open(path, 'w') as json_file:
        json.dump(raw_food_data, json_file)


def get_raw_foods_from_csv(
        path: Optional[str] = None,
        delimiter: Optional[str] = None,
        **kwargs,
) -> List[Dict]:

    if path is None:
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'food.csv')

    if delimiter is None:
        delimiter = '|'

    raw_food_data = []
    with open(path, 'r', newline='') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            row['all_names'] = row['all_names'].split(', ')
            raw_food_data.append(row)

    return raw_food_data


def raw_foods_to_csv(
        raw_food_data: List[Dict],
        path: Optional[str] = None,
        delimiter: Optional[str] = None,
        **kwargs,
) -> NoReturn:

    if path is None:
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'food.csv')

    raw_food_data_dump = copy.deepcopy(raw_food_data)

    for index, item in enumerate(raw_food_data_dump):
        raw_food_data_dump[index]['all_names'] = ', '.join(item['all_names'])

    csv_header = list(raw_food_data_dump[0].keys())

    with open(path, 'w') as f:
        dw = csv.DictWriter(f, delimiter=delimiter, fieldnames=csv_header)
        dw.writerow(dict((fn, fn) for fn in csv_header))
        for row in raw_food_data_dump:
            dw.writerow(row)
