from lib.Engine.BasicClasses import Game, EventSystem, Entity, EntitiesList
from config.GlobalVariables import *


game = Game(cs_global, entities=EntitiesList())

es = EventSystem({"move": [game.get_camera_class().move],
                  "horizontal_rotate": [game.get_camera_class().planar_rotate],
                  "vertical_rotate": [game.camera.set_direction]})
game.es = es


canvas = game.get_canvas_class()(40, 160)

camera = game.get_camera_class()(position=Point([-100, -100, 1]), direction=Vector([1, 1, 0]), fov=80, draw_dist=draw_distance)
camera.remove_property('identifier')
identifiers = []

# hyper_ellipsoid = game.get_hyper_ellipsoid_class()(position=Point([200, 200, 1]),
#                                     direction=Vector([2, 1, 1]),
#                                     semi_axes=[1, 1, 1])
# identifiers = hyper_ellipsoid.get_property('identifier')
#
hyper_plane = game.get_hyper_plane_class()(Point([10, 10, 0]), normal=Vector([-1, 0, 0]))
identifiers = hyper_plane.get_property('identifier')

canvas.update(camera)

game.run(canvas, camera)
