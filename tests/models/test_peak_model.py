from tests import factories


def test_slug_creation():
    fake_peak = factories.PeakFactory(
        display_name="testing", state="WA", country="USA", elevation=1000
    )
    assert fake_peak.slug == "testing-wa-usa-1000"
