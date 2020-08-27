import factory
from factory import random

from app.models import user_model

random.reseed_random("skagit60")


class UserFactory(factory.Factory):
    class Meta:
        model = user_model.User

    username = factory.Faker("first_name")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    active = True


class UserInFactory(UserFactory):
    class Meta:
        model = user_model.UserIn

    hashed_password = factory.Faker("pystr", min_chars=30, max_chars=40)


class UserBeforeFactory(UserFactory):
    class Meta:
        model = user_model.UserBefore

    unhashed_password = factory.Faker("password")
