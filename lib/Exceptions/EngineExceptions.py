class EngineExceptions(Exception):
    GET_PROPERTY_ERROR = "Can't get an object property."
    SET_PROPERTY_ERROR = "Can't set new object property."
    REMOVE_PROPERTY_ERROR = "Can't remove object property."
    ENTITY_NOT_EXIST = "Can't find this entity."
    ENTITY_LIST_ERROR = "Entity list hasn't any entities."
