from lib.Engine.BasicClasses import *
from config.GlobalVariables import *
entity_1 = Entity(cs_global)
entity_2 = Entity(cs_global)
entities = EntitiesList([entity_1, entity_2])
data = Game(cs_global, entities)
print(data.cs)
result = data.camera(Point([1, 2, 3]), fov=100, draw_distance=100, direction=Vector([1, 2, 3]))
print(result.direction)
result_1 = data.hyper_plane(Point([0, 1, 2]), Vector([1, 2, 3]))
print(result_1.position)
from lib.Engine.BasicClasses import Game, EventSystem, Entity, EntitiesList
from config.GlobalVariables import *


game = Game(cs_global, entities=EntitiesList())

es = EventSystem({"move": [game.get_camera_class().move],
                  "horizontal_rotate": [game.get_camera_class().planar_rotate],
                  "vertical_rotate": [game.camera.set_direction]})
game.es = es


canvas = game.get_canvas_class()(40, 160)
canvas_mtr = canvas.res_matrix.elements
for i in range(canvas_mtr.rows):
    for j in range(canvas_mtr.columns):
        print(canvas_mtr[i][j])