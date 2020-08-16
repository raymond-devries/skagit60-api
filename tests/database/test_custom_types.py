import pytest
from bson.objectid import ObjectId

from app.models.custom_types import PydanticObjectId


def test_pydantic_object_id_str():
    assert PydanticObjectId.validate("test_str") == "test_str"


def test_pydantic_object_id_object_id():
    assert (
        PydanticObjectId.validate(ObjectId("5f39bbe8f81387beb70d511b"))
        == "5f39bbe8f81387beb70d511b"
    )


def test_pydantic_object_id_wrong_type():
    with pytest.raises(TypeError):
        PydanticObjectId.validate(78)
