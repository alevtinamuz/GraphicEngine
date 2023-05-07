from lib.Math.LowLevelMath import *
import uuid


class Ray:
    def __init__(self, cs: CoordinateSystem, initial_pt: Point, direction: Vector):
        self.cs = cs
        self.initial_pt = initial_pt
        self.direction = direction


class Identifier:
    def __init__(self):
        self.identifier = self.__generate__()
        self.identifiers = []
        self.identifiers.append(self.identifier)
        set(self.identifiers)
        self.value = self.get_value(len(self.identifiers) - 1)

    @staticmethod
    def __generate__() -> Union[int, float, str]:
        return str(uuid.uuid4().get_hex().upper()[0:16])

    def get_value(self, element) -> Union[int, float, str]:
        return self.identifiers[element]


class Entity:
    def __init__(self, cs: CoordinateSystem):
        self.__dict__["properties"] = set()

    def get_property(self, prop: str, default=None):
        if prop not in self.__dict__["properties"]:
            return default

        return self.__dict__[prop]

    def set_property(self, prop: str, value: any):
        if prop == "properties":
            raise Exception

        self.__dict__[prop] = value
        self.__dict__["properties"].add(prop)

    def remove_property(self, prop):
        if prop == "properties":
            raise Exception

        self.__delattr__(prop)
        self.__dict__["properties"].remove(prop)

    def __getitem__(self, prop):
        return self.get_property(prop)

    def __setitem__(self, prop, value):
        self.set_property(prop, value)

    def __getattr__(self, prop):
        return self.get_property(prop)

    def __setattr__(self, prop, value):
        self.set_property(prop, value)


class EntitiesList:
    pass


class Game:
    pass

