import pytest
from lib.Engine.BasicClasses import *


class TestRay:
    def test_init(self):
        direction = Vector([1.0, 2.0, 3.0])

        result = isinstance(Ray(cs_global, Point([1.0, 2.0, 3.0]), direction), Ray)

        assert result


class TestIdentifier:
    def test_init(self):
        identifier_1 = Identifier()
        identifier_2 = Identifier()

        result = (len(identifiers) == 2)

        assert result

    def test_get_value(self):
        identifier = Identifier()
        result = (Identifier.get_value(2) == identifier.identifier)

        assert result


class TestEntity:
    def test_init(self):
        result = isinstance(Entity(cs_global), Entity)

        assert result

    def test_set_get_property(self):
        entity = Entity(cs_global)
        entity['test'] = 'testing'

        result = [entity['test'] == 'testing']

        assert result

    def test_remove_property(self):
        with pytest.raises(EngineExceptions):
            entity = Entity(cs_global)
            entity['test'] = 'testing'
            del entity['test']

            result = (entity['test'] is None)

            assert result


class TestEntitiesList:
    def test_init(self):
        entity_1 = Entity(cs_global)
        entity_2 = Entity(cs_global)
        entity_3 = Entity(cs_global)

        result = isinstance(EntitiesList([entity_1, entity_2, entity_3]), EntitiesList)

        assert result

    def test_append(self):
        entity_1 = Entity(cs_global)
        entity_2 = Entity(cs_global)
        entity_3 = Entity(cs_global)
        entities_list = EntitiesList([entity_1, entity_2])
        entities_list.append(entity_3)

        result = (len(entities_list.entities) == 3)

        assert result

    def test_remove(self):
        entity_1 = Entity(cs_global)
        entity_2 = Entity(cs_global)
        entity_3 = Entity(cs_global)
        entities_list = EntitiesList([entity_1, entity_2, entity_3])
        entities_list.remove(entity_3)

        result = (len(entities_list.entities) == 2)

        assert result

    def test_get(self):
        entity_1 = Entity(cs_global)
        entity_2 = Entity(cs_global)
        entity_3 = Entity(cs_global)
        entities_list = EntitiesList([entity_1, entity_2, entity_3])
        result = (entities_list[entity_2['identifier']] == entity_2)

        assert result

    def test_exec(self):
        entity_1 = Entity(cs_global)
        entity_2 = Entity(cs_global)
        entities_list = EntitiesList([entity_1, entity_2])
        res = exec(entities_list, Entity.set_property)

        for i in entities_list:
            res = i

    # def test_