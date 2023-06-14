from lib.Math.LowLevelMath import *


global identifiers
identifiers = []

global cs_global
cs_global = CoordinateSystem(Point([1.0, 0.0, 0.0]),
                             VectorSpace([Vector([1.0, 0.0, 0.0]), Vector([0.0, 1.0, 0.0]), Vector([0.0, 0.0, 1.0])]))
global canvas_n
canvas_n = 80

global canvas_m
canvas_m = 320

global draw_distance
draw_distance = 3000

global char_map
char_map = ".:;><+r*zsvfwqkP694VOGbUAKXH8RD#$B0MNWQ%&@"


