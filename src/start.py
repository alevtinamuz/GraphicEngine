from lib.Engine.BasicClasses import Game, EventSystem, Entity, EntitiesList
from config.GlobalVariables import *


game = Game(cs_global, entities=EntitiesList())

es = EventSystem({"move": [game.get_camera_class().move],
                  "horizontal_rotate": [game.get_camera_class().planar_rotate],
                  "vertical_rotate": [game.camera.set_direction]})
game.es = es


canvas = game.get_canvas_class()(80, 320)

camera = game.get_camera_class()(position=Point([-100, -100, 1]), direction=Vector([1, 1, 0]), fov=100, draw_distance=100)
camera.remove_property('identifier')
identifiers = []

# obj = g.get_hyper_ellipsoid_class()(position=Point([200, 200, 1]),
#                                     direction=Vector([2, 1, 1]),
#                                     semi_axes=[1, 1, 1])
#
# obj1 = g.get_hyper_ellipsoid_class()(position=Point([209, 203, 4]),
#                                      direction=Vector([2, 1, 1]),
#                                      semi_axes=[0.1, 2, 2])
#
# obj2 = g.get_hyper_ellipsoid_class()(position=Point([198, 204, 6]),
#                                      direction=Vector([2, 1, 1]),
#                                      semi_axes=[0.1, 3, 3])
#
# obj3 = g.get_hyper_ellipsoid_class()(position=Point([194, 201, -3]),
#                                      direction=Vector([2, 5, 2]),
#                                      semi_axes=[1, 2, 2])

hyper_plane = game.get_hyper_plane_class()(Point([10, 10, 0]), normal=Vector([-1, 0, 0]))
identifiers = hyper_plane.get_property('identifier')

canvas.update(camera)

game.run(canvas, camera)
