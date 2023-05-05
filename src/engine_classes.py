from math_classes import *


class Ray:
    def __init__(self, cs: CoordinateSystem, initial_pt: Point, direction: Vector):
        self.cs = cs
        self.initial_pt = initial_pt
        self.direction = direction


class Identifier:
    def __init__(self):
        if len(self) != 1:
            self.identifier = set(self)
        self.value = self.get_value


class Entity:
    def __init__(self, cs: CoordinateSystem):
        self.cs = cs
        self.identifier = generate_id()
        self.properties = dict()


class EntitiesList:
    pass


class Game:
    pass

