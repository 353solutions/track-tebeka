import yaml

import track
import pytest


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

def load_dist_cases():
    with open('dist_cases.yml') as fp:
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
