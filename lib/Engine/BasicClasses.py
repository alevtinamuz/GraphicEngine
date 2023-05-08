from collections.abc import Callable
import uuid

from lib.Math.LowLevelMath import *
from lib.Exceptions.EngineExceptions import EngineExceptions


PRECISION = 7


class Ray:
    def __init__(self, cs: CoordinateSystem, initial_pt: Point, direction: Vector):
        self.cs = cs
        self.initial_pt = initial_pt
        self.direction = direction


class Identifier:
    def __init__(self):
        self.identifier = Identifier.__generate__()
        self.identifiers.append(self.identifier)
        set(self.identifiers)
        self.value = self.get_value(self.identifiers.index(self.identifier))

    @staticmethod
    def __generate__() -> Union[int, float, str]:
        return str(uuid.uuid4().get_hex().upper()[0:16])

    def get_value(self, element: int) -> Union[int, float, str]:
        return self.identifiers[element]


class Entity:
    def __init__(self, cs: CoordinateSystem):
        self.__dict__["properties"] = set()
        self.set_property("cs", cs)
        self.set_property("identifier", self.Identifier.identifier)

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
    def __init__(self, entities: list):
        self.entities = entities

    def append(self, entity: Entity) -> None:
        if len(self.entities) != 0:
            raise EngineExceptions(EngineExceptions.ENTITY_LIST_ERROR)
        self.entities.append(entity)

    def remove(self, entity: Entity) -> None:
        if len(self.entities) != 0:
            raise EngineExceptions(EngineExceptions.ENTITY_LIST_ERROR)
        self.entities.remove(entity)

    def get(self, identifier: Identifier) -> Entity:
        if len(self.entities) != 0:
            raise EngineExceptions(EngineExceptions.ENTITY_LIST_ERROR)
        for entity in self.entities:
            if identifier.get_value() == Identifier.get_value(entity):
                return entity
        raise EngineExceptions(EngineExceptions.ENTITY_NOT_EXIST)

    def exec(self, func: Callable[[int, float, str], Entity]) -> None:
        if len(self.entities) != 0:
            raise EngineExceptions(EngineExceptions.ENTITY_LIST_ERROR)
        self.entities = list(map(lambda entity: func(entity), self.entities))
        return self.entities

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
        return Entity(CoordinateSystem[Point([0.0, 0.0, 0.0]), VectorSpace(Vector([1.0, 0.0, 0.0]), Vector([0.0, 1.0, 0.0]), Vector([0.0, 0.0, 1.0]))])

    @staticmethod
    def get_ray_class() -> Ray:
        return Ray(CoordinateSystem[Point([0.0, 0.0, 0.0]), VectorSpace(Vector([1.0, 0.0, 0.0]), Vector([0.0, 1.0, 0.0]), Vector([0.0, 0.0, 1.0]))])

    class Object(Entity):
        def __init__(self, position: Point, direction: Vector):
            direction = direction.normalize()
            self.entity = Game.get_entity_class()
            self.entity.set_property("position", position)
            self.entity.set_property("direction", direction)

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
        def __init__(self, position: Point, direction: Union[int, float],
                     fov: Union[int, float], v_fov: Union[int, float],
                     look_at: Point, draw_distance: Union[int, float]):
            self.entity.set_property("fov", fov * math.pi / 180)
            self.entity.set_property("draw_distance", draw_distance)
            if isinstance(v_fov, (int, float)):
                self.entity.set_property("v_fov", v_fov)
            if isinstance(look_at, Point):
                self.entity.set_property("look_at", look_at)



