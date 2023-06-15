from lib.Engine.BasicClasses import Game, EventSystem, EntitiesList
from config.GlobalVariables import *


game = Game(cs_global, entities=EntitiesList())

es = EventSystem({"move": [game.get_camera_class().move],
                  "horizontal_rotate": [game.get_camera_class().planar_rotate],
                  "vertical_rotate": [game.camera.set_direction]})
game.es = es


canvas = game.get_canvas_class()(20, 80)

camera = game.get_camera_class()(position=Point([-6000, -6000, 1]),
                                 direction=Vector([1, 1, 0]),
                                 fov=0.02, draw_dist=draw_distance)

hyper_ellipsoid_1 = game.get_hyper_ellipsoid_class()(position=Point([-1, -5, -1]),
                                                     direction=Vector([2, 2, 2]),
                                                     semi_axes=[1, 1, 1])

hyper_ellipsoid_2 = game.get_hyper_ellipsoid_class()(position=Point([-3.9, -5.9, 2]),
                                                     direction=Vector([1, 1, 1]),
                                                     semi_axes=[0.5, 0.5, 0.5])

# hyper_plane = game.get_hyper_plane_class()(Point([2, 2, 2]), normal=Vector([1, 1, 1]))

canvas.update(camera)

game.run(canvas, camera)
