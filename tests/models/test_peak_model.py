from tests.factories import peak_factories


def test_slug_creation():
    fake_peak = peak_factories.PeakWithSlugFactory(
        display_name="testing", state="WA", country="USA", elevation=1000
    )
    assert fake_peak.slug == "testing-wa-usa-1000"
