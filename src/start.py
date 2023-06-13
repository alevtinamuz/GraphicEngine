from lib.Engine.BasicClasses import *
from config.GlobalVariables import *


vs = VectorSpace([Vector([1, 0, 0]), Vector([0, 1, 0]), Vector([0, 0, 1])])
p1 = Point([0, 0, 0])
cs = CoordinateSystem(p1, vs)



g = Game(cs_global)
es = EventSystem({"move": [g.get_camera_class().move], "rotate_hor": [g.get_camera_class().planar_rotate],
                  "rotate_ver": [g.camera.set_direction]})
g.es = es


canv = g.get_canvas_class()()

camera = g.camera(position=Point([-100, -100, 1]), direction=Vector([1, 1, 0]), fov=100, draw_distance=100)

obj = g.get_hyper_ellipsoid_class()(position=Point([200, 200, 1]),
                               direction=Vector([2, 1, 1]),
                               semi_axes=[1, 1, 1])

obj1 = g.get_hyper_ellipsoid_class()(position=Point([209, 203, 4]),
                               direction=Vector([2, 1, 1]),
                               semi_axes=[0.1, 2, 2])

obj2 = g.get_hyper_ellipsoid_class()(position=Point([198, 204, 6]),
                               direction=Vector([2, 1, 1]),
                               semi_axes=[0.1, 3, 3])

obj3 = g.get_hyper_ellipsoid_class()(position=Point([194, 201, -3]),
                               direction=Vector([2, 5, 2]),
                               semi_axes=[1, 2, 2])

# obj1 = g.get_hyperplane()(Point([10, 10, 0]), normal=Vector([-1, 0, 0]))

canv.update(camera=camera)

g.run(canv, camera)
