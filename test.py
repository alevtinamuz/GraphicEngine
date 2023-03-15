from GraphicEngine import *

point_1 = Point(1, 1, 5)
point_2 = Point(2, 3, 6)

InitialPt = VectorSpace(
    initial_point = Point(0, 0, 0),
    basis_x = Vector(1, 0, 0),
    basis_y = Vector(0, 1, 0),
    basis_z = Vector(0, 0, 1)
)

vector_1 = Vector(2, 3, 4)
vector_2 = Vector(1, 2, 3)
vector_3 = Vector(point_1)



print("................ТОЧКИ................")
<<<<<<< HEAD
=======
print("point as list: ", point_1.as_list())
>>>>>>> origin/master
print("sum of two points: ", point_1 + point_2)
print("difference of two points: ", point_1 - point_2)
print("point * number: ", point_1 * 5.5)
print("number * point: ", 5.5 * point_1)
print("point / number: ", point_1 / 2)
<<<<<<< HEAD
print("distance between two points: ", Point.distance(point_1, point_2))
print("\n")
print("...............ВЕКТОРЫ...............")
=======
print("distance between two points: ", Point.distance_between(point_1, point_2))
print("\n")
print("...............ВЕКТОРЫ...............")
print("vector as list: ", vector_1.as_list())
>>>>>>> origin/master
print("vector as point: ", vector_3)
print("sum of two vectors: ", vector_1 + vector_2)
print("difference of two vectors: ", vector_1 - vector_2)
print("vector * number: ", vector_1 * 5)
print("number * vector: ", 5 * vector_1)
print("scalar product of vectors: ", vector_1 * vector_2)
print("vector product of vectors: ", vector_2 ** vector_1)
print("normalized vector: ", Vector.normalize(vector_1))
