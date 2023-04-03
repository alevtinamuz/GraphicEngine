import math


class Matrix:
    def __init__(self, elements):
        self.elements = elements
        self.height = len(elements)
        self.width = len(elements[0])
        max_len = 0
        min_len = float('inf')
        for i in range(0, len(elements)):
            if len(elements[i]) > max_len:
                max_len = len(elements[i])
            if len(elements[i]) < min_len:
                min_len = len(elements[i])
        if max_len != min_len:
            raise NameError('This is not matrix.')

    def __add__(self, other):
        if isinstance(other, Matrix) & isinstance(self, Matrix):
            if self.size() == other.size():
                return Matrix([[self.elements[i][j] + other.elements[i][j]
                                for j in range(self.width)]
                               for i in range(self.height)])
            else:
                raise NameError('Different sizes of matrices.')
        else:
            raise NameError('Different types of objects.')

    def __sub__(self, other):
        if isinstance(other, Matrix) & isinstance(self, Matrix):
            if self.size() == other.size():
                return Matrix([[self.elements[i][j] - other.elements[i][j]
                                for j in range(self.width)]
                               for i in range(self.height)])
            else:
                raise NameError('Different sizes of matrices.')
        else:
            raise NameError('Different types of objects.')

    def __mul__(self, other):
        if isinstance(other, (int, float)) & isinstance(self, Matrix):
            return Matrix([[self.elements[i][j] * other
                            for j in range(self.width)]
                           for i in range(self.height)])
        elif isinstance(other, Matrix) & isinstance(self, Matrix):
            if self.width == other.height:
                return Matrix([[self.product(self.elements[i], other.transpose().elements[j])
                                for j in range(other.width)]
                               for i in range(self.height)])
            else:
                raise NameError('Incorrect matrix sizes.')
        else:
            raise NameError('What did you enter?')

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(self, Matrix) & isinstance(other, (int, float)):
            return Matrix([[self.elements[i][j] * (1 / other)
                            for j in range(self.width)]
                           for i in range(self.height)])
        else:
            raise NameError('What did you enter?')

    def __invert__(self):
        if isinstance(self, Matrix) & self.is_square():
            return Matrix.inverse(self)
        else:
            raise NameError('The matrix is not square.')

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.elements[index]
        else:
            raise NameError('Index is not integer.')

    def is_square(self):
        return self.height == self.width

    def size(self):
        return len(self.elements), len(self.elements[0])

    def determinant(self):
        if isinstance(self, Matrix) & self.is_square():
            if self.height == 1:
                return self.elements[0][0]
            else:
                answer = 0
                for column, element in enumerate(self.elements[0]):
                    k = [i[:column] + i[column + 1:] for i in self.elements[1:]]
                    sign = 1 if column % 2 == 0 else -1
                    answer += sign * element * Matrix(k).determinant()
                return answer
        else:
            raise NameError('The matrix is not square.')

    def copy(self):
        tmp = []
        for r in self.elements:
            row = []
            for e in r:
                row.append(e)
            tmp.append(row)
        return Matrix(tmp)

    def minor(self, i, j):
        es = self.copy().elements
        es.pop(i)
        for r in range(len(es)):
            es[r].pop(j)
        return Matrix(es)

    def inverse(self):
        if isinstance(self, Matrix) & self.is_square():
            det = self.determinant()
            if det == 0:
                raise NameError('Matrix determinant = 0.')
            else:
                if self.height == 2:
                    return Matrix([[self.elements[1][1] / det, -1 * self.elements[0][1] / det],
                                   [-1 * self.elements[1][0] / det, self.elements[0][0] / det]])
                cofactors = []
                for height in range(self.height):
                    cofactor_row = []
                    for width in range(self.height):
                        minor = self.minor(height, width).determinant()
                        cofactor_row.append(((-1) ** (height + width)) * minor)
                    cofactors.append(cofactor_row)
                cofactors = Matrix(cofactors).transpose().elements
                for height in range(len(cofactors)):
                    for width in range(len(cofactors)):
                        cofactors[height][width] = cofactors[height][width] / det
                return Matrix(cofactors)
        else:
            raise NameError('The matrix is not square.')

    def transpose(self):
        return Matrix([[self.elements[j][i]
                        for j in range(self.height)]
                       for i in range(self.width)])

    def identity(self):
        if isinstance(self, int):
            return Matrix([[1 if i == j else 0 for i in range(self)] for j in range(self)])
        else:
            raise NameError('Please, enter integer value.')

    def product(self, first, second):
        return sum([first[i] * second[i] for i in range(len(first))])

    def gram_matrix(self):
        return Matrix([[self.product(self.elements[i], self.elements[j])
                        for i in range(self.height)]
                       for j in range(self.height)])

    def __str__(self):
        return '\n'.join([''.join(['{:8}'.format(round(item, 3)) for item in height]) for height in self.elements])


class Vector(Matrix):
    def __init__(self, vector: Matrix):
        if isinstance(vector, Matrix):
            vector = vector.elements
        if isinstance(vector[0], list):
            if len(vector[0]) == 1:
                self.as_matrix = Matrix(vector)
                self.vector = vector
                self.is_transposed = True
                self.dimension = len(vector)
            elif len(vector) == 1:
                self.as_matrix = Matrix(vector)
                self.vector = vector[0]
                self.is_transposed = False
                self.dimension = len(vector[0])
            else:
                raise Exception("Magic size of vector.")
        elif isinstance(vector[0], (int, float)):
            self.as_matrix = Matrix([vector])
            self.vector = vector
            self.is_transposed = False
            self.dimension = len(vector)

    def scalar_product(self, other):
        if isinstance(self, Vector) & isinstance(other, Vector):
            if self.dimension == other.dimension:
                return BilinearForm(Matrix.identity(self.dimension), self, other)
            else:
                raise NameError("Different sizes.")
        else:
            raise NameError("Enter vectors.")

    def vector_product(self, other):
        if isinstance(self, Vector) & isinstance(other, Vector):
            if self.dimension == 3 & other.dimension == 3:
                return Vector([self.vector[1] * other.vector[2] - self.vector[2] * other.vector[1],
                               self.vector[2] * other.vector[0] - self.vector[0] * other.vector[2],
                               self.vector[0] * other.vector[1] - self.vector[1] * other.vector[0]])
            else:
                raise NameError("Enter vectors in 3-dimensional space.")
        else:
            raise NameError("Enter vectors.")

    def length(self):
        return math.sqrt(self % self)

    def transpose(self):
        self.vector = Vector(self.as_matrix.transpose()).vector
        self.as_matrix = Vector(self.as_matrix.transpose()).as_matrix
        self.is_transposed = not(self.is_transposed)
        return self

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.as_matrix * other)
        else:
            NameError('Please, enter integer or float value.')

    __rmul__ = __mul__

    def __mod__(self, other):
        if isinstance(self, Vector) & isinstance(other, Vector):
            return Vector.scalar_product(self, other)
        else:
            raise NameError("Enter vectors.")

    def __pow__(self, other):
        return Vector.vector_product(self, other)

    def __getitem__(self, index: int):
        if isinstance(index, int):
            if self.is_transposed == False:
                return self.vector[index]
            else:
                return self.vector[index][0]
        else:
            raise NameError('Index is not integer.')

    def __add__(self, other):
        if isinstance(self, Vector) and isinstance(other, Vector):
            if self.dimension == other.dimension:
                return Vector(self.as_matrix + other.as_matrix)
            else:
                raise Exception("Different sizes.")
        else:
            raise NameError("Enter vectors.")

    def __sub__(self, other):
        if isinstance(self, Vector) and isinstance(other, Vector):
            if self.dimension == other.dimension:
                return Vector(self.as_matrix - other.as_matrix)
            else:
                raise Exception("Different sizes.")
        else:
            raise NameError("Enter vectors.")

    def __invert__(self):
        pass

    def is_square(self):
        pass

    def size(self):
        pass

    def determinant(self):
        pass

    def copy(self):
        pass

    def minor(self):
        pass

    def inverse(self):
        pass

    def identity(self):
        pass

    def gram_matrix(self):
        pass

    def __str__(self):
        return f'{self.vector}'


def BilinearForm(matrix, vector_1, vector_2):
    if matrix.height == matrix.width & matrix.height == vector_1.dimension & matrix.height == vector_2.dimension:
        return sum([matrix[i][j] * vector_1[i] * vector_2[j]
                    for i in range(matrix.height)
                    for j in range(matrix.height)])
    else:
        raise NameError('Different sizes of objects.')


class Point(Vector):
    def __add__(self, other):
        if isinstance(self, Point) & isinstance(other, Vector):
            if self.dimension == other.dimension:
                return Point([self[i] + other[i] for i in range(self.dimension)])
            else:
                raise Exception("Different sizes.")
        else:
            raise Exception("Error type of object.")

    __radd__ = __add__

    def __sub__(self, other: Vector):
        if isinstance(self, Point) & isinstance(other, Vector):
            if self.dimension == other.dimension:
                return Point([self[i] - other[i] for i in range(self.dimension)])
            else:
                raise Exception("Different sizes.")
        else:
            raise Exception("Error type of object.")

    def scalar_product(self, other):
        pass

    def vector_product(self, other):
        pass

    def length(self):
        pass

    def transpose(self):
        pass

    def __mul__(self, other):
        pass

    def __rmul__(self, other):
        pass

    def __mod__(self, other):
        pass

    def __pow__(self):
        pass

    def __invert__(self, other):
        pass


class VectorSpace:
    def __init__(self, basis):
        self.basis = Matrix([item.vector for item in basis])
        self.height = len(basis)

    def scalar_product(self, vector_1, vector_2):
        if vector_1.is_transposed == False & vector_2.is_transposed == False:
            return vector_1.as_matrix * self.basis.gram_matrix() * vector_2.transpose().as_matrix
        elif vector_1.is_transposed == False & vector_2.is_transposed:
            return vector_1.as_matrix * self.basis.gram_matrix() * vector_2.as_matrix
        elif vector_1.is_transposed & vector_2.is_transposed:
            return vector_1.transpose().as_matrix * self.basis.gram_matrix() * vector_2.as_matrix
        elif vector_1.is_transposed & vector_2.is_transposed == False:
            return vector_1.transpose().as_matrix * self.basis.gram_matrix() * vector_2.transpose().as_matrix

    def as_vector(self, point):
        if point.dimension == self.height:
            det = self.basis.determinant()
            answer = []
            for i in range(point.dimension):
                temp = self.basis.copy().transpose()
                for j in range(point.dimension):
                    temp[j][i] = point[j]
                answer.append(Matrix.determinant(temp) / det)
            return Vector(answer)
        else:
            raise NameError("Different sizes.")


class CoorinateSystem:
    def __init__(self, point: Point, vector_space: VectorSpace):
        self.point = point
