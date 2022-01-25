import math
from pathlib import Path

import yaml
from hypothesis import given
from hypothesis.strategies import floats

import track
import pytest
from schema import track_schema


def test_smoke():
    pass


def test_distance():
    dist = track.distance(0, 0, 1, 1)
    assert 144.1700384962146 == dist


distance_cases = [
    # coord1, coord2, distance
    [(0, 0), (1, 1), 144.1700384962146],
    # [(1, 1), (1, 1), 0],
    pytest.param((1, 1), (1, 1), 0, id='same location'),
    # ...
]

# Exercise: Instead of reading tests from distance_cases, read then from
# dist_cases.yml
# You'll need to install PyYAML to read YAML files
# import yaml
# with open('tests/dist_cases.yml') as fp:
#    data = yaml.safe_load(fp)  # data is a list of dicts

tests_dir = Path(__file__).absolute().parent


def load_dist_cases():
    with open(tests_dir / 'dist_cases.yml') as fp:
        data = yaml.safe_load(fp)

    cases = []
    for case in data:
        coord1 = (case['lat1'], case['lng1'])
        coord2 = (case['lat2'], case['lng2'])
        cases.append([coord1, coord2, case['distance']])
    return cases


@pytest.mark.parametrize('coord1, coord2, expected', load_dist_cases())
def test_distance_many(coord1, coord2, expected):
    lat1, lng1 = coord1
    lat2, lng2 = coord2
    dist = track.distance(lat1, lng1, lat2, lng2)
    assert expected == dist


def test_distance_type_error():
    with pytest.raises(TypeError):
        track.distance('1', 1, 0, 0)

    # try:
    #     track.distance('1', 1, 0, 0)
    #     assert False, 'did not raise'
    # except TypeError:
    #     pass


# from hypothesis import given
# from hypothesis.strategies import floats

@given(floats(), floats(), floats(), floats())
def test_distance_fuzz(lat1, lng1, lat2, lng2):
    # print(lat1, lng1, lat2, lng2)
    # run: python -m pytest -s
    dist = track.distance(lat1, lng1, lat2, lng2)
    if math.isnan(dist):
        return
    assert dist >= 0

# from schema import track_schema
def test_load_track():
    csv_file = tests_dir / 'track.csv'
    df = track.load_track(csv_file)
    track_schema.validate(df)


"""
Running tests:
- python -m flake8 track.py tests
- python -m pytest -v
"""