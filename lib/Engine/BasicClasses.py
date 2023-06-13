import curses
import time

from config.GlobalVariables import canvas_n, canvas_m, draw_distance
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
    def __init__(self, cs: CoordinateSystem, es: EventSystem = None, entities: EntitiesList = None):
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
        self.cosole = self.get_console_class()

    def run(self, canvas, camera):
        def main(stdscr):
            stdscr.clear()

            k, p = 0, 0

            while True:
                stdscr.addstr(61, 180, f"camera at: {str(camera.position.values)}")
                stdscr.addstr(62, 180, f"camera direction: {str(camera.direction.values)}")

                canvas.update(camera)

                matr = canvas.res_matrix

                for i in range(matr.rows):
                    for j in range(matr.columns):
                        stdscr.addch(i, j, matr[i][j])

                key = stdscr.getkey()
                if key == "l":
                    open('log.txt', 'w').close()
                    break
                if key == "w":
                    dist = camera.direction
                    self.es.trigger("move", camera, dist.norm() * 30)
                    k += 1
                    stdscr.addstr(59, 180, f"{k} move complete")
                elif key == "s":
                    dist = (-1) * camera.direction
                    self.es.trigger("move", camera, dist.norm() * 30)
                    k += 1
                    stdscr.addstr(59, 180, f"{k} move complete")
                elif key == "a":
                    self.es.trigger("move", camera, 5 * Vector.vector_product(camera.direction, Vector([0, 0.2, 0])))
                    k += 1
                    stdscr.addstr(59, 180, f"{k} move complete")
                elif key == "d":
                    self.es.trigger("move", camera, 5 * Vector.vector_product(camera.direction, Vector([0, -0.2, 0])))
                    k += 1
                    stdscr.addstr(59, 180, f"{k} move complete")
                elif key == "KEY_UP":
                    self.es.trigger("rotate_ver", camera, camera.direction - Vector([0, 0.005, 0]))
                    p += 1
                    stdscr.addstr(60, 180, f"{p} rotate complete")
                elif key == "KEY_DOWN":
                    self.es.trigger("rotate_ver", camera, camera.direction + Vector([0, 0.005, 0]))
                    p += 1
                    stdscr.addstr(60, 180, f"{p} rotate complete")
                elif key == "KEY_RIGHT":
                    self.es.trigger("rotate_hor", camera, [1, 2], -0.2)
                    p += 1
                    stdscr.addstr(60, 180, f"{p} rotate complete")
                elif key == "KEY_LEFT":
                    self.es.trigger("rotate_hor", camera, [1, 2], 0.2)
                    p += 1
                    stdscr.addstr(60, 180, f"{p} rotate complete")
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
            def __init__(pself, position: Point, direction: Vector):
                super().__init__()
                pself.set_direction(direction)
                pself.set_position(position)

            def move(self, direction: Vector) -> None:
                self.set_position(self.position + direction)

            def planar_rotate(self, i: int, j: int, angle: float) -> None:
                direction = Vector(self.entity["direction"])
                self.set_direction(direction * Matrix(self).rotate(i, j, angle))

            def rotate_3d(self, angle_x: Union[int, float], angle_y: Union[int, float],
                          angle_z: Union[int, float]) -> None:
                direction = Vector(self.entity["direction"])
                self.set_direction(direction * Matrix(self).rotate_three_dimensional(angle_x, angle_y, angle_z))

            def set_position(self, position: Point) -> None:
                self.set_property("position", position)

            def set_direction(self, direction: Vector) -> None:
                if direction is not None:
                    direction = direction.normalize()
                self.set_property("direction", direction)

            @classmethod
            def intersection_distance(self, ray: Ray):
                return 0

        return Object

    def get_camera_class(self):
        class Camera(self.object):
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

            def get_rays_matrix(self, n: int, m: int) -> Matrix:
                if self.direction is not None:
                    ray_list = []
                    alpha = self.fov
                    beta = self.v_fov
                    delta_alpha = alpha / n
                    delta_beta = beta / m
                    vector = self.direction
                    for i in range(0, n):
                        alpha_i = delta_alpha * i - alpha / 2
                        tmp_list = []
                        for j in range(0, m):
                            beta_i = delta_beta * j - beta / 2
                            vector_res = vector.copy()
                            vector_res.rotate(0, 1, alpha_i)
                            vector_res.rotate(0, 2, beta_i)
                            if (vector % vector_res) == 0:
                                raise Exceptions(Exceptions.ZERO_DIVISION)
                            vector_res = (vector_res * (vector.length() ** 2 / (vector % vector_res)))
                            tmp_list.append(vector_res)
                        ray_list.append(tmp_list)

                    return Matrix(ray_list)

                if self.look_at is not None:
                    ray_list = []
                    alpha = self.fov
                    beta = self.v_fov
                    delta_alpha = alpha / n
                    delta_beta = beta / m
                    look_at_vector = Vector([i for i in self.look_at.values])
                    position_vector = Vector([i for i in self.position.values])
                    vector = (look_at_vector - position_vector).normalize()
                    for i in range(0, n):
                        alpha_i = delta_alpha * i - alpha / 2
                        tmp_list = []
                        for j in range(0, m):
                            beta_i = delta_beta * j - beta / 2
                            vector_res = vector.copy()
                            vector_res.rotate(0, 1, alpha_i)
                            vector_res.rotate(0, 2, beta_i)
                            if (vector % vector_res) == 0:
                                raise Exceptions(Exceptions.ZERO_DIVISION)
                            vector_res = (vector_res * (vector.length() ** 2 / (vector % vector_res)))
                            tmp_list.append(vector_res)
                        ray_list.append(tmp_list)

                    return Matrix(ray_list)

        return Camera

    def get_hyper_plane_class(self):
        class HyperPlane(self.object):
            def __init__(pself, position: Point, normal: Vector):
                super().__init__(position, normal.normalize())
                pself.set_property("position", position)
                pself.set_property("normal", normal.normalize())

            def planar_rotate(self, i: int, j: int, angle: float) -> None:
                normal = self.normal.rotate(i, j, angle)
                self.normal = normal

            def rotate_3d(self, angle_x: Union[int, float], angle_y: Union[int, float], angle_z: Union[int, float]) -> None:
                normal = self.normal.rotate_3d(angle_x, angle_y, angle_z)
                self.normal = normal

            def intersection_distance(self, ray: Ray) -> float:
                normal_vector_hyper_plane = self.normal
                initial_pt_hyper_plane = self.position.as_vector()
                direction_ray = ray.direction
                initial_pt_ray = ray.initial_pt

                if normal_vector_hyper_plane % direction_ray == 0:
                    if normal_vector_hyper_plane % (initial_pt_ray - initial_pt_hyper_plane) != 0:
                        return EngineExceptions(EngineExceptions.PARALLEL_RAY)
                    return 0

                parameter = - (normal_vector_hyper_plane % (initial_pt_ray - initial_pt_hyper_plane)) / \
                              (normal_vector_hyper_plane % direction_ray)

                if parameter < 0:
                    return 0

                result_vector = Vector([initial_pt_ray[i] + direction_ray[i] * parameter
                                        for i in range(direction_ray.size)])

                return result_vector.length()

        return HyperPlane

    def get_hyper_ellipsoid_class(self):
        class HyperEllipsoid(self.object):
            def __init__(pself, position: Point, direction: Vector, semi_axes: list[float]):
                super().__init__(position, direction)
                pself.semi_axes = semi_axes
                pself.set_property("semi_axes", semi_axes)

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

                return min(result_1, result_2)

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

            def update(pself, camera: Game.get_camera_class(self)) -> None:
                rays = camera.get_rays_matrix(pself.n, pself.m)

                for i in range(pself.n):
                    for j in range(pself.m):
                        result = []
                        for entity in self.entities:
                            result.append(entity.intersection_distance(rays[i][j]))
                        result = [i for i in result if i > 0]
                        if len(result) == 0:
                            result = 0
                        else:
                            result = min(result)
                        pself.distances[i][j] = result

                char_map = Game.get_console_class().char_map
                length = len(Game.get_console_class().char_map)
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
                                res_matrix[i][j] = char_map[k]
                                break

                pself.res_matrix = res_matrix

        return Canvas

    def get_console_class(self):
        class Console(self.canvas):
            char_map = ".:;><+r*zsvfwqkP694VOGbUAKXH8RD#$B0MNWQ%&@"

        return Console
