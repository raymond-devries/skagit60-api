import factory
from factory import random

from app.models import user_model

random.reseed_random("skagit60")


class UserInFactory(factory.Factory):
    class Meta:
        model = user_model.UserIn

    username = factory.Faker("first_name")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    hashed_password = factory.Faker("pystr", min_chars=30, max_chars=40)
    active = True
