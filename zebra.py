"""
Zebra puzzle solver

This solves the classic zebra puzzle in a generic fashion. Written for the corresponding exercism
exercise. Putting here because there is no way I'm writing this again in my life.
"""

from itertools import chain
from abc import ABC
import operator
from functools import reduce, total_ordering


class Solver:
    """Solves a puzzle with given setup"""

    class Rule(ABC):
        """A single fact for the solver to consider"""

        def __init__(self, attrs):
            self.attrs = attrs

    class Exists(Rule):
        """Tells the solver that the a house has the given attribute"""

        def __init__(self, attr):
            super().__init__((attr,))

        def houses(self, solver):
            return [Solver.House(solver, [self.attrs[0]], [])]

        def spatial_update(self, solver):
            return []

    class Same(Rule):
        """Tells the solver that the given attributes are for the same house"""

        def __init__(self, first, second):
            super().__init__((first, second))

        def houses(self, solver):
            return [Solver.House(solver, self.attrs, [])]

        def spatial_update(self, solver):
            return []

    class NextTo(Rule):
        """ Tells the solver that the given attributes are for two adjacent houses"""

        def __init__(self, first, second):
            super().__init__((first, second))

        def houses(self, solver):
            return [Solver.House(solver, [self.attrs[0]], [self.attrs[1]]),
                    Solver.House(solver, [self.attrs[1]], [self.attrs[0]])]

        @staticmethod
        def _adjacents(solver, indices):
            return {i for i in chain(*((i-1, i+1) for i in indices)) if i in range(solver.size)}

        def spatial_update(self, solver):
            house1 = solver.find_house(self.attrs[0])
            house2 = solver.find_house(self.attrs[1])
            adjacents1 = Solver.NextTo._adjacents(solver, house1.data[0])
            adjacents2 = Solver.NextTo._adjacents(solver, house2.data[0])
            if house2.data[0] - adjacents1:
                house2.data[0] &= adjacents1
                return True
            if house1.data[0] - adjacents2:
                house1.data[0] &= adjacents2
                return True
            return False

    @total_ordering
    class House:
        """A fact about a house that is always true"""

        def __init__(self, solver, true_attrs, false_attrs):
            self.solver = solver
            self.data = [set() for x in solver.groups()]
            for attr in true_attrs:
                self.data[attr[0]] = {attr[1]}
            for group in solver.groups():
                if not self.data[group]:
                    self.data[group] = set(solver.attrs[group])
            for attr in false_attrs:
                self.data[attr[0]].discard(attr[1])

        def __repr__(self):
            result = f'House{tuple(self.data[0])} -> {self.precision()}'
            for line in self.data[1:]:
                result += '\n  '
                if len(line) == 1:
                    result += f'[{tuple(line)[0]}]'
                elif len(line) == self.solver.size:
                    result += '(?)'
                else:
                    result += '({})'.format(' '.join(line))
            return result

        def _summary(self):
            """Summary of the knowledge about this house"""
            return tuple((len(x), i) for i, x in enumerate(self.data))

        def precision(self):
            """Numeric value for how much knowledge this house contains"""
            return 1.0/reduce(operator.mul, (x[0] for x in self._summary()))

        def __eq__(self, other):
            """Whether two houses represent the exact same knowledge"""
            return self.data == other.data

        def __lt__(self, other):
            """More knowledge comes before less knowledge"""
            return self.precision() > other.precision()

        def __hash__(self):
            return hash(self._summary())

        def true(self, attr):
            """Return if this house definitely has the given attribute"""
            return self.data[attr[0]] == {attr[1]}

        def false(self, attr):
            """Return if this house definitely does not have the given attribute"""
            return attr[1] not in self.data[attr[0]]

        def knowns(self):
            """Return all certainly known attributes"""
            return {i: tuple(g)[0] for i, g in enumerate(self.data) if len(g) == 1}

        def falsify(self, attr):
            """Marks house as definitely not having attribute"""
            if attr[1] in self.data[attr[0]]:
                self.data[attr[0]].remove(attr[1])
                return True
            return False

        def _maybe_update_same_houses(self, other):
            """Merges facts if two houses definitely have the same single attribute"""
            for attr in self.knowns().items():
                if other.true(attr):
                    updated = False
                    for group1, group2 in zip(self.data, other.data):
                        if group1 - group2:
                            updated = True
                            group1 &= group2
                        if group2 - group1:
                            updated = True
                            group2 &= group1
                    return updated
            return False

        def _maybe_update_different_houses(self, other):
            """Updates the given house if it defiitely has a different attribute"""
            if any(not (g1 & g2) for g1, g2 in zip(self.data, other.data)):
                return (any(self.falsify(x) for x in other.knowns().items())
                        or any(other.falsify(x) for x in self.knowns().items()))

        def update(self, other):
            """Updates facts using another house"""
            return (self._maybe_update_same_houses(other)
                    or self._maybe_update_different_houses(other))

    def __init__(self, size, rules):
        self.size = size
        self.rules = rules
        self.attrs = []
        self.houses = []

        self._init_attributes()
        self._init_houses()
        self._solution_loop()

    def _init_attributes(self):
        if not self.attrs:
            self.attrs = [[] for x in self.groups()]
            self.attrs[0] = list(range(self.size))
        attrs = chain(*(x.attrs for x in self.rules))
        for attr in attrs:
            if attr[1] not in self.attrs[attr[0]]:
                self.attrs[attr[0]].append(attr[1])
        for group in self.attrs:
            if len(group) != self.size:
                raise ValueError(f'insufficient attrs: {group}')

    def _init_houses(self):
        self.houses = sorted(
            list(chain(*(r.houses(self) for r in self.rules))))

    def _simplify_houses(self):
        """Shares facts across houses and merges identical ones"""
        for house in self.houses:
            if any(house.update(x) for x in self.houses if x != house):
                self.houses = list(set(self.houses))
                return True
        return False

    def _simplify_combos(self):
        """Combine facts for two or more attributes for any uncertainty between them"""
        for house in self.houses:
            for group in self.groups():
                if len(house.data[group]) in range(2, self.size):
                    attrs = [(group, x) for x in house.data[group]]
                    others = [self.find_house(x) for x in attrs]
                    if all(others):
                        updated = False
                        for group in self.groups():
                            union = reduce(
                                set.union, (x.data[group] for x in others))
                            if house.data[group] - union:
                                house.data[group] &= union
                                updated = True
                        if updated:
                            return True
        return False

    def _add_spatial_facts(self):
        """Add houses defining spatial restrictions from the original rule set"""
        for rule in self.rules:
            if rule.spatial_update(self):
                return True
        return False

    def _solution_loop(self):
        while True:
            self.houses.sort()
            if not (self._simplify_houses()
                    # This is apparently not needed. I haven't verified fully.
                    # or self._simplify_combos()
                    or self._add_spatial_facts()):
                return

    def groups(self):
        """Numeral indices for each attribute group"""
        return range(self.size+1)

    def find_house(self, attr):
        """Returns all facts about the house with given attribute"""
        houses = [x for x in self.houses if x.true(attr)]
        if houses:
            assert len(houses) == 1, 'facts not merged'
            return houses[0]
        return None

    def find_known(self, attr, group):
        """Returns attribute for a house with another known attribute"""
        houses = [x for x in self.houses if x.true(
            attr) and group in x.knowns()]
        if houses:
            return tuple(houses[0].data[group])[0]
        return None

    def find_falses(self, attr, group):
        """Returns all impossible attributes for a house with another known attribute"""
        falses = set(self.attrs[group])
        for house in (x for x in self.houses if x.true(attr)):
            falses -= house.data[group]
        return falses


INDEX, OWNER, COLOR, PET, DRINK, SMOKE = tuple(range(6))
RULES = [
    Solver.Same((OWNER, 'Englishman'), (COLOR, 'red')),
    Solver.Same((OWNER, 'Spaniard'), (PET, 'dog')),
    Solver.Same((DRINK, 'coffee'), (COLOR, 'green')),
    Solver.Same((OWNER, 'Ukranian'), (DRINK, 'tea')),
    Solver.NextTo((COLOR, 'green'), (COLOR, 'ivory')),
    Solver.Same((SMOKE, 'Old Gold'), (PET, 'snails')),
    Solver.Same((SMOKE, 'Kools'), (COLOR, 'yellow')),
    Solver.Same((DRINK, 'milk'), (INDEX, 2)),
    Solver.Same((OWNER, 'Norwegian'), (INDEX, 0)),
    Solver.NextTo((SMOKE, 'Chesterfields'), (PET, 'fox')),
    Solver.NextTo((SMOKE, 'Kools'), (PET, 'horse')),
    Solver.Same((SMOKE, 'Lucky Strike'), (DRINK, 'orange juice')),
    Solver.Same((OWNER, 'Japanese'), (SMOKE, 'Parliaments')),
    Solver.NextTo((OWNER, 'Norwegian'), (COLOR, 'blue')),
    Solver.Exists((DRINK, 'water')),
    Solver.Exists((PET, 'zebra')),
]


print(Solver(5, RULES).find_known((DRINK, 'water'), OWNER))
print(Solver(5, RULES).find_known((PET, 'zebra'), OWNER))
