from bson.objectid import ObjectId


class PydanticObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v) -> str:
        if isinstance(v, (str, ObjectId)):
            return str(v)
        else:
            raise TypeError(f"Expected str or ObjectId, got {type(v)}")
