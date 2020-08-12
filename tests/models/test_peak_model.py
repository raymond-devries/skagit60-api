import pytest

from app.models import peak_model


@pytest.fixture
def fake_peak() -> peak_model.Peak:
    return peak_model.Peak(
        name="test",
        display_name="testing",
        elevation=1000,
        lat=45.77,
        long=120.68,
        state="WA",
        country="USA",
        peakbagger_link="https://peakbagger.com/test",
    )


def test_slug_creation(fake_peak):
    assert fake_peak.slug == "testing-wa-usa-1000"
