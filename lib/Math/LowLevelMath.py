import math
from typing import Union, List
import lib.Engine.BasicClasses
from lib.Exceptions.MathExceptions import Exceptions, MatrixExceptions, VectorExceptions, PointExceptions

PRECISION = lib.Engine.BasicClasses.PRECISION


@property
def attribute_error(self):
    raise AttributeError


class Matrix:
    def __init__(self, elements: Union[List[List[float]], 'Vector']):
        if isinstance(elements, Vector):
            if elements.is_transpose:
                self.elements = elements.vector
                self.rows = elements.dimension
                self.columns = 1
            else:
                self.elements = [elements.vector]
                self.rows = 1
                self.columns = elements.dimension
        else:
            self.elements = elements
            self.rows = len(elements)
            self.columns = len(elements[0])

            for i in range(self.rows - 1):
                if len(self.elements[i]) != len(self.elements[i + 1]):
                    raise MatrixExceptions(MatrixExceptions.WRONG_INIT)

    def is_square(self) -> bool:
        return self.rows == self.columns

    def size(self) -> int:
        return self.rows, self.columns

    def determinant(self) -> float:
        if not self.is_square():
            raise MatrixExceptions(MatrixExceptions.NOT_A_SQUARE)

        if self.rows == 1:
            return self.elements[0][0]

        elif isinstance(self.elements[0][0], (int, float)):
            size = self.columns
            result = 0
            for index in range(size):
                submatrix = self.minor(0, index)
                det = submatrix.determinant()
                result += (-1) ** index * det * self.elements[0][index]

            return result

        size = self.columns
        result = Vector([0, 0, 0])
        for index in range(size):
            submatrix = self.minor(0, index)
            det = submatrix.determinant()
            result += (-1) ** index * det * self.elements[0][index]

        return result

    def copy(self):
        tmp = []
        for i in self.elements:
            row = []
            for j in i:
                row.append(j)
            tmp.append(row)

        return Matrix(tmp)

    def minor(self, i: int, j: int) -> 'Matrix':
        tmp = self.copy().elements
        tmp.pop(i)
        for row in range(len(tmp)):
            tmp[row].pop(j)

        return Matrix(tmp)

    def inverse(self) -> 'Matrix':
        if not self.is_square():
            raise MatrixExceptions(MatrixExceptions.NOT_A_SQUARE)

        det = self.determinant()

        if det == 0:
            raise MatrixExceptions(MatrixExceptions.WRONG_DETERMINANT)

        cofactors = []
        for rows in range(self.rows):
            cofactor_row = []
            for columns in range(self.rows):
                minor = self.minor(rows, columns).determinant()
                cofactor_row.append(((-1) ** (rows + columns)) * minor)
            cofactors.append(cofactor_row)
        cofactors = Matrix(cofactors).transpose().elements
        for rows in range(len(cofactors)):
            for columns in range(len(cofactors)):
                cofactors[rows][columns] = cofactors[rows][columns] / det

        return Matrix(cofactors)

    def transpose(self) -> 'Matrix':
        return Matrix([[self.elements[j][i]
                        for j in range(self.rows)]
                       for i in range(self.columns)])

    @staticmethod
    def identity(size) -> 'Matrix':
        return Matrix([[1 if i == j else 0 for i in range(size)] for j in range(size)])

    def product(self: List[float], other: List[float]) -> float:
        return sum([self[i] * other[i] for i in range(len(self))])

    def gram(self) -> 'Matrix':
        return Matrix([[Matrix.product(self.elements[i], self.elements[j])
                        for i in range(self.rows)]
                       for j in range(self.rows)])

    def rotate(self, i: int, j: int, angle: float) -> 'Matrix':
        angle = angle * math.pi / 180
        rotation_matrix = Matrix.identity(self.columns)

        rotation_matrix[i][i] = math.cos(angle)
        rotation_matrix[j][j] = math.cos(angle)

        rotation_matrix[i][j] = -((-1) ** (i + j)) * math.sin(angle)
        rotation_matrix[j][i] = (-1) ** (i + j) * math.sin(angle)

        self.elements = (self * rotation_matrix).elements

        return self

    def equal(self, other: 'Matrix') -> bool:
        if not self.rows == other.rows and not self.columns == other.columns:
            raise MatrixExceptions(MatrixExceptions.NOT_EQUIVALENT)

        return all(abs(self[i][j] - other[i][j]) < 10 ** (-PRECISION)
                   for i in range(self.rows)
                   for j in range(self.columns))

    def additional(self, other: 'Matrix') -> 'Matrix':
        if not isinstance(other, Matrix):
            raise MatrixExceptions(MatrixExceptions.WRONG_TYPES)

        if not self.size() == other.size():
            raise MatrixExceptions(MatrixExceptions.WRONG_SIZES)

        return Matrix([[self.elements[i][j] + other.elements[i][j]
                        for j in range(self.columns)]
                       for i in range(self.rows)])

    def multiply(self, other: Union[float, 'Matrix']) -> 'Matrix':
        if isinstance(other, (int, float)):
            return Matrix([[self.elements[i][j] * other
                            for j in range(self.columns)]
                           for i in range(self.rows)])

        elif isinstance(other, Matrix):
            if not self.columns == other.rows:
                raise MatrixExceptions(MatrixExceptions.WRONG_SIZES_FOR_MULTIPLY)

            return Matrix([[Matrix.product(self.elements[i], other.transpose().elements[j])
                            for j in range(other.columns)]
                           for i in range(self.rows)])

        raise MatrixExceptions(MatrixExceptions.WRONG_TYPES)

    def division(self, other: float) -> 'Matrix':
        if not isinstance(other, (int, float)):
            raise MatrixExceptions(MatrixExceptions.WRONG_TYPES)

        if other == 0:
            raise MatrixExceptions(MatrixExceptions.ZERO_DIVISION)

        return self * (1 / other)

    def __eq__(self, other: 'Matrix') -> bool:
        return Matrix.equal(self, other)

    def __add__(self, other: 'Matrix') -> 'Matrix':
        return Matrix.additional(self, other)

    def __mul__(self, other: Union[float, 'Matrix']) -> 'Matrix':
        return Matrix.multiply(self, other)

    __rmul__ = __mul__

    def __sub__(self, other: 'Matrix') -> 'Matrix':
        return self + ((-1) * other)

    def __truediv__(self, other: float) -> 'Matrix':
        return Matrix.division(self, other)

    def __invert__(self) -> 'Matrix':
        return Matrix.inverse(self)

    def __getitem__(self, index: int):
        return self.elements[index]

    def __repr__(self):
        return f'{self.elements}'


class Vector(Matrix):
    def __init__(self, vector):
        if not isinstance(vector, list) and not isinstance(vector, Matrix):
            raise VectorExceptions(VectorExceptions.WRONG_TYPES)

        if isinstance(vector, Matrix):
            if 1 not in (vector.rows, vector.columns):
                raise VectorExceptions(VectorExceptions.WRONG_SIZES)

            self.dimension = [item for item in (vector.rows, vector.columns) if item != 1]
            vector = vector.elements

        if isinstance(vector, list) and isinstance(vector[0], list):
            for i in range(len(vector) - 1):
                if len(vector[i]) != len(vector[i + 1]):
                    raise VectorExceptions(VectorExceptions.WRONG_INIT)

        if isinstance(vector[0], list):
            if len(vector[0]) == 1:
                self.vector = vector
                self.is_transpose = True
                self.dimension = len(vector)
            else:
                self.vector = vector[0]
                self.is_transpose = False
                self.dimension = len(vector[0])

        if isinstance(vector[0], (int, float)):
            self.vector = vector
            self.is_transpose = False
            self.dimension = len(vector)

    def as_matrix(self):
        return Matrix(self)

    def scalar_product(self, other: 'Vector') -> float:
        if not isinstance(other, Vector):
            raise VectorExceptions(VectorExceptions.WRONG_TYPES)

        if not self.dimension == other.dimension:
            raise VectorExceptions(VectorExceptions.WRONG_SIZES)

        return bilinear_form(Matrix.identity(self.dimension), self, other)

    def vector_product(self, other: 'Vector') -> 'Vector':
        if not isinstance(other, Vector):
            raise VectorExceptions(VectorExceptions.WRONG_TYPES)

        if not (self.dimension == 3 and other.dimension == 3):
            raise VectorExceptions(VectorExceptions.WRONG_VECTOR_PRODUCT)

        basis = [Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])]
        matrix = Matrix([[basis[0], basis[1], basis[2]], self.vector, other.vector])
        return matrix.determinant()

    def length(self) -> float:
        return math.sqrt(self % self)

    def transpose(self) -> 'Vector':
        return Vector(self.as_matrix().transpose().elements)

    def rotate(self, i: int, j: int, angle: float):
        if not self.is_transpose:
            self.vector = self.as_matrix().rotate(i, j, angle).elements[0]
        else:
            self.vector = self.transpose().as_matrix().rotate(i, j, angle).transpose().elements
        return self

    def multiply(self, other: Union[float, 'Vector']) -> 'Vector':
        if isinstance(other, (int, float)):
            return Vector(self.as_matrix() * other)

        elif isinstance(other, Vector):
            return Vector(self.as_matrix() * other.as_matrix())

        raise VectorExceptions(VectorExceptions.WRONG_TYPES)

    def additional(self, other: 'Vector') -> 'Vector':
        if not isinstance(other, Vector):
            raise VectorExceptions(VectorExceptions.WRONG_TYPES)

        if not self.dimension == other.dimension:
            raise VectorExceptions(VectorExceptions.WRONG_SIZES)

        if self.is_transpose:
            self.transpose()

        if other.is_transpose:
            other.transpose()

        return Vector(self.as_matrix() + other.as_matrix())

    def subtraction(self, other: 'Vector') -> 'Vector':
        if not isinstance(other, Vector):
            raise VectorExceptions(VectorExceptions.WRONG_TYPES)

        if not self.dimension == other.dimension:
            raise VectorExceptions(VectorExceptions.WRONG_SIZES)

        if self.is_transpose:
            self.transpose()

        if other.is_transpose:
            other.transpose()

        return Vector(self.as_matrix() - other.as_matrix())

    def division(self, other: float) -> 'Vector':
        if other == 0:
            raise VectorExceptions(VectorExceptions.ZERO_DIVISION)
        if isinstance(other, (int, float)):
            return Vector(self.as_matrix() / other)

        raise VectorExceptions(VectorExceptions.WRONG_TYPES)

    def __eq__(self, other: 'Vector') -> bool:
        return self.as_matrix() == other.as_matrix()

    def __mul__(self, other: float) -> 'Vector':
        return Vector.multiply(self, other)

    __rmul__ = __mul__

    def __mod__(self, other: 'Vector') -> 'Vector':
        return Vector.scalar_product(self, other)

    def __pow__(self, other: 'Vector') -> 'Vector':
        return Vector.vector_product(self, other)

    def __getitem__(self, index: int) -> float:
        if not self.is_transpose:
            return self.vector[index]
        return self.vector[index][0]

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector.additional(self, other)

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector.subtraction(self, other)

    def __truediv__(self, other: float) -> 'Vector':
        return Vector.division(self, other)

    def __repr__(self):
        return f'{self.vector}'

    is_square = attribute_error
    size = attribute_error
    determinant = attribute_error
    copy = attribute_error
    minor = attribute_error
    inverse = attribute_error
    identity = attribute_error
    gram = attribute_error
    equal = attribute_error
    __invert__ = attribute_error


def bilinear_form(matrix, vector_1: Vector, vector_2: Vector) -> float:
    if not (matrix.rows == matrix.columns
            and matrix.rows == vector_1.dimension
            and matrix.rows == vector_2.dimension):
        raise MatrixExceptions(MatrixExceptions.WRONG_SIZES)

    return sum([matrix[i][j] * vector_1[i] * vector_2[j]
                for i in range(matrix.rows)
                for j in range(matrix.rows)])


class Point(Vector):
    def additional(self, other: Vector) -> 'Point':
        if not isinstance(other, Vector):
            raise PointExceptions(PointExceptions.WRONG_TYPES)

        if not self.dimension == other.dimension:
            raise PointExceptions(PointExceptions.WRONG_SIZES)

        return Point([self[i] + other[i] for i in range(self.dimension)])

    def subtraction(self, other: Vector) -> 'Point':
        if not isinstance(other, Vector):
            raise PointExceptions(PointExceptions.WRONG_TYPES)
        if not self.dimension == other.dimension:
            raise PointExceptions(PointExceptions.WRONG_SIZES)

        return Point([self[i] - other[i] for i in range(self.dimension)])

    def __add__(self, other: Vector) -> 'Point':
        return Point.additional(self, other)

    __radd__ = __add__

    def __sub__(self, other: Vector) -> 'Point':
        return Point.subtraction(self, other)

    scalar_product = attribute_error
    vector_product = attribute_error
    length = attribute_error
    transpose = attribute_error
    multiply = attribute_error
    division = attribute_error
    __mul__ = attribute_error
    __rmul__ = attribute_error
    __mod__ = attribute_error
    __pow__ = attribute_error
    __invert__ = attribute_error


class VectorSpace:
    def __init__(self, basis: List[Vector]):
        self.basis = Matrix([item.vector for item in basis])
        self.height = len(basis)

    def scalar_product(self, vector_1: Vector, vector_2: Vector) -> Matrix:
        if vector_1.is_transpose:
            vector_1 = vector_1.transpose()

        if not vector_2.is_transpose:
            vector_2 = vector_2.transpose()

        return (vector_1.as_matrix() * self.basis.gram() * vector_2.as_matrix())[0][0]

    def as_vector(self, point: Point) -> Vector:
        if not point.dimension == self.height:
            raise MatrixExceptions(MatrixExceptions.WRONG_SIZES)

        det = self.basis.determinant()
        answer = []
        for column in range(point.dimension):
            tmp = self.basis.copy().transpose()
            for row in range(point.dimension):
                tmp[row][column] = point[row]
            answer.append(Matrix.determinant(tmp) / det)
        return Vector(answer)

    def vector_product(self, vector_1: Vector, vector_2: Vector) -> Vector:
        if not isinstance(vector_2, Vector):
            raise VectorExceptions(VectorExceptions.WRONG_TYPES)

        if not (vector_1.dimension == 3 and vector_2.dimension == 3):
            raise VectorExceptions(VectorExceptions.WRONG_VECTOR_PRODUCT)

        basis = [Vector(self.basis[0]), Vector(self.basis[1]), Vector(self.basis[2])]
        i = basis[1].vector_product(basis[2])
        j = basis[2].vector_product(basis[0])
        k = basis[0].vector_product(basis[1])

        matrix = Matrix([[i, j, k], vector_1.vector, vector_2.vector])

        return matrix.determinant()

    def __repr__(self):
        return f'{self.basis}'


class CoordinateSystem:
    def __init__(self, point: Point, vector_space: VectorSpace):
        if not (isinstance(point, Point) and isinstance(vector_space, VectorSpace)):
            raise Exceptions(Exceptions.WRONG_TYPES)

        self.point = point
        self.vector_space = vector_space
