from collections.abc import Callable
import time

from lib.Math.LowLevelMath import *
from lib.Exceptions.EngineExceptions import EngineExceptions
from lib.GlobalVariables import identifiers


class Ray:
    def __init__(self, cs: CoordinateSystem, initial_pt: Union[Point, None] = None,
                 direction: Union[Vector, None] = None
                 ):
        self.cs = cs
        self.initial_pt = initial_pt
        self.direction = direction

    def normalize(self) -> Vector:
        return self.direction.normalize()


class Identifier:

    def __init__(self):
        self.identifier = Identifier.__generate__()
        identifiers.append(self.identifier)
        set(identifiers)
        self.value = Identifier.get_value(identifiers.index(self.identifier))

    @staticmethod
    def __generate__() -> Union[int, float, str]:
        time.sleep(0.000001)
        print(hex(int(time.time() * 10000000))[2:])
        return hex(int(time.time() * 10000000))[2:]

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
        self.entity = self.get_entity_class()
        self.ray = self.get_ray_class()
        self.object = self.get_object_class()
        self.camera = self.get_camera_class()

    def run(self) -> None:
        pass

    def update(self) -> None:
        pass

    def exit(self) -> None:
        pass

    def get_entity_class(self):
        class GameEntity(Entity):
            def __init__(pself):
                super().__init__(self.cs)

        return GameEntity

    def get_ray_class(self):
        class GameRay(Ray):
            def __init__(pself):
                super().__init__(self.cs)

        return GameRay

    def get_object_class(self):
        class Object(self.get_entity_class()):
            def __init__(pself, position: Point, direction: Vector):
                super().__init__()
                pself.set_direction(direction)
                pself.set_position(position)

            def move(pself, direction: Vector) -> None:
                pself.set_position(pself.position + direction)

            def planar_rotate(pself, i: int, j: int, angle: float) -> None:
                direction = Vector(pself.entity["direction"])
                pself.set_direction(direction * Matrix(pself).rotate(i, j, angle))

            def rotate_3d(pself, angle_x: Union[int, float], angle_y: Union[int, float],
                          angle_z: Union[int, float]) -> None:
                direction = Vector(pself.entity["direction"])
                pself.set_direction(direction * Matrix(pself).rotate_three_dimensional(angle_x, angle_y, angle_z))

            def set_position(pself, position: Point) -> None:
                pself.set_property("position", position)

            def set_direction(pself, direction: Vector) -> None:
                if direction != None:
                    direction = direction.normalize()
                pself.set_property("direction", direction)

            @classmethod
            def intersection_distance(pself, ray: Ray):
                return 0

        return Object

    def get_camera_class(self):
        class Camera(self.get_object_class()):
            def __init__(self, position: Point, fov: Union[int, float],
                         draw_distance: Union[int, float], v_fov: Union[int, float, None] = None,
                         direction: Union[Vector, None] = None, look_at: Union[Point, None] = None):
                super().__init__(position, direction)
                self.set_property("fov", fov * math.pi / 180)
                self.set_property("draw_distance", draw_distance)
                self.set_property("v_fov", math.atan(16 / 9 * math.tan(fov / 2)))

                if v_fov is not None:
                    self.set_property("v_fov", v_fov)
                if look_at is not None:
                    self.set_property("look_at", look_at)
                if direction is not None:
                    self.set_property("direction", direction)

            def get_rays_matrix(pself, n: int, m: int):
                print(pself.direction)
                # if pself.direction is not None:
                    # alpha =
                    # beta =

        return Camera
