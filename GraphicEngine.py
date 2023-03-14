import math

class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def as_list(self):
        return [self.x, self.y, self.z]

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Point(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Point(x, y, z)

    def __mul__(self, other):
        x = self.x * other
        y = self.y * other
        z = self.z * other
        return Point(x, y, z)

    __rmul__ = __mul__

    def __truediv__(self, other):
        try:
            x = self.x / other
            y = self.y / other
            z = self.z / other
            return Point(x, y, z)
        except ZeroDivisionError:
            print('\nZeroDivisionError!')

    def distance_between(self, other):
        diff = self - other
        return math.sqrt(diff.x ** 2 + diff.y ** 2 + diff.z ** 2)

    def __str__(self):
        return "({0}, {1}, {2})".format(self.x, self.y, self.z)



class Vector:
    def __init__(self, x: [float, Point] = 0.0, y: float = 0.0, z: float = 0.0):
        if isinstance(x, (int, float)):
            self.x = x
            self.y = y
            self.z = z
        elif isinstance(x, Point):
            self.x = x.x
            self.y = x.y
            self.z = x.z

    def as_list(self):
        return [self.x, self.y, self.z]

    def as_point(self):
        return Point(x = self.x, y = self.y, z = self.z)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vector(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vector(x, y, z)

    def scalar_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def vector_product(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector(x, y, z)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            x = self.x * other
            y = self.y * other
            z = self.z * other
            return Vector(x, y, z)
        elif isinstance(other, Vector):
            return Vector.scalar_product(self, other)

    __rmul__ = __mul__

    def __pow__(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector(x, y, z)

    def length(self):
        return Point.distance_between(VectorSpace.initial_point, self)

    def normalize(self):
        try:
            length = self.length()
            x = self.x
            y = self.y
            z = self.z
            if length != 0:
                x /= length
                y /= length
                z /= length
                return Vector(x, y, z)
        except ZeroDivisionError:
            print('Ошибка! Деление на 0')

    def __str__(self):
        return "({0}, {1}, {2})".format(self.x, self.y, self.z)



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

    def contains(self):
        BOOl = True
        return BOOl



class Sphere:
    def __init__(self, center: Point, radius: float = 0.0):
        self.radius = radius
        self.center = center