from __future__ import annotations
from dataclasses import dataclass

from recipeasy.exceptions.ValidationException import ValidationException


@dataclass
class Ingredient:
    id: str
    name: str

    @staticmethod
    def fromJson(json) -> Ingredient:
        if "name" not in json:
            raise ValidationException("Ingredient name must be provided")
        return Ingredient(
            id = json["id"] if "id" in json else "",
            name = json["name"]
        )
