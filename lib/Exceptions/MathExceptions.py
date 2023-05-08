class Exceptions(Exception):
    WRONG_TYPES = "Wrong object types."
    ZERO_DIVISION = "You can't divide by zero."


class MatrixExceptions(Exceptions):
    WRONG_INIT = "This is not matrix."
    WRONG_SIZES = "Different sizes of matrices."
    WRONG_SIZES_FOR_MULTIPLY = "Wrong sizes of matrices.The operation of multiplying " \
                               "two matrices is feasible only if the number of columns in the first " \
                               "multiplier is equal to the number of rows in the second."
    NOT_A_SQUARE = "This is not a square matrix."
    WRONG_DETERMINANT = "The determinant of the matrix is 0."
    NOT_EQUIVALENT = "The matrices are not equal."
    ROTATION_3D_ERROR = "This method can rotate only in three-dimensional."


class VectorExceptions(MatrixExceptions):
    WRONG_INIT = "This is not vectors."
    WRONG_VECTOR_PRODUCT = "Enter vectors in 3-dimensional space."
    WRONG_SIZES = "Different sizes of vectors."


class PointExceptions(MatrixExceptions):
    WRONG_SIZES = "Different sizes of points."


class VectorSpaceExceptions(Exceptions):
    WRONG_SIZES = "Different sizes of point and basis."
