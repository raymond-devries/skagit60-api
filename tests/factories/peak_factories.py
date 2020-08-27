import factory
from factory import random

from app.models import peak_model

random.reseed_random("skagit60")


class PeakInFactory(factory.Factory):
    class Meta:
        model = peak_model.PeakIn

    name = factory.Faker("sentence", nb_words=2)
    display_name = factory.Faker("sentence", nb_words=2)
    elevation = factory.Faker("pyint", max_value=20000)
    lat = factory.Faker("pyfloat", min_value=-90, max_value=90)
    long = factory.Faker("pyfloat", min_value=-180, max_value=180)
    state = factory.Faker("pystr")
    country = factory.Faker("country_code")
    peakbagger_link = factory.Faker("url")


class PeakWithSlugFactory(PeakInFactory):
    class Meta:
        model = peak_model.PeakWithSlug
