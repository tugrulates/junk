"""
Zebra puzzle solver

This solves the classic zebra puzzle in a generic fashion. Written for the corresponding exercism
exercise.
"""

from __future__ import annotations

from functools import total_ordering
from itertools import combinations
from typing import Iterable


class Solver:
    """Solves a puzzle with given setup."""

    @total_ordering
    class House:
        """A single house in the puzzle with known attributes."""

        def __init__(self, **attrs: str | int) -> None:
            """Initialize the house with a list of attributes."""
            self.attrs = {k: {str(v)} for k, v in attrs.items()}

        def same(self, other: Solver.House) -> bool:
            """Check if two houses are the same."""
            return any(
                len(self.attrs[attr]) == 1 and self.attrs[attr] == other.attrs[attr]
                for attr in self.attrs
            )

        def different(self, other: Solver.House) -> bool:
            """Check if two houses are different."""
            return any(
                len(self.attrs[attr] & other.attrs[attr]) == 0 for attr in self.attrs
            )

        def merge(self, other: Solver.House) -> bool:
            """Merge two houses into one."""
            attrs = {attr: self.attrs[attr] & other.attrs[attr] for attr in self.attrs}
            if self.attrs != attrs:
                self.attrs = attrs
                return True
            return False

        def exclude(self, other: Solver.House) -> bool:
            """Update the house with the attributes from a separate house."""
            attrs = {
                attr: self.attrs[attr] - other.attrs[attr]
                if len(other.attrs[attr]) == 1
                else self.attrs[attr]
                for attr in self.attrs
            }
            if self.attrs != attrs:
                self.attrs = attrs
                return True
            return False

        def move_next_to(self, other: Solver.House) -> bool:
            """Update house to be next to other house."""
            indices = self.attrs["index"] & (
                {str(int(i) - 1) for i in other.attrs["index"]}
                | {str(int(i) + 1) for i in other.attrs["index"]}
            )
            if self.attrs["index"] != indices:
                self.attrs["index"] = indices
                return True
            return False

        def __eq__(self, value: object) -> bool:
            """Check if two houses are equal."""
            if not isinstance(value, Solver.House):
                return NotImplemented
            return self.attrs == value.attrs

        def __le__(self, value: object) -> bool:
            """Check if a house has more precision than the other."""
            if not isinstance(value, Solver.House):
                return NotImplemented
            return sum(map(len, self.attrs.values())) <= sum(
                map(len, value.attrs.values())
            )

    Neighbors = tuple[House, House]

    def __init__(self, rules: Iterable[Solver.House | Solver.Neighbors]) -> None:
        """Initialize the solver with the size and rules."""
        self.houses: list[Solver.House] = []
        self.neighbors: list[Solver.Neighbors] = []
        self.attrs: dict[str, set[str]] = {}

        for rule in rules:
            if isinstance(rule, Solver.House):
                self.houses.append(rule)
            elif isinstance(rule, tuple):
                self.houses.extend([*rule])
                self.neighbors.extend([rule, rule[::-1]])

        for house in self.houses:
            for attr in house.attrs:
                self.attrs.setdefault(attr, set())
                self.attrs[attr] |= house.attrs[attr]
        sizes = {len(value) for attr, value in self.attrs.items() if attr != "index"}
        assert len(sizes) == 1, "Invalid puzzle setup."
        self.size = sizes.pop()
        self.attrs["index"] = set(map(str, range(1, self.size + 1)))

        for house in self.houses:
            for attr in self.attrs:
                house.attrs.setdefault(attr, self.attrs[attr])

        while self._solve():
            pass

    def _solve(self) -> bool:
        """Solve the puzzle by iteratively merging known facts."""
        self.houses.sort()
        for house, other in combinations(self.houses, 2):
            if house.same(other):
                house.merge(other)
                self.houses.remove(other)
                return True
            if house.different(other) and (
                house.exclude(other) or other.exclude(house)
            ):
                return True
            if any(house.same(a) and other.same(b) for a, b in self.neighbors) and (
                house.move_next_to(other) or other.move_next_to(house)
            ):
                return True
        return False

    def find(self, attr: str, **attrs: str) -> str:
        """Find the house with the given attributes."""
        search = Solver.House(**attrs)
        found = [house for house in self.houses if search.same(house)]
        if not found:
            raise ValueError("No house found")
        if len(found) > 1:
            raise ValueError("Multiple houses found")
        return found.pop().attrs[attr].pop()


KNOWN = (
    Solver.House(owner="Englishman", color="red"),
    Solver.House(owner="Spaniard", pet="dog"),
    Solver.House(color="green", drink="coffee"),
    Solver.House(owner="Ukranian", drink="tea"),
    (Solver.House(color="green"), Solver.House(color="ivory")),
    Solver.House(pet="snail", hobby="dancing"),
    Solver.House(color="yellow", hobby="painting"),
    Solver.House(index=3, drink="milk"),
    Solver.House(owner="Norwegian", index=1),
    (Solver.House(hobby="reading"), Solver.House(pet="fox")),
    (Solver.House(hobby="painting"), Solver.House(pet="horse")),
    Solver.House(hobby="football", drink="orange juice"),
    Solver.House(owner="Japanese", hobby="chess"),
    (Solver.House(owner="Norwegian"), Solver.House(color="blue")),
    Solver.House(drink="water"),
    Solver.House(pet="zebra"),
)


print(Solver(KNOWN).find("owner", drink="water"))
print(Solver(KNOWN).find("owner", pet="zebra"))
