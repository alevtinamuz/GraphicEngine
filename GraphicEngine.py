import math


class Point:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x,
                     self.y + other.y,
                     self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x,
                     self.y - other.y,
                     self.z - other.z)

    def __mul__(self, other):
        return Point(self.x * other,
                     self.y * other,
                     self.z * other)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if other == 0:
            raise Exception(ZeroDivisionError)
        return self * (1 / other)

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Vector:
    def __init__(self, x: [float, Point] = 0, y: float = 0, z: float = 0):
        if isinstance(x, (int, float)):
            self.x = x
            self.y = y
            self.z = z
        elif isinstance(x, Point):
            self.x = x.x
            self.y = x.y
            self.z = x.z

    def as_point(self):
        return Point(self.x,
                     self.y,
                     self.z)

    def __add__(self, other):
        return Vector(self.x + other.x,
                      self.y + other.y,
                      self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x,
                      self.y - other.y,
                      self.z - other.z)

    def scalar_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def vector_product(self, other):
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x * other,
                          self.y * other,
                          self.z * other)
        elif isinstance(other, Vector):
            return Vector.scalar_product(self, other)

    __rmul__ = __mul__

    def __pow__(self, other):
        return Vector.vector_product(self, other)

    def length(self):
        return Point.distance(VectorSpace.initial_point, self)

    def normalize(self):
        length = self.length()
        if length == 0:
            raise Exception(ZeroDivisionError)
        return Vector(self.x / length,
                      self.y / length,
                      self.z / length)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


class VectorSpace:
    initial_point = Point(0, 0, 0)

    def __init__(self, initial_point: Point, basis_x: Vector, basis_y: Vector, basis_z: Vector):
        self.initial_point = initial_point
        self.basis_x = basis_x
        self.basis_y = basis_y
        self.basis_z = basis_z


class Camera:
    def __init__(self, position: Point, look_at: [Vector, Point], FOV: float, draw_distance: float):
        height = 1080
        width = 1920
        k = 1.0
        self.position = position
        self.look_at = look_at
        self.FOV = FOV
        self.vFOV = (height / width) * FOV * k
        self.draw_distance = draw_distance

    def send_rays(self, number_of_rays):
        pass


class Object:
    def __init__(self, position: Point, rotation: Vector):
        self.position = position
        self.rotation = rotation

    def contains(self, point: Point):
        return False
