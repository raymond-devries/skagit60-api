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


class UserSignUpFactory(UserFactory):
    class Meta:
        model = user_model.UserSignUp

    unhashed_password = factory.Faker("password")


class UserBeforeDbFactory(UserFactory):
    class Meta:
        model = user_model.UserBeforeDb

    active = True
    staff = False
    admin = False
    unhashed_password = factory.Faker("password")


class UserInDbFactory(UserFactory):
    class Meta:
        model = user_model.UserInDb

    active = True
    staff = False
    admin = False
    hashed_password = factory.Faker("pystr", min_chars=30, max_chars=40)
