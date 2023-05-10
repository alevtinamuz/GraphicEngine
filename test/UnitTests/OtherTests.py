from lib.Engine.BasicClasses import *
entity_1 = Entity(cs_global)
entity_2 = Entity(cs_global)
entities_list = EntitiesList([entity_1, entity_2])
result = entities_list.exec(Entity.set_property('test', 'testing'))
print(result)
