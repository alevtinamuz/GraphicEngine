from curses import wrapper
import time

from config.GlobalVariables import canvas_n, canvas_m, draw_distance, char_map
from lib.Math.LowLevelMath import *
from lib.Exceptions.EngineExceptions import EngineExceptions
from config.GlobalVariables import identifiers
from lib.Engine.EventSystem import *
from config.Configuration import *


class Ray:
    def __init__(self, cs: CoordinateSystem, initial_pt: Point, direction: Vector):
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
    def __init__(self, entities: list = None):
        if entities is None:
            entities = []
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
        entity = [entity for entity in self.entities
                  if entity['identifier'] == identifier]
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
    def __init__(self, cs: CoordinateSystem, entities: EntitiesList, es: EventSystem = None):
        self.cs = cs
        self.entities = entities
        self.es = es
        self.entity = self.get_entity_class()
        self.ray = self.get_ray_class()
        self.object = self.get_object_class()
        self.camera = self.get_camera_class()
        self.hyper_plane = self.get_hyper_plane_class()
        self.hyper_ellipsoid = self.get_hyper_ellipsoid_class()
        self.canvas = self.get_canvas_class()
        self.console = self.get_console_class()

    def run(self, canvas, camera):
        def main(stdscr):
            stdscr.clear()

            k, p = 0, 0

            while True:
                canvas.update(camera)

                matrix = canvas.res_matrix

                for i in range(len(matrix.elements)):
                    for j in range(len(matrix.elements[0])):

                        stdscr.addch(i, j, str(matrix[i][j]))

                key = stdscr.getkey()

                if key == "e":
                    break

                if key == "w":
                    dist = camera.direction
                    self.es.trigger("move", camera, dist.normalize() * 30)

                elif key == "s":
                    dist = (-1) * camera.direction
                    self.es.trigger("move", camera, dist.normalize() * 30)

                elif key == "a":
                    self.es.trigger("move", camera, 5 * Vector.vector_product(camera.direction, Vector([0, 0.2, 0])))

                elif key == "d":
                    self.es.trigger("move", camera, 5 * Vector.vector_product(camera.direction, Vector([0, -0.2, 0])))

                elif key == "KEY_UP":
                    self.es.trigger("vertical_rotate", camera, camera.direction - Vector([0, 0.005, 0]))

                elif key == "KEY_DOWN":
                    self.es.trigger("vertical_rotate", camera, camera.direction + Vector([0, 0.005, 0]))

                elif key == "KEY_RIGHT":
                    self.es.trigger("horizontal_rotate", camera, [1, 2], -0.2)

                elif key == "KEY_LEFT":
                    self.es.trigger("horizontal_rotate", camera, [1, 2], 0.2)
                # with open("log.txt", 'w') as f:
                #     for i in canvas.distances:
                #         f.write(str(i)+'\n')
                #     f.close()

        wrapper(main)

    def update(self) -> None:
        pass

    def exit(self) -> None:
        pass

    def get_event_system(self) -> EventSystem:
        return EventSystem(self.es)

    def apply_configuration(self, configuration: Configuration):
        pass

    def get_entity_class(self):
        class GameEntity(Entity):
            def __init__(pself):
                super().__init__(self.cs)

        return GameEntity

    def get_ray_class(self):
        class GameRay(Ray):
            def __init__(pself, initial_pt: Point, direction: Vector):
                super().__init__(self.cs, initial_pt, direction)

        return GameRay

    def get_object_class(self):
        class Object(self.entity):
            def __init__(pself, position: Point, direction: Vector = None):
                super().__init__()
                position = Point([round(x, PRECISION)
                                 for x in position.vector])
                pself.set_direction(direction)
                pself.set_position(position)

            def move(self, direction: Vector) -> None:
                self.set_position(self['position'] + direction)

            def planar_rotate(self, i: int, j: int, angle: float) -> None:
                direction = Vector(self.entity["direction"])
                self.set_direction(direction * Matrix(self).rotate(i, j, angle))

            def rotate_3d(self, angle_x: Union[int, float], angle_y: Union[int, float],
                          angle_z: Union[int, float]) -> None:
                direction = Vector(self.entity["direction"])
                self.set_direction(direction * Matrix(self).rotate_three_dimensional(angle_x, angle_y, angle_z))

            def set_position(self, position: Point) -> None:
                position = Point([round(x, PRECISION)
                                  for x in position.vector])

                self['position'] = position

            def set_direction(self, direction: Vector) -> None:
                if direction is not None and direction is not Vector([0, 0, 0]):
                    direction = Vector([round(x, PRECISION)
                                        for x in direction.normalize().vector])

                self.set_property('direction', direction)

            @classmethod
            def intersection_distance(self, ray: Ray):
                return 0

        return Object

    def get_camera_class(self):
        class Camera(self.object):
            def __init__(pself, position: Point, fov: Union[int, float] = None,
                         draw_dist: Union[int, float] = None, v_fov: Union[int, float, None] = None,
                         direction: Union[Vector, None] = None, look_at: Union[Point, None] = None):
                super().__init__(position, direction)
                pself.set_property("draw_distance", draw_dist)
                pself.set_property("v_fov", math.atan(canvas_m/canvas_n * math.tan(fov / 2)))
                if fov is not None:
                    pself.set_property("fov", fov)
                else:
                    pself.set_property("fov", fov * math.pi / 180)
                if v_fov is not None:
                    pself.set_property("v_fov", v_fov)
                if look_at is not None:
                    pself.set_property("look_at", look_at)
                if direction is not None:
                    pself.set_property("direction", direction)

            def get_rays_matrix(self, n: int, m: int) -> Matrix:
                if self.direction is not None:
                    result = Matrix.zero_matrix(n, m)

                    alpha, beta = self.fov, self.v_fov
                    dalpha, dbeta = alpha / n, beta / m
                    vec = self.direction

                    for i in range(n):
                        for j in range(m):
                            temp_vec = vec
                            temp_vec.rotate(0, 1, dalpha * i - alpha / 2)
                            temp_vec.rotate(0, 2, dbeta * j - beta / 2)
                            if (vec % temp_vec) == 0:
                                raise Exceptions(Exceptions.ZERO_DIVISION)
                            temp_vec = (temp_vec * (vec.length() ** 2 / (vec % temp_vec)))
                            result[i][j] = Ray(self.cs, self.position, temp_vec)

                    return result

                if self.look_at is not None:
                    result = Matrix.zero_matrix(n, m)
                    look_at_vec = Vector([x for x in self.look_at.vector])
                    position_vec = Vector([x for x in self.position.vector])

                    vec = (look_at_vec - position_vec).normalize()

                    alpha, beta = self.fov, self.vfov
                    dalpha, dbeta = alpha / n, beta / m

                    for i in range(n):
                        for j in range(m):
                            temp_vec = vec.copy()
                            temp_vec.rotate([0, 1], dalpha * i - alpha / 2)
                            temp_vec.rotate([0, 2], dbeta * j - beta / 2)
                            if (vec % temp_vec) == 0:
                                raise Exceptions(Exceptions.ZERO_DIVISION)
                            temp_vec = (temp_vec * (vec.length() ** 2 / (vec % temp_vec)))
                            result[i][j] = Ray(self.cs, self.position, temp_vec)

                    return result

        return Camera

    def get_hyper_plane_class(self):
        class HyperPlane(self.object):
            def __init__(pself, position: Point, normal: Vector):
                super().__init__(position)
                pself.set_property("position", position)
                pself.set_property("normal", normal.normalize())
                pself.normal = normal.normalize()
                pself.position = position
                self.entities.append(pself)

            def planar_rotate(self, i: int, j: int, angle: float) -> None:
                normal = self.normal.rotate(i, j, angle)
                self.normal = normal

            def rotate_3d(self, angle_x: Union[int, float], angle_y: Union[int, float], angle_z: Union[int, float]) -> None:
                normal = self.normal.rotate_3d(angle_x, angle_y, angle_z)
                self.normal = normal

            def intersection_distance(self, ray: Ray) -> float:
                ray_inp_vec = ray.initial_pt.as_vector()  # x^1
                pos_vec = self.position.as_vector()  # x^0
                dim = ray.direction.dimension

                if (self.normal % ray.direction) == 0:
                    return 0

                t = -((self.normal % (ray_inp_vec - pos_vec)) /
                      (self.normal % ray.direction))

                if t <= 0:
                    return 0

                temp_vec = Vector([ray_inp_vec[i] + ray.direction[i] * t
                                   for i in range(dim)])

                return round(temp_vec.length(), PRECISION) / 2

        return HyperPlane

    def get_hyper_ellipsoid_class(self):
        class HyperEllipsoid(self.object):
            def __init__(pself, position: Point, direction: Vector, semi_axes: list[float]):
                super().__init__(position, direction)
                pself.semi_axes = semi_axes
                pself.set_property("semi_axes", semi_axes)
                self.entities.append(pself)

            def planar_rotate(self, i: int, j: int, angle: float) -> None:
                direction = self.direction.rotate(i, j, angle)
                self.set_direction(direction)

            def rotate_3d(self, angle_x: Union[int, float], angle_y: Union[int, float],
                          angle_z: Union[int, float]) -> None:
                direction = self.direction.rotate_3d(angle_x, angle_y, angle_z)
                self.set_direction(direction)

            def intersection_distance(self, ray: Ray) -> float:
                initial_pt_hyper_ellipsoid = self.position
                direction_ray = ray.direction
                initial_pt_ray = ray.initial_pt
                param_1 = 0
                param_2 = 0
                param_3 = 0
                param_4 = 0
                for i in range(len(self.semi_axes)):
                    param_1 += direction_ray[i] ** 2
                    param_2 += (initial_pt_ray[i] - initial_pt_hyper_ellipsoid[i]) * direction_ray[i]
                    param_3 += (initial_pt_ray[i] - initial_pt_hyper_ellipsoid[i]) ** 2
                    param_4 = self.semi_axes[i] ** 2

                param_2 *= 2
                param_3 -= param_4

                t = param_2 ** 2 - 4 * param_1 * param_3
                if t < 0:
                    return 0

                result_1 = (- param_2 - math.sqrt(t)) / (2 * param_1)
                result_2 = (- param_2 + math.sqrt(t)) / (2 * param_1)

                if result_1 < 0:
                    if result_2 < 0:
                        return 0

                if result_2 < 0:
                    return result_1

                return round(min(result_1, result_2), PRECISION)

        return HyperEllipsoid

    def get_canvas_class(self):
        class Canvas:
            def __init__(self, n: int = None, m: int = None):
                if n is not None:
                    self.n = n
                else:
                    self.n = canvas_n
                if m is not None:
                    self.m = m
                else:
                    self.m = canvas_m
                self.distances = Matrix.zero_matrix(n, m)
                self.res_matrix = None

            def draw(self) -> None:
                pass

            def update(pself, camera) -> None:
                rays = camera.get_rays_matrix(pself.n, pself.m)

                for i in range(pself.n):
                    for j in range(pself.m):
                        result = []
                        for ent in self.entities.entities:
                            result.append(ent.intersection_distance(rays[i][j]))
                        result = [i for i in result if i > 0]
                        if len(result) == 0:
                            result = 0
                        else:
                            result = min(result)
                        pself.distances[i][j] = result

                simbols = char_map
                length = len(char_map)
                draw_dist = draw_distance

                step = draw_dist / length
                list_steps = [step * i for i in range(length)]

                matrix = pself.distances

                res_matrix = Matrix.zero_matrix(pself.n, pself.m)

                for i in range(pself.n):
                    for j in range(pself.m):
                        for k in range(length):
                            if matrix[i][j] == 0 or matrix[i][j] > draw_dist:
                                res_matrix[i][j] = '.'
                                break
                            if matrix[i][j] < list_steps[k]:
                                res_matrix[i][j] = simbols[k]
                                break

                pself.res_matrix = res_matrix

        return Canvas

    def get_console_class(self):
        class Console(self.canvas):
            char_map = ".:;><+r*zsvfwqkP694VOGbUAKXH8RD#$B0MNWQ%&@"

        return Console
