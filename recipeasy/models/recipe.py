from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

from recipeasy.exceptions.ValidationException import ValidationException


@dataclass
class Recipe:
    id: str
    name: str
    ingredients: Dict[str, float]

    @staticmethod
    def from_json(json) -> Recipe:
        if "name" not in json:
            raise ValidationException("Recipe name must be provided")
        return Recipe(
            id=json["id"] if "id" in json else "",
            name=json["name"],
            ingredients=json["ingredients"] if "ingredients" in json else {}
        )
