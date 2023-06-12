import pytest

from lib.Math.LowLevelMath import *


class TestMatrix:
    def test_init(self):
        matrix = Matrix([[2.0, 3.0],
                         [5.1, 3.8],
                         [8.5, 8.0]])

        result = isinstance(matrix, Matrix)

        assert result

    def test_exception_init(self):
        with pytest.raises(MatrixExceptions):
            result = Matrix([[1.0, 2.0],
                             [3.0]])

            assert result

    def test_is_square(self):
        matrix = Matrix([[8.0, 8.0, 8.0],
                         [8.0, 8.0, 8.0],
                         [8.0, 8.0, 8.0]])

        result = (matrix.is_square() is True)

        assert result

    def test_size(self):
        matrix = Matrix([[8.0, 8.0],
                         [8.0, 8.0],
                         [8.0, 8.0]])

        result = (matrix.size() == (3, 2))

        assert result

    def test_determinant(self):
        matrix = Matrix([[1.0, 2.0, 3.0],
                        [4.0, 5.0, 6.0],
                        [7.0, 8.0, 9.0]])

        result = (matrix.determinant() == 0)

        assert result

    def test_exception_determinant(self):
        with pytest.raises(MatrixExceptions):
            result = Matrix([[8.0, 8.0],
                             [8.0, 8.0],
                             [8.0, 8.0]]).determinant()

            assert result

    def test_copy(self):
        matrix = Matrix([[8.0, 8.0],
                         [8.0, 8.0],
                         [8.0, 8.0]])

        result = (matrix.copy() == matrix)

        assert result

    def test_minor(self):
        matrix = Matrix([[8.0, 8.0],
                         [8.0, 8.0],
                         [8.0, 8.0]])

        matrix_minor = Matrix([[8.0],
                               [8.0],
                               [8.0]])

        result = (matrix.minor(1, 1) == matrix_minor)

        assert result

    def test_inverse(self):
        matrix = Matrix([[2.0, 1.0, 0.0, 0.0],
                        [3.0, 2.0, 0.0, 0.0],
                        [1.0, 1.0, 3.0, 4.0],
                        [2.0, -1.0, 2.0, 3.0]])

        matrix_inverse = Matrix([[2.0, -1.0, 0.0, 0.0],
                                [-3.0, 2.0, 0.0, 0.0],
                                [31.0, -19.0, 3.0, -4.0],
                                [-23.0, 14.0, -2.0, 3.0]])

        result = (~matrix == matrix_inverse)

        assert result

    def test_exception_inverse_not_a_square(self):
        with pytest.raises(MatrixExceptions):
            result = Matrix([[8.0, 8.0],
                            [8.0, 8.0],
                            [8.0, 8.0]]).inverse()

            assert result

    def test_exception_inverse_det_0(self):
        with pytest.raises(MatrixExceptions):
            result = Matrix([[1.0, 2.0, 3.0],
                            [4.0, 5.0, 6.0],
                            [7.0, 8.0, 9.0]]).inverse()
            assert result

    def test_transpose(self):
        matrix_1 = Matrix([[2.0, 4.0],
                           [6.0, 2.0],
                           [8.0, 8.0]])

        matrix_2 = Matrix([[2.0, 6.0, 8.0],
                           [4.0, 2.0, 8.0]])

        result = (matrix_1.transpose() == matrix_2)

        assert result

    def test_identity(self):
        matrix = Matrix([[1.0, 0.0, 0.0],
                        [0.0, 1.0, 0.0],
                        [0.0, 0.0, 1.0]])

        result = (matrix == Matrix.identity(3))

        assert result

    def test_zero_matrix(self):
        matrix = Matrix([[0, 0, 0],
                        [0, 0, 0]])
        print(matrix)
        print(Matrix.zero_matrix(2, 3))
        result = (matrix == Matrix.zero_matrix(2, 3))

        assert result

    def test_product_of_lists(self):
        matrix = Matrix([[1.0, 1.0, 0.0],
                         [0.0, 2.0, 0.0],
                         [0.0, 0.0, 1.0]])

        result = (Matrix.product(matrix[0], matrix[1]) == 2.0)

        assert result

    def test_gram(self):
        matrix = Matrix([[1.0, 2.0],
                         [3.0, 4.0]]).gram()

        matrix_gram = Matrix([[5.0, 11.0],
                              [11.0, 25.0]])

        result = (matrix == matrix_gram)

        assert result

    def test_equal(self):
        matrix = Matrix([[1.0, 2.0, 3.0],
                         [4.0, 5.0, 6.0],
                         [7.0, 8.0, 9.0]])

        result = (matrix == matrix)

        assert result

    def test_exception_equal(self):
        with pytest.raises(MatrixExceptions):
            matrix = Matrix([[1.0, 2.0, 3.0],
                            [4.0, 5.0, 6.0],
                            [7.0, 8.0, 9.0]])

            result = (matrix == matrix.minor(1, 1))

            assert result

    def test_additional(self):
        matrix_1 = Matrix([[2.0, 3.0],
                           [5.1, 3.8],
                           [8.5, 8.0]])

        matrix_2 = Matrix([[2.0, 3.0],
                           [5.1, 3.8],
                           [8.5, 8.0]])

        matrix_3 = Matrix([[4.0, 6.0],
                           [10.2, 7.6],
                           [17.0, 16.0]])

        result = ((matrix_1 + matrix_2) == matrix_3)

        assert result

    def test_exception_additional_wrong_types(self):
        with pytest.raises(MatrixExceptions):
            matrix = Matrix([[2.0, 3.0],
                             [5.1, 3.8],
                             [8.5, 8.0]])

            result = (matrix + 2)

            assert result

    def test_exception_additional_wrong_sizes(self):
        with pytest.raises(MatrixExceptions):
            matrix_1 = Matrix([[2.0, 3.0],
                               [5.1, 3.8],
                               [8.5, 8.0]])

            matrix_2 = Matrix([[2.0],
                               [5.1],
                               [8.5]])

            result = (matrix_1 + matrix_2)

            assert result

    def test_difference(self):
        matrix_1 = Matrix([[2.0, 3.0],
                           [5.1, 3.8],
                           [8.5, 8.0]])

        matrix_2 = Matrix([[2.0, 3.0],
                           [5.1, 3.8],
                           [8.5, 8.0]])

        matrix_3 = Matrix([[0.0, 0.0],
                           [0.0, 0.0],
                           [0.0, 0.0]])

        result = ((matrix_1 - matrix_2) == matrix_3)

        assert result

    def test_exception_difference_wrong_types(self):
        with pytest.raises(MatrixExceptions):
            matrix = Matrix([[2.0, 3.0],
                             [5.1, 3.8],
                             [8.5, 8.0]])

            result = (matrix - 3)

            assert result

    def test_exception_difference_wrong_sizes(self):
        with pytest.raises(MatrixExceptions):
            matrix_1 = Matrix([[2.0, 3.0],
                               [5.1, 3.8],
                               [8.5, 8.0]])

            matrix_2 = Matrix([[2.0],
                               [5.1],
                               [8.5]])

            result = (matrix_1 - matrix_2)

            assert result

    def test_multiply_matrix_by_scalar(self):
        matrix_1 = Matrix([[2.0, 4.0],
                           [6.0, 2.0],
                           [8.0, 8.0]])

        matrix_2 = Matrix([[4.0, 8.0],
                           [12.0, 4.0],
                           [16.0, 16.0]])

        result = ((matrix_1 * 2) == matrix_2)

        assert result

    def test_multiply_scalar_by_matrix(self):
        matrix_1 = Matrix([[2.0, 4.0],
                           [6.0, 2.0],
                           [8.0, 8.0]])

        matrix_2 = Matrix([[4.0, 8.0],
                           [12.0, 4.0],
                           [16.0, 16.0]])

        result = ((2 * matrix_1) == matrix_2)

        assert result

    def test_product_of_matrices(self):
        matrix_1 = Matrix([[1.0, 2.0, 3.0],
                           [4.0, 5.0, 6.0],
                           [7.0, 8.0, 9.0]])

        matrix_2 = Matrix([[1.0, 2.0, 1.0],
                           [1.0, 2.0, 1.0],
                           [1.0, 2.0, 1.0]])

        matrix_3 = Matrix([[6.0, 12.0, 6.0],
                           [15.0, 30.0, 15.0],
                           [24.0, 48.0, 24.0]])

        result = ((matrix_1 * matrix_2) == matrix_3)

        assert result

    def test_exception_multiply_wrong_types(self):
        with pytest.raises(MatrixExceptions):
            matrix = Matrix([[2.0, 4.0],
                             [6.0, 2.0],
                             [8.0, 8.0]])

            vector = Vector([1.0, 2.0, 3.0])

            result = (matrix * vector)

            assert result

    def test_exception_multiply_wrong_sizes(self):
        with pytest.raises(MatrixExceptions):
            matrix_1 = Matrix([[2.0, 4.0],
                               [6.0, 2.0],
                               [8.0, 8.0]])

            matrix_2 = Matrix([[2.0, 4.0, 8.0],
                               [6.0, 2.0, 8.0],
                               [8.0, 8.0, 8.0]])

            result = (matrix_1 * matrix_2)

            assert result

    def test_division(self):
        matrix_1 = Matrix([[2.0, 4.0],
                           [6.0, 2.0],
                           [8.0, 8.0]])

        matrix_2 = Matrix([[1.0, 2.0],
                           [3.0, 1.0],
                           [4.0, 4.0]])

        result = ((matrix_1 / 2) == matrix_2)

        assert result

    def test_exception_division_wrong_types(self):
        with pytest.raises(MatrixExceptions):
            matrix_1 = Matrix([[2.0, 4.0],
                               [6.0, 2.0],
                               [8.0, 8.0]])

            matrix_2 = Matrix([[2.0, 4.0],
                               [6.0, 2.0],
                               [8.0, 8.0]])

            result = (matrix_1 / matrix_2)

            assert result

    def test_exception_zero_division(self):
        with pytest.raises(MatrixExceptions):
            matrix_1 = Matrix([[2.0, 4.0],
                               [6.0, 2.0],
                               [8.0, 8.0]])

            result = (matrix_1 / 0)

            assert result

    def test_rotate(self):
        matrix = Matrix([[1.0, 2.0], [3.0, 4.0]])

        matrix_rotated = Matrix([[2.0, -1.0], [4.0, -3.0]])

        result = (matrix.rotate(1, 0, 90) == matrix_rotated)

        assert result


class TestVector:

    def test_init(self):
        vector = Vector([1.0, 2.0, 3.0])

        result = isinstance(vector, Vector)

        assert result

    def test_exception_init(self):
        with pytest.raises(VectorExceptions):
            vector = Vector(1.0)

            result = isinstance(vector, Vector)

            assert result

    def test_as_matrix(self):
        vector_1 = Vector([0.0, 0.0, 0.0]).as_matrix()
        matrix_1 = Matrix([[0.0, 0.0, 0.0]])

        result = (vector_1 == matrix_1)

        assert result

    def test_scalar_product(self):
        vector_1 = Vector([0.0, 0.0, 0.0])
        vector_2 = Vector(Matrix([[1.8, 2.1, 4.5]]))

        result = (vector_1 % vector_2 == 0.0)

        assert result

    def test_exception_scalar_product_wrong_types(self):
        with pytest.raises(VectorExceptions):
            vector_1 = Vector([0.0, 0.0, 0.0])
            vector_2 = Matrix([[1.8, 2.1, 4.5]])

            result = (vector_1 % vector_2)

            assert result

    def test_exception_scalar_product_wrong_sizes(self):
        with pytest.raises(VectorExceptions):
            vector_1 = Vector([0.0, 0.0, 0.0])
            vector_2 = Vector(Matrix([[1.8, 2.1]]))

            result = (vector_1 % vector_2)

            assert result

    def test_vector_product(self):
        vector_1 = Vector([1.0, 2.0, 3.0])
        vector_2 = Vector(Matrix([[1.0, 2.0, 4.0]]))
        vector_answer = Vector([2.0, -1.0, 0.0])

        result = (vector_1 ** vector_2 == vector_answer)

        assert result

    def test_exception_vector_product_wrong_types(self):
        with pytest.raises(VectorExceptions):
            vector_1 = Vector([1.0, 2.0, 3.0])
            vector_2 = Matrix([[1.8, 2.1, 4.5]])

            result = (vector_1 ** vector_2)

            assert result

    def test_exception_vector_product_wrong_dimensional_space(self):
        with pytest.raises(VectorExceptions):
            vector_1 = Vector([1.0, 2.0, 3.0, 4.0])
            vector_2 = Vector([[1.8, 2.1, 4.5, 5.0]])

            result = (vector_1 ** vector_2)

            assert result

    def test_length(self):
        vector = Vector([3.0, 4.0, 0.0])

        result = (vector.length() == 5.0)

        assert result

    def test_transpose(self):
        vector = Vector([3.0, 4.0, 0.0])
        vector_transposed = Vector([[3.0], [4.0], [0.0]])

        result = (vector.transpose() == vector_transposed)

        assert result

    def test_rotate(self):
        vector = Vector([1.0, 2.0, 3.0])

        result = (vector.rotate(1, 0, 90) == Vector([2.0, -1.0, 3.0]))

        assert result

    def test_addition(self):
        vector_1 = Vector([0.0, 0.0, 0.0])
        vector_2 = Vector(Matrix([[1.8, 2.1, 4.5]]))

        result = (vector_1 + vector_2 == vector_2)

        assert result

    def test_exception_addition_wrong_types(self):
        with pytest.raises(VectorExceptions):
            vector_1 = Vector([0.0, 0.0, 0.0])
            vector_2 = Vector(1.0)

            result = (vector_1 + vector_2)

            assert result

    def test_exception_addition_wrong_sizes(self):
        with pytest.raises(VectorExceptions):
            vector_1 = Vector([0.0, 0.0, 0.0])
            vector_2 = Vector(Matrix([[1.8, 2.1]]))

            result = (vector_1 + vector_2)

            assert result

    def test_difference(self):
        vector_1 = Vector([0.0, 0.0, 0.0])
        vector_2 = Vector(Matrix([[1.8, 2.1, 4.5]]))

        result = (vector_2 - vector_1 == vector_2)

        assert result

    def test_exception_difference_wrong_types(self):
        with pytest.raises(VectorExceptions):
            vector_1 = Vector([0.0, 0.0, 0.0])
            vector_2 = Vector(1.0)

            result = (vector_2 - vector_1)

            assert result

    def test_exception_difference_wrong_sizes(self):
        with pytest.raises(VectorExceptions):
            vector_1 = Vector([0.0, 0.0, 0.0])
            vector_2 = Vector(Matrix([[1.8, 2.1]]))

            result = (vector_2 - vector_1)

            assert result

    def test_multiply_vector_by_scalar(self):
        vector_1 = Vector([1.0, 2.0, 3.0])
        vector_2 = Vector(Matrix([[2.0, 4.0, 6.0]]))

        result = (vector_1 * 2 == vector_2)

        assert result

    def test_multiply_scalar_by_vector(self):
        vector_1 = Vector([1.0, 2.0, 3.0])
        vector_2 = Vector(Matrix([[2.0, 4.0, 6.0]]))

        result = (2 * vector_1 == vector_2)

        assert result

    def test_multiply_vectors(self):
        vector_1 = Vector([1.0, 2.0, 3.0])
        vector_2 = Vector([[2.0], [4.0], [6.0]])
        vector_answer = Vector([28])

        result = (vector_1 * vector_2 == vector_answer)

        assert result

    def test_exception_multiply_wrong_types(self):
        with pytest.raises(Exceptions):
            vector_1 = Vector([0.0, 0.0, 0.0])
            vector_2 = Vector(1.0)

            result = (vector_2 * vector_1)

            assert result

    def test_exception_multiply_wrong_sizes(self):
        with pytest.raises(MatrixExceptions):
            vector_1 = Vector([0.0, 0.0, 0.0])
            vector_2 = Vector(Matrix([[1.8, 2.1]]))

            result = (vector_2 * vector_1)

            assert result

    def test_division_vector_by_scalar(self):
        vector_1 = Vector([2.0, 4.0, 8.0])
        vector_2 = Vector([1.0, 2.0, 4.0])

        result = (vector_1 / 2 == vector_2)

        assert result

    def test_exception_division_wrong_types(self):
        with pytest.raises(VectorExceptions):
            vector_1 = Vector([0.0, 0.0, 0.0])
            vector_2 = Vector(1.0)

            result = (vector_2 / vector_1)

            assert result

    def test_exception_division_zero(self):
        with pytest.raises(VectorExceptions):
            vector_1 = Vector([1.0, 2.0, 3.0])

            result = (vector_1 / 0)

            assert result


class TestPoint:
    def test_init(self):
        point = Point([1.0, 2.0, 3.0])

        result = isinstance(point, Point)

        assert result

    def test_additional_point_vector(self):
        point = Point([1.0, 2.0, 3.0])
        vector = Vector([1.0, 2.0, 3.0])
        additional = Point([2.0, 4.0, 6.0])

        result = (point + vector == additional)

        assert result

    def test_additional_vector_point(self):
        point = Point([1.0, 2.0, 3.0])
        vector = Vector([1.0, 2.0, 3.0])
        additional = Point([2.0, 4.0, 6.0])

        result = (vector + point == additional)

        assert result

    def test_exception_additional_wrong_types(self):
        with pytest.raises(PointExceptions):
            point = Point([1.0, 2.0, 4.0])
            matrix = Matrix([[2.0]])

            assert (point + matrix)

    def test_exception_additional_wrong_sizes(self):
        with pytest.raises(PointExceptions):
            point = Point([1.0, 2.0, 3.0])
            vector = Vector([1.0, 2.0])

            assert (point + vector)

    def test_difference_point_vector(self):
        point = Point([1.0, 2.0, 3.0])
        vector = Vector([1.0, 2.0, 3.0])
        additional = Point([0.0, 0.0, 0.0])

        result = (point - vector == additional)

        assert result

    def test_exception_difference_wrong_types(self):
        with pytest.raises(PointExceptions):
            point = Point([1.0, 2.0, 4.0])
            matrix = Matrix([[2.0]])

            assert (point - matrix)

    def test_exception_difference_wrong_sizes(self):
        with pytest.raises(VectorExceptions):
            point = Point([1.0, 2.0, 3.0])
            vector = Vector([1.0, 2.0])

            assert (vector - point)


class TestVectorSpace:
    def test_init(self):
        vector_space = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])

        result = isinstance(vector_space, VectorSpace)

        assert result

    def test_scalar_product(self):
        vector_space = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
        vector_1 = Vector([1.0, 2.0, 3.0])
        vector_2 = Vector([1.0, 2.0, 3.0])

        result = (vector_space.scalar_product(vector_1, vector_2) == vector_1 % vector_2)

        assert result

    def test_as_vector(self):
        vector_space = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
        point = Point([1.0, 2.0, 3.0])
        point_as_vector = Vector([1.0, 2.0, 3.0])

        result = (vector_space.as_vector(point) == point_as_vector)

        assert result

    def test_exception_as_vector_wrong_sizes(self):
        with pytest.raises(MatrixExceptions):
            vector_space = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
            point = Point([1.0, 2.0])

            result = (vector_space.as_vector(point))

            assert result

    def test_vector_product(self):
        vector_1 = Vector([1.0, 2.0, 3.0])
        vector_2 = Vector(Matrix([[1.0, 2.0, 4.0]]))
        vector_space = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
        vector_answer = Vector([2.0, -1.0, 0.0])

        result = (VectorSpace.vector_product(vector_space, vector_1, vector_2) == vector_answer)

        assert result


class TestCoordinateSystem:
    def test_init(self):
        point = Point([1.0, 2.0, 3.0])
        vector_space = VectorSpace([Vector([1.0, 0.0, 0.0]), Vector([0.0, 1.0, 0.0]), Vector([0.0, 0.0, 1.0])])

        result = isinstance(CoordinateSystem(point, vector_space), CoordinateSystem)

        assert result

