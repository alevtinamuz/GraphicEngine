from collections.abc import Callable
import uuid

from lib.Math.LowLevelMath import *
from lib.Exceptions.EngineExceptions import EngineExceptions
from lib.GlobalVariables import cs_global, identifiers


class Ray:
    def __init__(self, cs: CoordinateSystem, initial_pt: Union[Point, None] = None, direction: Union[Vector, None] = None):
        self.cs = cs
        self.initial_pt = initial_pt
        self.direction = direction


class Identifier:

    def __init__(self):
        self.identifier = Identifier.__generate__()
        identifiers.append(self.identifier)
        set(identifiers)
        self.value = Identifier.get_value(identifiers.index(self.identifier))

    @staticmethod
    def __generate__() -> Union[int, float, str]:
        return str(uuid.uuid4().hex.upper())

    @staticmethod
    def get_value(element: int) -> Union[int, float, str]:
        return identifiers[element]


class Entity:
    def __init__(self, cs: CoordinateSystem):
        self.__dict__["properties"] = set()
        self.set_property("cs", cs)
        self.set_property("identifier", Identifier().identifier)

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

    def __delitem__(self, prop):
        return self.remove_property(prop)


class EntitiesList:
    def __init__(self, entities: list):
        self.entities = entities

    def append(self, entity: Entity) -> None:
        self.entities.append(entity)

    def remove(self, entity: Entity) -> None:
        if len(self.entities) == 0:
            raise EngineExceptions(EngineExceptions.ENTITY_LIST_ERROR)
        self.entities.remove(entity)

    def get(self, identifier: Identifier) -> Entity:
        if len(self.entities) == 0:
            raise EngineExceptions(EngineExceptions.ENTITY_LIST_ERROR)
        for entity in self.entities:
            if Identifier.get_value(identifiers.index(identifier)) == entity['identifier']:
                return entity
        raise EngineExceptions(EngineExceptions.ENTITY_NOT_EXIST)

    def exec(self, func: Callable[[int, float, str], 'EntitiesList'], *prop, **value) -> None:
        if len(self.entities) == 0:
            raise EngineExceptions(EngineExceptions.ENTITY_LIST_ERROR)
        for entity in self.entities:
            func(entity, *prop, **value)

    def __getitem__(self, item):
        return self.get(item)


class Game:
    def __init__(self, cs: CoordinateSystem, entities: EntitiesList):
        self.cs = cs
        self.entities = entities

    def run(self) -> None:
        pass

    def update(self) -> None:
        pass

    def exit(self) -> None:
        pass

    @staticmethod
    def get_entity_class() -> Entity:
        return Entity(cs_global)

    @staticmethod
    def get_ray_class() -> Ray:
        return Ray(cs_global)

    class Object(Entity):
        def __init__(self, position: Point, direction: Vector):
            direction = direction.normalize()
            self.entity = Game.get_entity_class()
            self.entity["position"] = position
            self.entity["direction"] = direction

        def move(self, direction: Vector) -> None:
            self.entity["position"] = self.entity["position"] + direction

        def planar_rotate(self, i: int, j: int, angle: float) -> None:
            direction = Vector(self.entity["direction"])
            self.set_direction(direction * Matrix(self).rotate(i, j, angle))

        def rotate_3d(self, angle_x: Union[int, float], angle_y: Union[int, float], angle_z: Union[int, float]) -> None:
            direction = Vector(self.entity["direction"])
            self.set_direction(direction * Matrix(self).rotate_three_dimensional(angle_x, angle_y, angle_z))

        def set_position(self, position: Point) -> None:
            self.set_property("position", position)

        def set_direction(self, direction: Vector) -> None:
            self.set_property("direction", direction.normalize())

    class Camera(Object):
        def __init__(self, fov: Union[int, float], draw_distance: Union[int, float],
                     v_fov: Union[int, float, None] = None, look_at: Union[Point, None] = None):
            self.entity.set_property("fov", fov * math.pi / 180)
            self.entity.set_property("draw_distance", draw_distance)
            if v_fov is not None:
                self.entity.set_property("v_fov", v_fov)
            if look_at is not None:
                self.entity.set_property("look_at", look_at)
