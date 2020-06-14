from __future__ import annotations
from typing import FrozenSet
from dataclasses import dataclass, field


@dataclass(frozen=True)
class FoodState:
    name: str = 'atomic'


@dataclass(frozen=True)
class FoodElement:
    name: str
    state: FoodState = FoodState()
    previous: FoodElement = field(default=None, repr=False)

    def change_state(self, new_state: FoodState):
        return FoodElement(name=self.name, state=new_state, previous=self)


@dataclass(frozen=True)
class Food:
    elements: FrozenSet[FoodElement]
    previous: FrozenSet[Food] = field(default=None, repr=False)

    def change_state(self, new_state: FoodState):
        return Food(
            elements=frozenset({element.change_state(new_state=new_state) for element in self.elements}),
            previous=frozenset({self}),
        )

    def mix(self, other):
        return Food(
            elements=frozenset().union(*[self.elements, other.elements]),
            previous=frozenset({self, other}),
        )

    def remove(self, food_element):
        elements = set(self.elements)
        elements.remove(food_element)
        return Food(elements=frozenset(elements), previous=frozenset({self}))
