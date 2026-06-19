import pytest

from s95 import helpers


min_to_try = ['17:00', '19:15', '23:30', '23:31', '24:58', '24:59', '25:01', '25:02', '18:45', '18:46', '59:59']


def min_converter(m):
    return sum(k * int(p) for k, p in zip([1 / 60, 1, 60], m.split(':')[::-1]))


@pytest.mark.parametrize('mmss', min_to_try)
def test_min_to_mmss(mmss):
    mins = min_converter(mmss)
    actual_mmss = helpers.min_to_mmss(mins)
    assert isinstance(actual_mmss, str)
    assert actual_mmss == mmss
    assert helpers.min_to_mmss(mins - 10**(-8)) == mmss
    assert helpers.min_to_mmss(mins + 10**(-8)) == mmss


# --- Tests for mmss_to_min ---

@pytest.mark.parametrize('time_str, expected_minutes', [
    ('23:45', 23.75),
    ('0:00', 0.0),
    ('0:30', 0.5),
    ('1:00', 1.0),
    ('59:59', 59.983333333333334),
    ('1:23:45', 83.75),
    ('0:00:30', 0.5),
    ('0:01:00', 1.0),
    ('1:00:00', 60.0),
])
def test_mmss_to_min_valid(time_str, expected_minutes):
    """Verify mmss_to_min returns correct decimal minutes for valid inputs."""
    result = helpers.mmss_to_min(time_str)
    assert isinstance(result, float)
    assert result == pytest.approx(expected_minutes, rel=1e-9)


def test_mmss_to_min_roundtrip():
    """Verify that min_to_mmss and mmss_to_min are inverses of each other."""
    original_times = ['17:00', '19:15', '23:30', '24:58', '25:01', '59:59']
    for time_str in original_times:
        minutes = helpers.mmss_to_min(time_str)
        roundtrip = helpers.min_to_mmss(minutes)
        assert roundtrip == time_str, f"Roundtrip failed for '{time_str}': got '{roundtrip}'"


@pytest.mark.parametrize('invalid_input', [
    '',
    'abc',
    '12:34:56:78',   # too many parts
    ':30',            # empty minutes
    '12::30',         # double colon
])
def test_mmss_to_min_invalid(invalid_input):
    """Verify mmss_to_min raises ValueError for malformed inputs."""
    with pytest.raises(ValueError):
        helpers.mmss_to_min(invalid_input)
