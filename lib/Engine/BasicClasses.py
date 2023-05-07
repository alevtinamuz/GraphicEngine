from collections.abc import Callable
from lib.Math.LowLevelMath import *
from lib.Exceptions.EngineExceptions import EngineExceptions
import uuid

PRECISION = 7


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
        self.value = self.get_value(self.identifiers.index(self.identifier))

    @staticmethod
    def __generate__() -> Union[int, float, str]:
        return str(uuid.uuid4().get_hex().upper()[0:16])

    def get_value(self, element) -> Union[int, float, str]:
        return self.identifiers[element]


class Entity:
    def __init__(self, cs: CoordinateSystem):
        self.__dict__["properties"] = set()
        self.set_property("cs", cs)
        self.set_property("identifier", Identifier())

    def get_property(self, prop: str) -> Union[int, float, str]:
        if prop not in self.__dict__["properties"]:
            raise EngineExceptions(EngineExceptions.GET_PROPERTY_ERROR)

        return self.__dict__[prop]

    def set_property(self, prop: str, value: Union[int, float, str]) -> None:
        if prop == "properties":
            raise EngineExceptions(EngineExceptions.SET_PROPERTY_ERROR)

        self.__dict__[prop] = value
        self.__dict__["properties"].add(prop)

    def remove_property(self, prop: str) -> None:
        if prop == "properties":
            raise EngineExceptions(EngineExceptions.REMOVE_PROPERTY_ERROR)

        if prop not in self.__dict__["properties"]:
            raise EngineExceptions(EngineExceptions.REMOVE_PROPERTY_ERROR)

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
    def __init__(self):
        pass

    def append(self, entity: Entity) -> None:
        pass

    def remove(self, entity: Entity) -> None:
        pass

    def get(self, identifier: Identifier) -> Entity:
        pass

    def exec(self, func: Callable[[int, float, str], Entity]) -> None:
        pass

    def __getitem__(self, item):
        pass


class Game:
    def __init__(self):
        pass

    def run(self):
        pass

    def update(self):
        pass

    def exit(self):
        pass

    def get_entity_class(self):
        pass

    def get_ray_class(self):
        pass

    class Object(Entity):
        pass

    class Camera(Object):
        pass

