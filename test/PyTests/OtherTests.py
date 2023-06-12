from lib.Engine.BasicClasses import *
from lib.GlobalVariables import *
entity_1 = Entity(cs_global)
entity_2 = Entity(cs_global)
entities = EntitiesList([entity_1, entity_2])
data = Game(cs_global, entities)
print(data.cs)
result = data.camera(Point([1, 2, 3]), fov=100, draw_distance=100, direction=Vector([1, 2, 3]))
print(result.direction)
